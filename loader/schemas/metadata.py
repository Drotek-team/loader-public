from typing import Optional

from pydantic import BaseModel

from loader import __version__


class Metadata(BaseModel):
    loader_version: str = __version__
    lightshow_creator_version: Optional[str] = None
    blender_version: Optional[str] = None
