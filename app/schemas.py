from datetime import datetime

from pydantic import BaseModel, ConfigDict


class BriefingResponse(BaseModel):
    id: int
    status: str
    created_at: datetime
    completed_at: datetime | None

    model_config = ConfigDict(from_attributes=True)