from typing import List

from pydantic import BaseModel


class IostarJson(BaseModel):
    binary_dances: List[List[int]]  # List of the dance in binary composing the show
