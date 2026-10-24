from pydantic import BaseModel, Field


# 전력 흐름 장비 노드의 배치 저장 형식
class PowerFlowNodeBody(BaseModel):
    client_id: str  # 클라이언트에서 배치 요소를 구분하는 ID
    device_id: int  # 연결 장비 ID
    x: float  # 캔버스 기준 가로 좌표 (px)
    y: float  # 캔버스 기준 세로 좌표 (px)
    width: float = 190  # 노드 너비 (px)
    height: float = 104  # 노드 높이 (px)


# 전력 흐름 분기점의 배치 저장 형식
class PowerFlowJunctionBody(BaseModel):
    client_id: str  # 클라이언트에서 배치 요소를 구분하는 ID
    x: float  # 캔버스 기준 가로 좌표 (px)
    y: float  # 캔버스 기준 세로 좌표 (px)


# 전력 흐름 배선과 경유점 저장 형식
class PowerFlowWireBody(BaseModel):
    client_id: str  # 클라이언트에서 배치 요소를 구분하는 ID
    source_type: str  # 출발 요소 종류 (NODE 또는 JUNCTION)
    source_ref: str  # 출발 요소의 client_id
    source_anchor: str  # 출발 요소의 연결 위치
    target_type: str  # 도착 요소 종류 (NODE 또는 JUNCTION)
    target_ref: str  # 도착 요소의 client_id
    target_anchor: str  # 도착 요소의 연결 위치
    direction: str = "FORWARD"  # 배선의 흐름 방향
    metric_key: str | None = None  # 계측 지표 키
    is_enabled: bool = True  # 배선 활성 여부
    route_points: list[dict[str, float]] = Field(default_factory=list)  # 배선 경유점의 x·y 좌표 목록 (px)


# 기본 전력 흐름 배치 전체 교체 요청
class PowerFlowLayoutSaveBody(BaseModel):
    canvas_width: int = 1280  # 캔버스 너비 (px)
    canvas_height: int = 720  # 캔버스 높이 (px)
    nodes: list[PowerFlowNodeBody] = Field(default_factory=list)  # 배치할 장비 노드 목록
    junctions: list[PowerFlowJunctionBody] = Field(default_factory=list)  # 배치할 분기점 목록
    wires: list[PowerFlowWireBody] = Field(default_factory=list)  # 배치할 배선 목록
