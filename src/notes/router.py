from fastapi import APIRouter, Depends, status, HTTPException, Path

from auth.auth import get_current_active_user
from auth.schemas import SUserInDB
from notes.schemas import SNoteCreate, SNoteInDB, SNotePatch

from notes.repository import NoteRepository
from pagination import SPagination, get_pagination

router = APIRouter(prefix="/notes", tags=["notes"])

credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="У пользователя недостаточно прав для совершения действия"
)


@router.get("/", response_model=list[SNoteInDB], status_code=status.HTTP_200_OK)
async def get_notes(
        pagination: SPagination = Depends(get_pagination),
        user: SUserInDB = Depends(get_current_active_user)
) -> list[SNoteInDB]:
    note_models = await NoteRepository.get_notes_by_user_id(user.id, pagination)
    note_schemas: list[SNoteInDB] = [
        SNoteInDB.model_validate(note_model, from_attributes=True)
        for note_model in note_models
    ]
    return note_schemas


@router.post("/", response_model=SNoteInDB, status_code=status.HTTP_201_CREATED)
async def create_note(
        note_data: SNoteCreate,
        user: SUserInDB = Depends(get_current_active_user)
) -> SNoteInDB:
    note_model = await NoteRepository.create_note(user.id, note_data)
    return SNoteInDB.model_validate(note_model, from_attributes=True)


@router.put("/{note_id}", response_model=SNoteInDB, status_code=status.HTTP_200_OK)
async def update_note(
        note_data: SNoteCreate,
        note_id: int = Path(),
        user: SUserInDB = Depends(get_current_active_user),
) -> SNoteInDB:
    if not NoteRepository.check_note_creator(note_id, user.id):
        raise credentials_exception
    note_model = await NoteRepository.update_note(note_id, note_data)
    return SNoteInDB.model_validate(note_model, from_attributes=True)


@router.patch("/{note_id}", response_model=SNoteInDB, status_code=status.HTTP_200_OK)
async def patch_note(
        note_data: SNotePatch,
        note_id: int = Path(),
        user: SUserInDB = Depends(get_current_active_user),
) -> SNoteInDB:
    if not NoteRepository.check_note_creator(note_id, user.id):
        raise credentials_exception
    note_model = await NoteRepository.patch_note(note_id, note_data)
    return SNoteInDB.model_validate(note_model, from_attributes=True)


@router.delete("/", response_model=None, status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(note_id: int, user: SUserInDB = Depends(get_current_active_user)) -> None:
    if not NoteRepository.check_note_creator(note_id, user.id):
        raise credentials_exception
    await NoteRepository.delete_note(note_id)
