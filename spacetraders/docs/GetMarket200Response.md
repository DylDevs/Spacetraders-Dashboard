# GetMarket200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**Market**](Market.md) |  | 

## Example

```python
from spacetraders.models.get_market200_response import GetMarket200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetMarket200Response from a JSON string
get_market200_response_instance = GetMarket200Response.from_json(json)
# print the JSON string representation of the object
print(GetMarket200Response.to_json())

# convert the object into a dict
get_market200_response_dict = get_market200_response_instance.to_dict()
# create an instance of GetMarket200Response from a dict
get_market200_response_from_dict = GetMarket200Response.from_dict(get_market200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


