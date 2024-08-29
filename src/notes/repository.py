from sqlalchemy import select

from database import new_session
from notes.schemas import SNoteCreate
from notes.models import NoteOrm


class NoteRepository:
    @staticmethod
    async def create_note(note: SNoteCreate):
        async with new_session() as session:
            note_model = NoteOrm(title=note.title, content=note.content, user_id=note.user_id)
            session.add(note_model)
            await session.commit()
            return note_model

    @staticmethod
    async def get_note_by_user_id(user_id: int):
        async with new_session() as session:
            query = select(NoteOrm).where(NoteOrm.user_id == user_id)
            result = await session.execute(query)
            note_models = result.scalars().all()
            return note_models
