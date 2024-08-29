from importlib.resources import contents
from lib2to3.fixes.fix_input import context

from fastapi import APIRouter, Depends

from auth.auth import get_current_active_user
from auth.schemas import SUser
from notes.schemas import SNote, SNoteCreate, SNoteBase

from notes.repository import NoteRepository

router = APIRouter(prefix="/notes", tags=["notes"])


@router.get("/", response_model=list[SNote])
async def get_notes(user: SUser = Depends(get_current_active_user)):
    note_models = await NoteRepository.get_note_by_user_id(user.id)
    note_schemas: list[SNote] = [SNote.model_validate(note_model, from_attributes=True) for note_model in note_models]
    return note_schemas


@router.post("/", response_model=SNote)
async def create_note(note_data: SNoteBase, user: SUser = Depends(get_current_active_user)):
    note_data: SNoteCreate = SNoteCreate(title=note_data.title, content=note_data.content, user_id=user.id)
    await NoteRepository.create_note(note_data)
    return note_data
