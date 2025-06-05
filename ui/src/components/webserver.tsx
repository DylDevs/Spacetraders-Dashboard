// @ts-ignore | Prevents module not found error from js-cookie, even though it is installed
import Cookies from 'js-cookie';

async function FetchServer(extension: string, body: any = {}, method : string = "GET", error : boolean = true) {
  const webserver_url = Cookies.get("webserver_url")
  try {
    let response = await fetch(webserver_url + extension, {
      method: method,
      headers: {
        "Content-Type": "application/json",
      },
      ...(method !== "GET" && method !== "HEAD" ? { body: JSON.stringify(body) } : {}),
    });
  
    if (!response.ok && error) {
      throw new Error("Response was not ok to URL: " + webserver_url + " (Response Status: " + response.status + ")");
    } else if (!response.ok && !error) {
      return false;
    }

    let data = await response.json();

    if (data.status !== "ok" && error) {
      throw new Error(data.traceback);
    } else if (data.status !== "ok" && !error) {
      return data;
    }

    return data;
  } catch (e) {
    if (error) {
      if (e instanceof Error) {
        throw new Error("Failed to get data from server: " + e.message);
      } else {
        throw new Error("Failed to get data from server: " + e);
      }
    }
  }
}

export async function AttemptServerConnection(test_webserver_url : string) {
  Cookies.set("webserver_url", test_webserver_url);
  let connected = true;

  let data = await FetchServer("", {}, "GET", false);
  if (data) {
    console.log(data)
    connected = true;
    Cookies.set("webserver_url", test_webserver_url);
  } else {
    Cookies.set("webserver_url", "https://localhost:8000");
    connected = false;
  }

  return connected;
}

export async function GetSystems() {
  // @ts-ignore
  const data : {status: string, systems: Array} = await FetchServer("/systems");
  return data.systems;
}

export async function GetCurrentSystem() {
  // @ts-ignore
  const data : {status: string, symbol: string} = await FetchServer("/systems/current");
  return data.symbol;
}

export async function GetWaypoints(system_symbol : string | null = null) {
  if (system_symbol === null) {
    system_symbol = await GetCurrentSystem();
  }

  // @ts-ignore
  const data : {status: string, waypoints: Array} = await FetchServer("/systems/" + system_symbol + "/waypoints");
  return {symbol: system_symbol, waypoints: data.waypoints};
}