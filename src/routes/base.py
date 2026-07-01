from fastapi import APIRouter, Depends

from helpers.config import Settings, get_settings

router = APIRouter(
    prefix="/api/v1"
)

@router.get("/")
async def welcome(app_settings: Settings = Depends(get_settings)):
    return {
        "message": f"Hello, {app_settings.APP_NAME}! Version: {app_settings.APP_VERSION}"
    }
