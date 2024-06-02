"""Flitsmeister Python API."""

from __future__ import annotations

import logging
from typing import Any, TypeVar

import async_timeout
from aiohttp.client import ClientSession
from aiohttp.hdrs import METH_GET, METH_POST

from .models import Auth, Statistics, User

_LOGGER = logging.getLogger(__name__)

T = TypeVar("T")

ENDPOINT = "https://account.flitsmeister.app/"


class NotauthenticatedException(Exception):
    """Not authenticated exception."""


class FM:
    """Implementation of Flitsmeister."""

    _session: ClientSession | None
    _close_session: bool = False
    _request_timeout: int = 10

    _auth: Auth | None = None

    def __init__(
        self,
        client_session: ClientSession = None,
        request_timeout: int = 10,
        auth: Auth | None = None,
    ):
        """Create a FM object.

        Args:
            client_session: The client session.
            request_timeout: Request timeout in seconds.
            auth: Auth object.
        """

        self._session = client_session
        self._request_timeout = request_timeout
        self._auth = auth

    async def login(self, username: str, password: str) -> Auth:
        """Login to the API.

        https://account.flitsmeister.app/parse/login { "_method": "GET", "password": "<password>", "username": "<email>"}
        {
            "objectId": "1EqBUC03nK",
            "sessionToken": "r:b866...",
            "accessToken": "eyJhbGci...",
            (And a lot more -for now irrelevant- data)
        }
        """

        response = await self._request(
            "parse/login",
            METH_POST,
            {"_method": "GET", "username": username, "password": password},
        )
        return Auth.from_dict(response)

    async def user(self) -> User:
        """Get user information.

        https://account.flitsmeister.app/parse/classes/_User/<USER_ID>
        {
            "4411EvEnabled": false,
            "4411ParkingEnabled": true,
            "4411PaymentMethodSet": true,
            "ACL": {
                "*": {
                    "read": true
                },
                "1EqBUC03nK": {
                    "read": true,
                    "write": true
                }
            },
            "accepted_privacy": {
                "policy-25-05-2018": true,
                "terms-25-05-2018": true
            },
            "accessToken": "eyJhbG...",
            "authProvider": "apple",
            "authProviders": [
                "email",
                "apple"
            ],
            "birthday": {
                "__type": "Date",
                "iso": "1995-01-20T00:00:00.000Z"
            },
            "country_code": "NL",
            "createdAt": "2019-11-13T11:55:46.431Z",
            "firstName": "D...",
            "gender": 1,
            "has4411Account": true,
            "invitesEnabled": true,
            "lastCarplaySession": {
                "__type": "Date",
                "iso": "2024-05-31T16:08:53.154Z"
            },
            "lastParkingSession": {
                "__type": "Date",
                "iso": "2024-04-04T15:37:32.525Z"
            },
            "linkedFlitsmeisterONE": false,
            "locale": "nl-NL",
            "objectId": "1Eq...",
            "parkingEnabled": true,
            "picture": {
                "__type": "Bytes",
                "base64": "/9j/4AAQSkZJRgABAQAASAB..."
            },
            "sessionToken": "r:de..",
            "statistics": {
                "topSpeed": 413,
                "topSprint": 1,
                "travelDistance": 59,
                "travelTime": 158824560000
            },
            "updatedAt": "2024-06-02T08:27:37.276Z",
            "username": "flit...@...",
            "validated": true,
            "vehicleType": 1
        }

        """

        if self._auth is None:
            raise NotauthenticatedException

        response = await self._request(
            f"parse/classes/_User/{self._auth.object_id}", METH_GET, {}
        )
        return User.from_dict(response)

    async def statistics(self) -> Statistics:
        """Get user statistics.

        https://account.flitsmeister.app/parse/functions/fetchStatistics
        {
            "result": {
                "ambassador": true,
                "countries_visited": [
                    "NL",
                    "DE",
                    "BE",
                ],
                "fines_avoided": 210,
                "km_driven": 63550,
                "navigation_finished": 301,
                "parked_once": true,
                "provinces_visited": [
                    "NL-ZH",
                    "NL-UT",
                    "NL-GE",
                    "NL-NH",
                    "NL-LI",
                    "NL-OV",
                    "NL-FL",
                    "NL-NB",
                    "BE-VAN",
                    "BE-VOV",
                    "NL-DR",
                    "BE-VBR"
                ],
                "recruiter": 0,
                "sec_driven": 162900000,
                "times_in_traffic": 500,
                "top_100_sprint_ms": 4000,
                "top_consecutive_days": 61,
                "top_speed": 413,
                "total_ratings": 450,
                "ufo_km_driven": 30205
            }
        }
        """

        if self._auth is None:
            raise NotauthenticatedException

        response = await self._request("parse/functions/fetchStatistics", METH_POST, {})
        return Statistics.from_dict(response)

    async def _request(
        self, path: str, method: str = METH_GET, data: object = None
    ) -> Any:
        """Make a request to the API."""
        if self._session is None:
            self._session = ClientSession()
            self._close_session = True

        headers = {"Content-Type": "application/json"}
        if self._auth is not None:
            headers["x-parse-session-token"] = self._auth.session_token

        url = f"{ENDPOINT}{path}"
        _LOGGER.debug("%s, %s, %s", method, url, data)

        async with async_timeout.timeout(self._request_timeout):
            resp = await self._session.request(
                method,
                url,
                json=data,
                headers=headers,
            )
            _LOGGER.debug("%s, %s", resp.status, await resp.text("utf-8"))

        content_type = resp.headers.get("Content-Type", "")
        if "application/json" in content_type:
            return await resp.json()

        return await resp.text()

    async def close(self) -> None:
        """Close client session."""
        _LOGGER.debug("Closing clientsession")
        if self._session and self._close_session:
            await self._session.close()

    async def __aenter__(self) -> FM:
        """Async enter.

        Returns:
            The FM object.
        """
        return self

    async def __aexit__(self, *_exc_info: Any) -> None:
        """Async exit.

        Args:
            _exc_info: Exec type.
        """
        await self.close()
