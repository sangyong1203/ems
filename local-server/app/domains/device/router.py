from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import DeviceSaveBody
from .service import add_device, get_device_detail, get_device_list, remove_device, save_device


router = APIRouter(prefix="/api/devices", tags=["devices"])


@router.get("")
def devices(
    deviceType: str = Query(default=""),
    status: str = Query(default=""),
    keyword: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(get_device_list(db, device_type=deviceType, status=status, keyword=keyword))


@router.get("/{device_id}")
def device_detail(device_id: int, db: Session = Depends(get_db)):
    return ok(get_device_detail(db, device_id))


@router.post("")
def create_device(body: DeviceSaveBody, db: Session = Depends(get_db)):
    return ok(add_device(db, body))


@router.put("/{device_id}")
def update_device(device_id: int, body: DeviceSaveBody, db: Session = Depends(get_db)):
    return ok(save_device(db, device_id, body))


@router.delete("/{device_id}")
def delete_device(device_id: int, db: Session = Depends(get_db)):
    return ok(remove_device(db, device_id))
