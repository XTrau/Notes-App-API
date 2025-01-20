from typing import Sequence

from sqlalchemy import select, and_

from database import new_session
from notes.schemas import SNoteCreate, SNotePatch
from notes.models import NoteOrm
from pagination import SPagination


class NoteRepository:
    @staticmethod
    async def create_note(user_id: int, note: SNoteCreate) -> NoteOrm:
        async with new_session() as session:
            note_model = NoteOrm(title=note.title, content=note.content, user_id=user_id)
            session.add(note_model)
            await session.commit()
            return note_model

    @staticmethod
    async def get_notes_by_user_id(user_id: int, pagination: SPagination) -> Sequence[NoteOrm]:
        async with new_session() as session:
            query = (
                select(NoteOrm)
                .where(and_(NoteOrm.user_id == user_id, NoteOrm.deleted == False))
                .offset(pagination.page * pagination.count)
                .limit(pagination.count)
            )
            result = await session.execute(query)
            note_models = result.scalars().all()
            return note_models

    @staticmethod
    async def check_note_creator(note_id: int, user_id: int) -> bool:
        async with new_session() as session:
            note_model = await session.get(NoteOrm, note_id)
            return user_id == note_model.user_id

    @staticmethod
    async def update_note(note_id: int, note: SNoteCreate) -> NoteOrm:
        async with new_session() as session:
            note_model = await session.get(NoteOrm, note_id)
            note_model.title = note.title
            note_model.content = note.content
            await session.commit()
            return note_model

    @staticmethod
    async def patch_note(note_id: int, note: SNotePatch) -> NoteOrm:
        async with new_session() as session:
            note_model = await session.get(NoteOrm, note_id)
            if note.title is not None:
                note_model.title = note.title
            if note.content is not None:
                note_model.content = note.content
            await session.commit()
            return note_model

    @staticmethod
    async def delete_note(note_id: int) -> None:
        async with new_session() as session:
            note_model = await session.get(NoteOrm, note_id)
            note_model.deleted = True
            await session.commit()
