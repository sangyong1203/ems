from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .schemas import MaintenanceSaveBody
from .service import (
    add_maintenance,
    get_maintenance_detail,
    get_maintenance_list,
    remove_maintenance,
    save_maintenance,
)


router = APIRouter(prefix="/api/maintenance", tags=["maintenance"])


@router.get("")
def maintenance(
    keyword: str = Query(default=""),
    deviceId: int | None = Query(default=None),
    maintenanceType: str = Query(default=""),
    status: str = Query(default=""),
    dateFrom: str = Query(default=""),
    dateTo: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(
        get_maintenance_list(
            db,
            keyword=keyword,
            device_id=deviceId,
            maintenance_type=maintenanceType,
            status=status,
            date_from=dateFrom,
            date_to=dateTo,
        )
    )


@router.get("/{maintenance_id}")
def maintenance_detail(maintenance_id: int, db: Session = Depends(get_db)):
    return ok(get_maintenance_detail(db, maintenance_id))


@router.post("")
def create_maintenance(body: MaintenanceSaveBody, db: Session = Depends(get_db)):
    return ok(add_maintenance(db, body))


@router.put("/{maintenance_id}")
def update_maintenance(maintenance_id: int, body: MaintenanceSaveBody, db: Session = Depends(get_db)):
    return ok(save_maintenance(db, maintenance_id, body))


@router.delete("/{maintenance_id}")
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    return ok(remove_maintenance(db, maintenance_id))
