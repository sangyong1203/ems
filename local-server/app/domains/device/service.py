from fastapi import HTTPException
from sqlalchemy.orm import Session

from .repository import create_device, delete_device, device_delete_blockers, get_device, list_devices, update_device
from .schemas import DeviceOut, DeviceSaveBody
from ..pv_string.repository import list_inverter_links


# 조건에 맞는 장비에 스트링 연결 정보를 포함하여 목록과 건수를 반환합니다.
def get_device_list(db: Session, device_type: str = "", status: str = "", keyword: str = "") -> dict:
    items = list_devices(db, device_type=device_type, status=status, keyword=keyword)
    return {"list": [_device_out(item, db) for item in items], "totalCount": len(items)}


# 장비 상세를 반환하며 대상이 없으면 404 오류를 발생시킵니다.
def get_device_detail(db: Session, device_id: int) -> dict:
    device = get_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return _device_out(device, db)


# 요청에서 스트링 연결을 분리하여 장비와 함께 저장하고 상세를 반환합니다.
def add_device(db: Session, body: DeviceSaveBody) -> dict:
    payload = body.model_dump()
    pv_string_links = payload.pop("pv_string_links", [])
    device = create_device(db, payload, pv_string_links=pv_string_links)
    return _device_out(device, db)


# 요청에서 스트링 연결을 분리하여 수정하며 대상이 없으면 404 오류를 발생시킵니다.
def save_device(db: Session, device_id: int, body: DeviceSaveBody) -> dict:
    payload = body.model_dump()
    pv_string_links = payload.pop("pv_string_links", [])
    device = update_device(db, device_id, payload, pv_string_links=pv_string_links)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    return _device_out(device, db)


# 장비가 없으면 404, 다른 데이터에서 참조하면 409 오류를 발생시키고 나머지는 삭제합니다.
def remove_device(db: Session, device_id: int) -> dict:
    device = get_device(db, device_id)
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    blockers = device_delete_blockers(db, device_id)
    if blockers:
        raise HTTPException(status_code=409, detail=f"Device is referenced by: {', '.join(blockers)}")
    delete_device(db, device_id)
    return {"deleted": True}


# 장비를 응답으로 변환하며 인버터에만 스트링 연결 목록을 포함합니다.
def _device_out(device, db: Session) -> dict:
    data = DeviceOut.model_validate(device).model_dump()
    data["pv_string_links"] = list_inverter_links(db, device.id) if device.device_type == "INVERTER" else []
    return data
