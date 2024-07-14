from fastapi import APIRouter, Depends

from auth.auth import get_current_active_user
from auth.schemas import SUserInDB
from notes.schemas import SNote, SNoteCreate

from notes.repository import NoteRepository

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[SNote])
async def get_notes(user: SUserInDB = Depends(get_current_active_user)):
    note_models = await NoteRepository.get_note_by_user_id(user.id)
    note_schemas = [SNote.model_validate(note_model, from_attributes=True) for note_model in note_models]
    return note_schemas


@router.post("/", response_model=SNote)
async def create_note(note_data: SNoteCreate = Depends(), user: SUserInDB = Depends(get_current_active_user)):
    note_data.user_id = user.id
    await NoteRepository.create_note(note_data)
    return note_data
