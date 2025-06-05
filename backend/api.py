import backend.variables as Variables
import concurrent.futures as futures
from backend.logger import Logger
from dataclasses import dataclass
from typing import Literal
import threading
import requests
import time

logger = Logger()

# Variables for rate limiting and concurrency
RATE_LIMIT = 2 # Requests per second
THREADS = 3 # Number of threads to parallelize the downloads

class RateLimiter:
    def __init__(self):
        self.limiter = threading.Semaphore(0)
        self.waiting = False

        threading.Thread(target=self._thread).start()

    def _thread(self):
        while True:
            if not self.waiting:
                time.sleep(0.1)
            self.limiter.release(RATE_LIMIT)
            time.sleep(1.1)

    def Wait(self):
        self.waiting += 1
        self.limiter.acquire()
        self.waiting -= 1

rate_limiter = RateLimiter()

@dataclass
class Request:
    path : str
    method : Literal["GET", "POST", "PATCH"] = "GET"
    json : dict = None
    headers : dict = None
    timeout : int = 5

@dataclass
class Response:
    success : bool = False
    data : dict | None = None
    error : dict | None = None
    status_code : int = None
    other_tags : dict = None

def _APIRequest(request : Request) -> Response:
    '''
    Rate limited API fetcher, not meant to be called directly
    '''
    
    # Ensure the request headers have the mandatory Content-Type and Authorization headers
    if not request.headers:
        request.headers = {}
    request.headers['Content-Type'] = 'application/json'
    request.headers['Authorization'] = f'Bearer {Variables.agent_token}'

    rate_limiter.Wait()
    try:
        response = None
        for _ in range(2): # Retry in case of timeout
            try: 
                if request.method == "GET":
                    response = requests.get(f"https://api.spacetraders.io/v2{request.path}", headers=request.headers, timeout=request.timeout)
                elif request.method == "POST":
                    response = requests.post(f"https://api.spacetraders.io/v2{request.path}", headers=request.headers, json=request.json, timeout=request.timeout)
                elif request.method == "PATCH":
                    response = requests.patch(f"https://api.spacetraders.io/v2{request.path}", headers=request.headers, json=request.json, timeout=request.timeout)
                else:
                    return Response(
                        error="Unknown API request method",
                        status_code=405 # Method Not Allowed
                    )
                break # Success
            except requests.exceptions.Timeout: # Timeout
                response = None
            except Exception as e: # Unknown error
                return Response(
                    error=f"Unknown error while making API request: {str(e)}",
                    status_code=500 # Internal Server Error
                )

        if response is None: # Timed out twice
            return Response(
                error="API request timed out",
                status_code=504 # Gateway Timeout
            )
        
        json_response : dict = response.json()
        
        if response.status_code != 200: # Non-200 status code
            return Response(
                error=f"{response.status_code} - {json_response['error']['message']}",
                status_code=response.status_code
            )
        
        if 'data' in json_response: # Endpoint returns data inside of a data key
            data = json_response['data']
            other_tags = json_response.copy()
            del other_tags['data']
        else:
            data = json_response
            other_tags = None

        return Response(
            success=True,
            data=data,
            status_code=response.status_code,
            other_tags=other_tags
        )
    except Exception as e:
        return Response(
            error=f"Unkown error in _APIRequest: {str(e)}",
            status_code=500
        )
        
def Handler(request : Request) -> Response:
    '''
    Rate-limited API handler
    '''
    if not isinstance(request, Request):
        raise Exception("APIHandler must be initialized with an APIRequest object")
        
    return _APIRequest(request)

class ThreadedHandler:
    '''
    Threaded and rate-limited API handler
    '''
    def __init__(self, requests : list[Request] = []):
        self.running = True
        self.queue : list[Response] = []
        self.executor = futures.ThreadPoolExecutor(max_workers=THREADS)
        self.requests : list[Request] = []

        # Spacetraders API starts at page 1
        self.index = 1

        for request in requests: # If the request is an APIRequest, add it to the list
            if isinstance(request, Request):
                self.requests.append(request)
        self.total = len(self.requests)
        
        for request in self.requests: # When the executor completes a request, the response is added to the queue
            self.executor.submit(_APIRequest, request).add_done_callback(self._on_complete)
    
        return None
    
    def _on_complete(self, future : futures.Future[Response]):
        try:
            result = future.result()
            self.queue.append({"data": result})
        except Exception as e:
            self.queue.append({"error": str(e)})
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.running = False
        self.executor.shutdown()
        return None
    
    def AwaitResponse(self) -> Response | None:
        while not self.queue: # Empty queue (response not ready)
            if self.index - 1 >= self.total: # No more requests to make
                self.running = False
            if not self.running:
                return None
            time.sleep(0.05)

        response = self.queue.pop() # Return the last response added to the list, and remove it
        if "error" in response: # If the response has an error, raise an exception
            raise Exception(response["error"])
        
        self.index += 1
        return response["data"]