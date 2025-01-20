from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class NoteOrm(Base):
    __tablename__ = 'note'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    content: Mapped[str]

    user_id: Mapped[int] = mapped_column(ForeignKey('user.id'), nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), nullable=False)
    deleted: Mapped[bool] = mapped_column(default=False, nullable=False)

    user: Mapped["UserOrm"] = relationship(back_populates="notes")
