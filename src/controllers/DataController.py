from fastapi import Depends
from controllers.BaseController import BaseController
from fastapi import UploadFile
from helpers.config import Settings, get_settings
from models import ResponseEnum
from .ProjectController import ProjectController
import re
import os


class DataController(BaseController):
    def __init__(self, app_settings: Settings = Depends(get_settings)):
        super().__init__(app_settings=app_settings)
        self.size_scale = 1024 * 1024
    
    def validate_file(self, file: UploadFile):
        if file.content_type not in self.app_settings.FILE_ALLOWED_TYPES:
            return False, ResponseEnum.FILE_TYPE_NOT_SUPPORTED.value
        if file.size > self.app_settings.FILE_MAX_SIZE * self.size_scale:
            return False, ResponseEnum.FILE_SIZE_EXCEEDED.value
        return True, ResponseEnum.FILE_VALIDATE_SUCCESS.value

    def generate_unique_filepath(self, org_filename: str, project_id: str):
        random_filename = self.generate_random_string()
        project_path = ProjectController(app_settings=self.app_settings).get_project_path(project_id=project_id)
        clean_filename = self.get_clean_filename(org_filename)
        extension = org_filename.rsplit(".", 1)[-1] if "." in org_filename else ""
        stored_filename = (
            f"{random_filename}_{clean_filename}.{extension}"
            if extension
            else f"{random_filename}_{clean_filename}"
        )
        new_file_path = os.path.join(project_path, stored_filename)
        while os.path.exists(new_file_path):
            random_filename = self.generate_random_string()
            stored_filename = (
                f"{random_filename}_{clean_filename}.{extension}"
                if extension
                else f"{random_filename}_{clean_filename}"
            )
            new_file_path = os.path.join(project_path, stored_filename)
        return new_file_path, stored_filename

    def get_clean_filename(self, filename: str):
        basename = filename.rsplit(".", 1)[0] if "." in filename else filename
        clean_filename = re.sub(r"[^\w.]", "", basename)
        return clean_filename.replace(" ", "_")
