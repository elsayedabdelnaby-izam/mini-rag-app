from pydantic import BaseModel
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    _id: Optional[ObjectId]
    project_id: str = Field(..., min_length=1, description="The project ID")
    

    @validator("project_id", pre=True)
    def validate_project_id(cls, v):
        if not v:
            raise ValueError("Project ID is required")
        if not v.isalnum():
            raise ValueError("Project ID must be alphanumeric")
        return v

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }