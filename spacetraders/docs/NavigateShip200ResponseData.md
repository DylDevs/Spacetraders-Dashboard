# NavigateShip200ResponseData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fuel** | [**ShipFuel**](ShipFuel.md) |  | 
**nav** | [**ShipNav**](ShipNav.md) |  | 
**events** | [**List[ShipConditionEvent]**](ShipConditionEvent.md) |  | 

## Example

```python
from spacetraders.models.navigate_ship200_response_data import NavigateShip200ResponseData

# TODO update the JSON string below
json = "{}"
# create an instance of NavigateShip200ResponseData from a JSON string
navigate_ship200_response_data_instance = NavigateShip200ResponseData.from_json(json)
# print the JSON string representation of the object
print(NavigateShip200ResponseData.to_json())

# convert the object into a dict
navigate_ship200_response_data_dict = navigate_ship200_response_data_instance.to_dict()
# create an instance of NavigateShip200ResponseData from a dict
navigate_ship200_response_data_from_dict = NavigateShip200ResponseData.from_dict(navigate_ship200_response_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


