# GetFaction200Response


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**Faction**](Faction.md) |  | 

## Example

```python
from spacetraders.models.get_faction200_response import GetFaction200Response

# TODO update the JSON string below
json = "{}"
# create an instance of GetFaction200Response from a JSON string
get_faction200_response_instance = GetFaction200Response.from_json(json)
# print the JSON string representation of the object
print(GetFaction200Response.to_json())

# convert the object into a dict
get_faction200_response_dict = get_faction200_response_instance.to_dict()
# create an instance of GetFaction200Response from a dict
get_faction200_response_from_dict = GetFaction200Response.from_dict(get_faction200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


