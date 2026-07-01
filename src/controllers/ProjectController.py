from fastapi import Depends

from controllers.BaseController import BaseController
from helpers.config import Settings, get_settings
import os

class ProjectController(BaseController):
    def __init__(self, app_settings: Settings = Depends(get_settings)):
        super().__init__(app_settings=app_settings)

    def get_project_path(self, project_id: str):
        project_dir = os.path.join(self.files_dir, project_id)
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        return project_dir