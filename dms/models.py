from datetime import datetime
from uuid import UUID

from . import db

from sqlalchemy.orm import Mapped, mapped_column, Relationship
from sqlalchemy import ForeignKey
from typing import List


class User(db.Model):
    """An application user."""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("user_id", primary_key=True)
    name: Mapped[str] = mapped_column("user_name", nullable=False)
    email: Mapped[str] = mapped_column("user_email",
                                       unique=True, nullable=False)
    password: Mapped[str] = mapped_column("user_password", nullable=False)
    documents: Mapped[List["Document"]] = Relationship(back_populates="owner")

    def __repr__(self):
        return f'<User {self.name} ({self.email})>'


class Document(db.Model):
    """A document (not necessarily a text document) which may be an assessment
    submission or the assessment itself."""
    __tablename__ = "document"

    id: Mapped[UUID] = mapped_column("document_id", primary_key=True)
    name: Mapped[str] = mapped_column("document_name", nullable=False)
    mime: Mapped[str] = mapped_column("document_mime", nullable=False)
    uploaded: Mapped[datetime] = mapped_column("document_uploaded",
                                               nullable=False)

    owner_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    owner: Mapped[User] = Relationship(back_populates="documents")

    def __repr__(self):
        return f'<Document {self.name} ({self.mime})>'
