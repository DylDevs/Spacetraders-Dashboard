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
import pprint
import re  # noqa: F401
import orjson as json

from pydantic import BaseModel, ConfigDict, Field
from typing import Any, ClassVar, Dict, List
from spacetraders.models.agent import Agent
from spacetraders.models.ship_cargo import ShipCargo
from spacetraders.models.ship_modification_transaction import ShipModificationTransaction
from spacetraders.models.ship_mount import ShipMount
from typing import Optional, Set
from typing_extensions import Self

class RemoveMount201ResponseData(BaseModel):
    """
    RemoveMount201ResponseData
    """ # noqa: E501
    agent: Agent
    mounts: List[ShipMount] = Field(description="List of installed mounts after the removal of the selected mount.")
    cargo: ShipCargo
    transaction: ShipModificationTransaction
    __properties: ClassVar[List[str]] = ["agent", "mounts", "cargo", "transaction"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of RemoveMount201ResponseData from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of agent
        if self.agent:
            _dict['agent'] = self.agent.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in mounts (list)
        _items = []
        if self.mounts:
            for _item_mounts in self.mounts:
                if _item_mounts:
                    _items.append(_item_mounts.to_dict())
            _dict['mounts'] = _items
        # override the default output from pydantic by calling `to_dict()` of cargo
        if self.cargo:
            _dict['cargo'] = self.cargo.to_dict()
        # override the default output from pydantic by calling `to_dict()` of transaction
        if self.transaction:
            _dict['transaction'] = self.transaction.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of RemoveMount201ResponseData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "agent": Agent.from_dict(obj["agent"]) if obj.get("agent") is not None else None,
            "mounts": [ShipMount.from_dict(_item) for _item in obj["mounts"]] if obj.get("mounts") is not None else None,
            "cargo": ShipCargo.from_dict(obj["cargo"]) if obj.get("cargo") is not None else None,
            "transaction": ShipModificationTransaction.from_dict(obj["transaction"]) if obj.get("transaction") is not None else None
        })
        return _obj


