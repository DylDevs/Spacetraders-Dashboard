# GetSystems200Response



## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[System]**](System.md) |  | 
**meta** | [**Meta**](Meta.md) |  | 

## Example

```python
from spacetraders.models.get_systems200_response import GetSystems200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetSystems200Response from a JSON string
get_systems200_response_instance = GetSystems200Response.from_json(json)
# print the JSON string representation of the object
print(GetSystems200Response.to_json())

# convert the object into a dict
get_systems200_response_dict = get_systems200_response_instance.to_dict()
# create an instance of GetSystems200Response from a dict
get_systems200_response_from_dict = GetSystems200Response.from_dict(get_systems200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


