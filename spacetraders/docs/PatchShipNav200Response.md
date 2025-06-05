# PatchShipNav200Response

Success response for updating the nav configuration of a ship.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**PatchShipNav200ResponseData**](PatchShipNav200ResponseData.md) |  | 

## Example

```python
from spacetraders.models.patch_ship_nav200_response import PatchShipNav200Response

# TODO update the JSON string below
json = "{}"
# create an instance of PatchShipNav200Response from a JSON string
patch_ship_nav200_response_instance = PatchShipNav200Response.from_json(json)
# print the JSON string representation of the object
print(PatchShipNav200Response.to_json())

# convert the object into a dict
patch_ship_nav200_response_dict = patch_ship_nav200_response_instance.to_dict()
# create an instance of PatchShipNav200Response from a dict
patch_ship_nav200_response_from_dict = PatchShipNav200Response.from_dict(patch_ship_nav200_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


