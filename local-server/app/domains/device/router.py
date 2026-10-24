from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import DeviceSaveBody
from .service import add_device, get_device_detail, get_device_list, remove_device, save_device


router = APIRouter(prefix="/api/devices", tags=["devices"])  # 이 도메인의 API 경로와 문서 태그


# 장비 종류·상태·검색어를 서비스에 전달하고 목록을 반환합니다.
@router.get("")
def devices(
    deviceType: str = Query(default=""),
    status: str = Query(default=""),
    keyword: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_device_list(db, device_type=deviceType, status=status, keyword=keyword))


# 장비 ID로 상세 조회를 요청하고 공통 성공 응답으로 반환합니다.
@router.get("/{device_id}")
def device_detail(device_id: int, db: Session = Depends(get_db)):
    return ok(get_device_detail(db, device_id))


# 장비와 스트링 연결 등록 본문을 서비스에 전달합니다.
@router.post("")
def create_device(body: DeviceSaveBody, db: Session = Depends(get_db)):
    return ok(add_device(db, body))


# 장비 ID와 수정 본문을 서비스에 전달합니다.
@router.put("/{device_id}")
def update_device(device_id: int, body: DeviceSaveBody, db: Session = Depends(get_db)):
    return ok(save_device(db, device_id, body))


# 참조 검사와 삭제를 서비스에 요청하고 결과를 반환합니다.
@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    return ok(remove_device(db, device_id))
