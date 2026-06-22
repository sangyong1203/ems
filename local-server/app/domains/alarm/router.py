from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ...core.database import get_db
from ...core.responses import ok
from .service import (
    ack_alarm,
    add_alarm_maintenance,
    complete_alarm,
    get_alarm_detail,
    get_alarm_list,
)


router = APIRouter(prefix="/api/alarms", tags=["alarms"])


@router.get("")
def alarms(
    keyword: str = Query(default=""),
    deviceId: int | None = Query(default=None),
    severity: str = Query(default=""),
    alarmType: str = Query(default=""),
    status: str = Query(default=""),
    dateFrom: str = Query(default=""),
    dateTo: str = Query(default=""),
    db: Session = Depends(get_db),
):
    return ok(
        get_alarm_list(
            db,
            keyword=keyword,
            device_id=deviceId,
            severity=severity,
            alarm_type=alarmType,
            status=status,
            date_from=dateFrom,
            date_to=dateTo,
        )
    )


@router.get("/{alarm_id}")
def alarm_detail(alarm_id: int, db: Session = Depends(get_db)):
    return ok(get_alarm_detail(db, alarm_id))


@router.put("/{alarm_id}/ack")
def acknowledge(alarm_id: int, db: Session = Depends(get_db)):
    return ok(ack_alarm(db, alarm_id))


@router.put("/{alarm_id}/resolve")
def resolve(alarm_id: int, db: Session = Depends(get_db)):
    return ok(complete_alarm(db, alarm_id))


@router.post("/{alarm_id}/maintenance")
def create_maintenance_from_alarm(alarm_id: int, db: Session = Depends(get_db)):
    return ok(add_alarm_maintenance(db, alarm_id))
