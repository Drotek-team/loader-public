"""Metadata of the show."""

from typing import Optional

from pydantic import BaseModel

from loader import __version__


class Metadata(BaseModel):
    """Metadata of the show."""

    loader_version: str = __version__
    """The version of the loader that created the show."""
    lightshow_creator_version: Optional[str] = None
    """The version of the Lightshow Creator that created the show (if applicable)."""
    blender_version: Optional[str] = None
    """The version of Blender that created the show (if applicable)."""
