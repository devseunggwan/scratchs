from datetime import datetime

from app.db import notes, database
from app.note.models import NoteSchema


async def post(payload: NoteSchema):
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = notes.insert().values(title=payload.title, description=payload.description, completed=payload.completed, created_date=created_date)
    return await database.execute(query=query)


async def get(idx: int):
    query = notes.select().where(idx == notes.c.idx)
    return await database.fetch_one(query=query)


async def get_all():
    query = notes.select()
    return await database.fetch_all(query=query)


async def put(idx: int, payload=NoteSchema):
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = (
        notes.update().where(idx == notes.c.idx).values(title=payload.title, description=payload.description, completed=payload.completed, created_date=created_date).returning(notes.c.id)
    )
    
    return await database.execute(query=query)


async def delete(idx: int):
    query = notes.delete().where(idx == notes.c.idx)
    return await database.execute(query=query)