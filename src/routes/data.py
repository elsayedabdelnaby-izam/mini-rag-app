from fastapi import APIRouter, Depends, File, UploadFile, status
from fastapi.responses import JSONResponse
import os
from helpers.config import Settings, get_settings
from controllers import DataController, ProjectController
import aiofiles
from models import ResponseEnum

router = APIRouter(
    prefix="/api/v1/data"
)

@router.post("/upload/{project_id}")
async def upload_data(project_id: str, file: UploadFile = File(...), app_settings: Settings = Depends(get_settings)):
    data_controller = DataController(app_settings=app_settings)
    is_valid, message = data_controller.validate_file(file)
    if not is_valid:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST, content={"message": message})
    
    project_dir_path = ProjectController(app_settings=app_settings).get_project_path(project_id=project_id)
    file_path = data_controller.generate_unique_filename(org_filename=file.filename, project_id=project_id)
    async with aiofiles.open(file_path, "wb") as f:
        while chunk := await file.read(app_settings.FILE_DEFAULT_CHUNK_SIZE):
            await f.write(chunk)
        await file.close()
    return JSONResponse(status_code=status.HTTP_200_OK, content={"message": ResponseEnum.FILE_UPLOAD_SUCCESS.value})