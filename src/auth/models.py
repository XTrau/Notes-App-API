from sqlalchemy.orm import mapped_column, Mapped, relationship

from database import Base


class UserOrm(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]

    is_verified: Mapped[bool] = mapped_column(default=False)
    disabled: Mapped[bool] = mapped_column(default=False)

    notes: Mapped[list["NoteOrm"]] = relationship(back_populates="user")
