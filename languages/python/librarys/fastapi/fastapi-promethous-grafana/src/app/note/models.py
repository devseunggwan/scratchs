from datetime import datetime

from pydantic import BaseModel, Field
from pytz import timezone as tz


class NoteSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)
    completed: str = "False"
    created_date: str = datetime.now(tz("Asia/Seoul")).strftime("%Y-%m-%d %H:%M:%S")


class NoteDB(NoteSchema):
    idx: int
