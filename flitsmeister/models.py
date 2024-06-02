"""Models for FM."""

from __future__ import annotations

from contextlib import suppress
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Any

import jwt

@dataclass
class Auth:
    """Represent Auth data."""    
    object_id: str
    session_token: str
    access_token: str
    
    access_token_expires: datetime
    
    def __init__(self, session_token: str, access_token: str):
        self.session_token = session_token
        self.access_token = access_token
        
        with suppress(jwt.ExpiredSignatureError):
            decoded_jwt = jwt.decode(self.access_token, options={"verify_signature": False})
            self.object_id = decoded_jwt.get("sub")
            self.access_token_expires = datetime.fromtimestamp(decoded_jwt.get("exp"))
    
    @property
    def is_access_token_expired(self) -> bool:
        """Check if the access token is expired."""
        return datetime.now() > self.access_token_expires

    @staticmethod
    def from_dict(data: dict[str, str]) -> Auth:
        """TODO"""
        
        return Auth(
            session_token=data.get("sessionToken"),
            access_token=data.get("accessToken"),
        )

@dataclass
class User:
    """Represent User data."""

    fourfouroneone_ev_enabled: bool
    fourfouroneone_parking_enabled: bool
    fourfouroneone_payment_method_set: bool
    access_token: str
    first_name: str
    gender: int
    has_4411_account: bool
    object_id: str
    parking_enabled: bool
    session_token: str
    statistics_top_speed: int
    statistics_top_sprint: int
    statistics_travel_distance: int
    statistics_travel_time: int
    username: str
    vehicle_type: int
    
    @staticmethod
    def from_dict(data: dict[str, Any]) -> User:
        """TODO"""
        return User(
            fourfouroneone_ev_enabled=data.get("4411EvEnabled"),
            fourfouroneone_parking_enabled=data.get("4411ParkingEnabled"),
            fourfouroneone_payment_method_set=data.get("4411PaymentMethodSet"),
            access_token=data.get("accessToken"),
            first_name=data.get("firstName"),
            gender=data.get("gender"),
            has_4411_account=data.get("has4411Account"),
            object_id=data.get("objectId"),
            parking_enabled=data.get("parkingEnabled"),
            session_token=data.get("sessionToken"),
            statistics_top_speed=data.get("statistics").get("topSpeed"),
            statistics_top_sprint=data.get("statistics").get("topSprint"),
            statistics_travel_distance=data.get("statistics").get("travelDistance"),
            statistics_travel_time=data.get("statistics").get("travelTime"),
            username=data.get("username"),
            vehicle_type=data.get("vehicleType"),
        )
    
@dataclass
class Statistics:
    """Represent Statistics data."""
    
    ambassador: bool
    countries_visited: list[str]
    fines_avoided: int
    km_driven: int
    navigation_finished: int
    parked_once: bool
    provinces_visited: list[str]
    recruiter: int
    sec_driven: int
    times_in_traffic: int
    top_100_sprint_ms: int
    top_consecutive_days: int
    top_speed: int
    total_ratings: int
    
    @staticmethod
    def from_dict(data: dict[str, int]) -> Statistics:
        """TODO"""
        data = data.get("result")
        return Statistics(
            ambassador=data.get("ambassador"),
            countries_visited=data.get("countries_visited"),
            fines_avoided=data.get("fines_avoided"),
            km_driven=data.get("km_driven"),
            navigation_finished=data.get("navigation_finished"),
            parked_once=data.get("parked_once"),
            provinces_visited=data.get("provinces_visited"),
            recruiter=data.get("recruiter"),
            sec_driven=data.get("sec_driven"),
            times_in_traffic=data.get("times_in_traffic"),
            top_100_sprint_ms=data.get("top_100_sprint_ms"),
            top_consecutive_days=data.get("top_consecutive_days"),
            top_speed=data.get("top_speed"),
            total_ratings=data.get("total_ratings"),
        )
