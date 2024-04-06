from typing import List, Optional
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import Mapped, mapped_column, Relationship
from datetime import datetime
from dms import db


class User(db.Model):
    """An application user."""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("user_id",autoincrement=True, primary_key=True)
    name: Mapped[str] = mapped_column("user_name", nullable=False)
    email: Mapped[str] = mapped_column("user_email", nullable=False)
    password: Mapped[str] = mapped_column("user_password", nullable=False)
    documents: Mapped[List["Document"]] = Relationship(back_populates="owner")
    assessments: Mapped[List["Assessment"]
                        ] = Relationship(back_populates="owner")

    def __repr__(self):
        return '<User %r>' % self.username

    def __init__(self, name: str, password: str, email: str):
        self.name = name
        self.email = email
        self.password = password


submission_author = Table(
    "submission_author",
    db.metadata,
    Column("submission_id", ForeignKey(
        "submission.submission_id"), primary_key=True),
    Column("author_id", ForeignKey("author.author_id"), primary_key=True)
)

submission_attachment = Table(
    "submission_attachment",
    db.metadata,
    Column("submission_id", ForeignKey(
        "submission.submission_id"), primary_key=True),
    Column("document_id", ForeignKey("document.document_id"), primary_key=True)
)


class Document(db.Model):
    """A document (not necessarily a text document) which may be an assessment submission or the assessment itself."""
    __tablename__ = "document"

    id: Mapped[int] = mapped_column("document_id", primary_key=True)
    name: Mapped[str] = mapped_column("document_name")
    mime: Mapped[str] = mapped_column("document_mime")
    uploaded: Mapped[datetime] = mapped_column("document_uploaded")
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    owner: Mapped[User] = Relationship(back_populates="documents")


class Author(db.Model):
    """A submission author."""
    __tablename__ = "author"
    __table_args__ = {"extend_existing": True}

    id: Mapped[int] = mapped_column("author_id", primary_key=True)
    name: Mapped[str] = mapped_column("author_name", nullable=False)
    submissions: Mapped[List["Submission"]] = Relationship(
        secondary=submission_author, back_populates="authors")


class Assessment(db.Model):
    """An assessment task, not to be confused with a submission, which is the deliverable for an assessment."""
    __tablename__ = "assessment"

    id: Mapped[int] = mapped_column("assessment_id", primary_key=True)
    name: Mapped[str] = mapped_column("assessment_name")
    created: Mapped[datetime] = mapped_column("assessment_created")
    modified: Mapped[Optional[datetime]] = mapped_column("assessment_modified")
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    rubric_id: Mapped[int] = mapped_column(ForeignKey("document.document_id"))
    owner: Mapped["User"] = Relationship(back_populates="assessments")
    rubric: Mapped["Document"] = Relationship()
    criteria: Mapped[List["Criterion"]] = Relationship(
        back_populates="assessment")
    submissions: Mapped[List["Submission"]] = Relationship(
        back_populates="assessment")


class Criterion(db.Model):
    __tablename__ = "criterion"

    id: Mapped["int"] = mapped_column("criterion_id", primary_key=True)
    name: Mapped[str] = mapped_column("criterion_name")
    min: Mapped[int] = mapped_column("criterion_min")
    max: Mapped[int] = mapped_column("criterion_max")
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessment.assessment_id"))
    assessment: Mapped["Assessment"] = Relationship(back_populates="criteria")


class Submission(db.Model):
    """A submission. That is, the deliverable for an assessment."""
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column("submission_id", primary_key=True)
    submitted: Mapped[datetime] = mapped_column("submission_submitted")
    modified: Mapped[Optional[datetime]] = mapped_column("submission_modified")
    assessment_id: Mapped[int] = mapped_column(
        ForeignKey("assessment.assessment_id"))
    assessment: Mapped["Assessment"] = Relationship(
        back_populates="submissions")
    authors: Mapped[List["Author"]] = Relationship(
        secondary=submission_author, back_populates="submissions")
    attachments: Mapped[List["Document"]] = Relationship(
        secondary=submission_attachment)


class Result(db.Model):
    __tablename__ = "result"

    submission_id: Mapped[int] = mapped_column(
        ForeignKey("submission.submission_id"), primary_key=True)
    criterion_id: Mapped[int] = mapped_column(
        ForeignKey("criterion.criterion_id"), primary_key=True)
    value: Mapped[int] = mapped_column("result_value")
    marker_id: Mapped[id] = mapped_column(ForeignKey("user.user_id"))
    marked: Mapped[datetime] = mapped_column("result_marked")
    submission: Mapped["Submission"] = Relationship()
    criterion: Mapped["Criterion"] = Relationship()
    marker: Mapped["User"] = Relationship( )
