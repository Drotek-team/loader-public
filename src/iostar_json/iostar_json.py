import json
from typing import List

from pydantic import BaseModel


class IostarJson(BaseModel):
    binary_dances: List[List[int]]  # List of the dance in binary composing the show

    def get_json(self) -> str:
        class DummyClass:
            def __init__(self, show: IostarJson):
                self.show = show

        return json.dumps(
            DummyClass(self), default=lambda o: o.__dict__, sort_keys=True, indent=4
        )
