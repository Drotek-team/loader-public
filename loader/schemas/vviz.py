# ruff: noqa: A003, N815
from enum import Enum
from typing import TYPE_CHECKING, List, Optional, Tuple, Union

from pydantic import BaseModel

if TYPE_CHECKING:
    from . import ColorEventUser, DroneUser, FireEventUser, PositionEventUser, ShowUser


class ExportType(Enum):
    VVIZ = "VVIZ"
    Finale3D = "Finale 3D"

    def convert_enu_coordinates(
        self,
        xyz: Tuple[float, float, float],
    ) -> Tuple[float, float, float]:  # pragma: no cover
        if self == ExportType.VVIZ:
            return xyz[0], xyz[2], xyz[1]
        if self == ExportType.Finale3D:
            return xyz[0], xyz[2], -xyz[1]
        msg = f"Unknown export type {self}"
        raise NotImplementedError(msg)


class GlobalReferenceFrame(BaseModel):
    lat: float
    lon: float
    alt: float


class PositionDeltaSample(BaseModel):
    dt: Optional[float] = None
    dx: float
    dy: float
    dz: float


class AgentDescription(BaseModel):
    homeX: float
    homeY: float
    homeZ: float
    airframe: str
    agentTraversal: List[PositionDeltaSample]

    @classmethod
    def from_position_events(
        cls, positions: List["PositionEventUser"], airframe: str, export_type: ExportType
    ) -> "AgentDescription":
        agent_traversal: List[PositionDeltaSample] = []
        if positions[0].frame != 0:
            agent_traversal.append(
                PositionDeltaSample(
                    dt=positions[0].frame / 24,
                    dx=0,
                    dy=0,
                    dz=0,
                )
            )
        last_frame = positions[0].frame
        last_xyz = positions[0].xyz
        for position in positions[1:]:
            dx = position.xyz[0] - last_xyz[0]
            dy = position.xyz[1] - last_xyz[1]
            dz = position.xyz[2] - last_xyz[2]
            dx, dy, dz = export_type.convert_enu_coordinates((dx, dy, dz))
            dt = (position.frame - last_frame) / 24
            last_frame = position.frame
            last_xyz = position.xyz
            agent_traversal.append(
                PositionDeltaSample(
                    dt=dt if dt != 1 / 4 else None,
                    dx=dx,
                    dy=dy,
                    dz=dz,
                )
            )
        home_x, home_y, home_z = export_type.convert_enu_coordinates(positions[0].xyz)
        return AgentDescription(
            homeX=home_x,
            homeY=home_y,
            homeZ=home_z,
            airframe=airframe,
            agentTraversal=agent_traversal,
        )


class LightSample(BaseModel):
    r: int
    g: int
    b: int
    w: int
    frames: Optional[int] = None


class LigthPayloadDescription(BaseModel):
    id: int = 0
    type: str = "Light"
    lumens: float
    colorType: str = "RGBW"
    sourceType: str
    payloadActions: List[LightSample]

    @classmethod
    def from_color_events(
        cls,
        colors: List["ColorEventUser"],
        lumens: float,
        source_type: str,
    ) -> "LigthPayloadDescription":
        payload_actions: List[LightSample] = []
        if colors[0].frame != 0:
            payload_actions.append(
                LightSample(
                    r=0,
                    g=0,
                    b=0,
                    w=0,
                )
            )
        last_frame = 0
        for color in colors:
            frames = color.frame - last_frame
            last_frame = color.frame
            payload_actions.append(
                LightSample(
                    r=round(color.rgbw[0] * 255),
                    g=round(color.rgbw[1] * 255),
                    b=round(color.rgbw[2] * 255),
                    w=round(color.rgbw[3] * 255),
                    frames=frames if frames > 1 else None,
                )
            )

        return LigthPayloadDescription(
            lumens=lumens,
            sourceType=source_type,
            payloadActions=payload_actions,
        )


class PyroPayloadDescription(BaseModel):
    id: int
    type: str = "Pyro"
    eventTime: float
    vdl: str
    partNumber: str = ""

    @classmethod
    def from_fire_events(
        cls,
        fires: List["FireEventUser"],
        vdl: str,
    ) -> List["PyroPayloadDescription"]:
        return [
            PyroPayloadDescription(id=index + 1, eventTime=24 * fire.frame, vdl=vdl)
            for index, fire in enumerate(fires)
        ]


class Performance(BaseModel):
    id: int
    agentDescription: AgentDescription
    payloadDescription: List[Union[LigthPayloadDescription, PyroPayloadDescription]]

    @classmethod
    def from_drone_user(
        cls,
        drone_user: "DroneUser",
        export_type: ExportType,
        airframe: str,
        lumens: float,
        source_type: str,
        vdl: str,
    ) -> "Performance":
        return Performance(
            id=drone_user.index,
            agentDescription=AgentDescription.from_position_events(
                drone_user.position_events, airframe, export_type
            ),
            payloadDescription=[
                LigthPayloadDescription.from_color_events(
                    drone_user.color_events, lumens, source_type
                ),
                *PyroPayloadDescription.from_fire_events(drone_user.fire_events, vdl),
            ],
        )


class Vviz(BaseModel):
    version: str = "1.0"
    performanceName: str
    coordinateFrame: str = "ogl"
    globalReferenceFrame: Optional[GlobalReferenceFrame] = None
    defaultPositionRate: float = 4
    defaultColorRate: float = 24
    performances: List[Performance]

    @classmethod
    def from_show_user(
        cls,
        show_user: "ShowUser",
        *,
        performance_name: str,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
        alt: Optional[float] = None,
        export_type: ExportType,
        airframe: str = "IOStar",
        lumens: float = 900.0,
        source_type: str = "Dome",
        vdl: str = "10s Gold Glittering Gerb",
    ) -> "Vviz":
        global_reference_frame = (
            GlobalReferenceFrame(lat=lat, lon=lon, alt=alt)
            if lat is not None and lon is not None and alt is not None
            else None
        )
        performances = [
            Performance.from_drone_user(drone_user, export_type, airframe, lumens, source_type, vdl)
            for drone_user in show_user.drones_user
        ]
        return Vviz(
            performanceName=performance_name,
            globalReferenceFrame=global_reference_frame,
            performances=performances,
        )
