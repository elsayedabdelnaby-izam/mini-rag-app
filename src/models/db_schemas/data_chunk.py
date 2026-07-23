from pydantic import BaseModel, Field, validator
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id: Optional[ObjectId]
    chunk_text: str = Field(..., min_length=1, description="The chunk text")
    chunk_metadata: dict = Field(..., description="The chunk metadata")
    chunk_order: int = Field(..., description="The chunk order", gt=0)
    chunk_project_id: ObjectId = Field(..., description="The project ID")

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }