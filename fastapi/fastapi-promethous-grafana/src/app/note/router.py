from datetime import datetime
from typing import List

from fastapi import APIRouter, HTTPException, Path

from app.note import crud
from app.note.models import NoteDB, NoteSchema

router = APIRouter()


@router.post("/", response_model=NoteDB, status_code=201)
async def create_note(payloal: NoteSchema):
    note_id = await crud.post(payload=payload)
    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
        "created_date": created_date,
    }
    
    return response_object


@router.get("/{idx}/", response_model=NoteDB)
async def read_note(idx: int = Path(..., gt=0),):
    note = await crud.get(idx=idx)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud.get_all()


@router.put("/{idx}/", response_model=NoteDB)
async def update_note(payload: NoteSchema, idx: int=Path(..., gt=0)):
    note = await crud.get(idx=idx)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    note_id = await crud.put(idx=idx, payload=payload)
    response_object = {
        "id": note_id,
        "title": payload.title,
        "description": payload.description,
        "completed": payload.completed,
    }
    
    return response_object


@router.delete("/{idx}/", response_model=NoteDB)
async def delete_note(idx: int = Path(..., gt=0)):
    note = await crud.get(idx=idx)
    
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    
    await crud.delete(idx=idx)
    
    return note