from pydantic import BaseModel, Field


class PowerFlowNodeBody(BaseModel):
    client_id: str
    device_id: int
    x: float
    y: float
    width: float = 190
    height: float = 104


class PowerFlowJunctionBody(BaseModel):
    client_id: str
    x: float
    y: float


class PowerFlowWireBody(BaseModel):
    client_id: str
    source_type: str
    source_ref: str
    source_anchor: str
    target_type: str
    target_ref: str
    target_anchor: str
    direction: str = "FORWARD"
    metric_key: str | None = None
    is_enabled: bool = True
    route_points: list[dict[str, float]] = Field(default_factory=list)


class PowerFlowLayoutSaveBody(BaseModel):
    canvas_width: int = 1280
    canvas_height: int = 720
    nodes: list[PowerFlowNodeBody] = Field(default_factory=list)
    junctions: list[PowerFlowJunctionBody] = Field(default_factory=list)
    wires: list[PowerFlowWireBody] = Field(default_factory=list)
