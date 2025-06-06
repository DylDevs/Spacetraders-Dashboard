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
from enum import Enum
from typing_extensions import Self


class ShipRole(str, Enum):
    """
    The registered role of the ship
    """

    """
    allowed enum values
    """
    FABRICATOR = 'FABRICATOR'
    HARVESTER = 'HARVESTER'
    HAULER = 'HAULER'
    INTERCEPTOR = 'INTERCEPTOR'
    EXCAVATOR = 'EXCAVATOR'
    TRANSPORT = 'TRANSPORT'
    REPAIR = 'REPAIR'
    SURVEYOR = 'SURVEYOR'
    COMMAND = 'COMMAND'
    CARRIER = 'CARRIER'
    PATROL = 'PATROL'
    SATELLITE = 'SATELLITE'
    EXPLORER = 'EXPLORER'
    REFINERY = 'REFINERY'

    @classmethod
    def from_json(cls, json_str: str) -> Self:
        """Create an instance of ShipRole from a JSON string"""
        return cls(json.loads(json_str))


