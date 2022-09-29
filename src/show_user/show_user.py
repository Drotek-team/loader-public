from pydantic import BaseModel
from typing import List
from .drone_user.drone_user import DroneUser
from .family_user.family_user import FamilyUser


class ShowUser(BaseModel):
    drones_user: List[DroneUser]
    family_user: FamilyUser
