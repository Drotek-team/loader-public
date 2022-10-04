from pydantic import BaseModel
from typing import List
from .drone_user.drone_user import DroneUser
from .family_user.family_user import FamilyUser
import json


class ShowUser(BaseModel):
    drones_user: List[DroneUser]
    family_user: FamilyUser

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: ShowUser):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
