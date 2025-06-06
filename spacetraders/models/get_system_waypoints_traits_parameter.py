# coding: utf-8

"""
    SpaceTraders API

    SpaceTraders is an open-universe game and learning platform that offers a set of HTTP endpoints to control a fleet of ships and explore a multiplayer universe.  The API is documented using [OpenAPI](https://github.com/SpaceTradersAPI/api-docs). You can send your first request right here in your browser to check the status of the game server.  ```json http {   \"method\": \"GET\",   \"url\": \"https://api.spacetraders.io/v2\", } ```  Unlike a traditional game, SpaceTraders does not have a first-party client or app to play the game. Instead, you can use the API to build your own client, write a script to automate your ships, or try an app built by the community.  We have a [Discord channel](https://discord.com/invite/jh6zurdWk5) where you can share your projects, ask questions, and get help from other players.   

    The version of the OpenAPI document: 2.3.0
    Contact: joel@spacetraders.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import orjson as json
import pprint
from pydantic import BaseModel, ConfigDict, Field, StrictStr, ValidationError, field_validator
from typing import Any, List, Optional
from spacetraders.models.waypoint_trait_symbol import WaypointTraitSymbol
from pydantic import StrictStr, Field
from typing import Union, List, Set, Optional, Dict
from typing_extensions import Literal, Self

GETSYSTEMWAYPOINTSTRAITSPARAMETER_ONE_OF_SCHEMAS = ["List[WaypointTraitSymbol]", "WaypointTraitSymbol"]

class GetSystemWaypointsTraitsParameter(BaseModel):
    """
    GetSystemWaypointsTraitsParameter
    """
    # data type: WaypointTraitSymbol
    oneof_schema_1_validator: Optional[WaypointTraitSymbol] = None
    # data type: List[WaypointTraitSymbol]
    oneof_schema_2_validator: Optional[List[WaypointTraitSymbol]] = None
    actual_instance: Optional[Union[List[WaypointTraitSymbol], WaypointTraitSymbol]] = None
    one_of_schemas: Set[str] = { "List[WaypointTraitSymbol]", "WaypointTraitSymbol" }

    model_config = ConfigDict(
        validate_assignment=True,
        protected_namespaces=(),
    )


    def __init__(self, *args, **kwargs) -> None:
        if args:
            if len(args) > 1:
                raise ValueError("If a position argument is used, only 1 is allowed to set `actual_instance`")
            if kwargs:
                raise ValueError("If a position argument is used, keyword arguments cannot be used.")
            super().__init__(actual_instance=args[0])
        else:
            super().__init__(**kwargs)

    @field_validator('actual_instance')
    def actual_instance_must_validate_oneof(cls, v):
        instance = GetSystemWaypointsTraitsParameter.model_construct()
        error_messages = []
        match = 0
        # validate data type: WaypointTraitSymbol
        if not isinstance(v, WaypointTraitSymbol):
            error_messages.append(f"Error! Input type `{type(v)}` is not `WaypointTraitSymbol`")
        else:
            match += 1
        # validate data type: List[WaypointTraitSymbol]
        try:
            instance.oneof_schema_2_validator = v
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when setting `actual_instance` in GetSystemWaypointsTraitsParameter with oneOf schemas: List[WaypointTraitSymbol], WaypointTraitSymbol. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when setting `actual_instance` in GetSystemWaypointsTraitsParameter with oneOf schemas: List[WaypointTraitSymbol], WaypointTraitSymbol. Details: " + ", ".join(error_messages))
        else:
            return v

    @classmethod
    def from_dict(cls, obj: Union[str, Dict[str, Any]]) -> Self:
        return cls.from_json(json.dumps(obj))

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Returns the object represented by the json string"""
        instance = cls.model_construct()
        error_messages = []
        match = 0

        # deserialize data into WaypointTraitSymbol
        try:
            instance.actual_instance = WaypointTraitSymbol.from_json(json_str)
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))
        # deserialize data into List[WaypointTraitSymbol]
        try:
            # validation
            instance.oneof_schema_2_validator = json.loads(json_str)
            # assign value to actual_instance
            instance.actual_instance = instance.oneof_schema_2_validator
            match += 1
        except (ValidationError, ValueError) as e:
            error_messages.append(str(e))

        if match > 1:
            # more than 1 match
            raise ValueError("Multiple matches found when deserializing the JSON string into GetSystemWaypointsTraitsParameter with oneOf schemas: List[WaypointTraitSymbol], WaypointTraitSymbol. Details: " + ", ".join(error_messages))
        elif match == 0:
            # no match
            raise ValueError("No match found when deserializing the JSON string into GetSystemWaypointsTraitsParameter with oneOf schemas: List[WaypointTraitSymbol], WaypointTraitSymbol. Details: " + ", ".join(error_messages))
        else:
            return instance

    def to_json(self) -> str:
        """Returns the JSON representation of the actual instance"""
        if self.actual_instance is None:
            return "null"

        if hasattr(self.actual_instance, "to_json") and callable(self.actual_instance.to_json):
            return self.actual_instance.to_json()
        else:
            return json.dumps(self.actual_instance)

    def to_dict(self) -> Optional[Union[Dict[str, Any], List[WaypointTraitSymbol], WaypointTraitSymbol]]:
        """Returns the dict representation of the actual instance"""
        if self.actual_instance is None:
            return None

        if hasattr(self.actual_instance, "to_dict") and callable(self.actual_instance.to_dict):
            return self.actual_instance.to_dict()
        else:
            # primitive type
            return self.actual_instance

    def to_str(self) -> str:
        """Returns the string representation of the actual instance"""
        return pprint.pformat(self.model_dump())


