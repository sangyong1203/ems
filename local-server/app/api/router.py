from fastapi import APIRouter

from ..domains.alarm.router import router as alarms_router
from ..domains.auth.router import router as auth_router
from ..domains.auth.user_router import router as users_router
from ..domains.dashboard.router import router as dashboard_router
from ..domains.device.router import router as devices_router
from ..domains.ess.router import router as ess_router
from ..domains.maintenance.router import router as maintenance_router
from ..domains.power_flow.editor_router import router as power_flow_editor_router
from ..domains.power_flow.router import router as power_flow_router
from ..domains.project.router import router as project_router
from ..domains.pv_string.router import router as pv_strings_router
from ..domains.report.router import router as reports_router
from ..domains.simulator.router import router as simulator_router
from ..domains.solar.router import router as solar_router
from ..domains.telemetry.router import router as telemetry_router
from ..domains.trend.router import router as trend_router


api_router = APIRouter()

api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(project_router)
api_router.include_router(dashboard_router)
api_router.include_router(solar_router)
api_router.include_router(ess_router)
api_router.include_router(power_flow_router)
api_router.include_router(power_flow_editor_router)
api_router.include_router(trend_router)
api_router.include_router(devices_router)
api_router.include_router(pv_strings_router)
api_router.include_router(telemetry_router)
api_router.include_router(alarms_router)
api_router.include_router(maintenance_router)
api_router.include_router(reports_router)
api_router.include_router(simulator_router)
