from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Database base class"""


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("user_id", primary_key=True)
    name: Mapped[str] = mapped_column("user_name", nullable=False)
    email: Mapped[str] = mapped_column("user_email", nullable=False)
    password: Mapped[str] = mapped_column("user_password", nullable=False)

