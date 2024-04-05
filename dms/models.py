from . import db

from sqlalchemy.orm import Mapped, mapped_column


class User(db.Model):
    """An application user."""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("user_id", primary_key=True)
    name: Mapped[str] = mapped_column("user_name", nullable=False)
    email: Mapped[str] = mapped_column("user_email",
                                       unique=True, nullable=False)
    password: Mapped[str] = mapped_column("user_password", nullable=False)

    def __repr__(self):
        return f'<User {self.name} ({self.email})>'
