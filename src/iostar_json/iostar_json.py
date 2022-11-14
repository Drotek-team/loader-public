import json
from typing import List

from pydantic import BaseModel


class Show(BaseModel):
    binary_dances: List[
        List[int]
    ]  # List of the dance composing the show with  List of integer symbolising the list of octect


class IostarJson(BaseModel):
    show: Show

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: IostarJson):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
