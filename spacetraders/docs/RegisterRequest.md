# RegisterRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**faction** | [**FactionSymbol**](FactionSymbol.md) |  | 
**symbol** | **str** | Your desired agent symbol. This will be a unique name used to represent your agent, and will be the prefix for your ships. | 
**email** | **str** | Your email address. This is used if you reserved your call sign between resets. | [optional] 

## Example

```python
from spacetraders.models.register_request import RegisterRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RegisterRequest from a JSON string
register_request_instance = RegisterRequest.from_json(json)
# print the JSON string representation of the object
print(RegisterRequest.to_json())

# convert the object into a dict
register_request_dict = register_request_instance.to_dict()
# create an instance of RegisterRequest from a dict
register_request_from_dict = RegisterRequest.from_dict(register_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


