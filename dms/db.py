from typing import List, Optional
from sqlalchemy import ForeignKey, Column, Table
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Relationship
from datetime import datetime


class Base(DeclarativeBase):
    """Database base class"""


submission_author = Table(
    "submission_author", Base.metadata,
    Column("submission_id", ForeignKey("submission.submission_id"), primary_key=True),
    Column("author_id", ForeignKey("author.author_id"), primary_key=True)
)

submission_attachment = Table(
    "submission_attachment", Base.metadata,
    Column("submission_id", ForeignKey("submission.submission_id"), primary_key=True),
    Column("attachment_id", ForeignKey("document.document_id"), primary_key=True)
)


class User(Base):
    """An application user."""
    __tablename__ = "user"

    id: Mapped[int] = mapped_column("user_id", primary_key=True)
    name: Mapped[str] = mapped_column("user_name", nullable=False)
    email: Mapped[str] = mapped_column("user_email", unique=True, nullable=False)
    password: Mapped[str] = mapped_column("user_password", nullable=False)
    documents: Mapped[List["Document"]] = Relationship(back_populates="owner")
    assessments: Mapped[List["Assessment"]] = Relationship(back_populates="owner")


class Author(Base):
    """A submission author."""
    __tablename__ = "author"

    id: Mapped[int] = mapped_column("author_id", primary_key=True)
    name: Mapped[str] = mapped_column("author_name", nullable=False)
    submissions: Mapped[List["Submission"]] = Relationship(secondary=submission_author, back_populates="authors")


class Document(Base):
    """A document (not necessarily a text document) which may be an assessment submission or the assessment itself."""
    __tablename__ = "document"

    id: Mapped[int] = mapped_column("document_id", primary_key=True)
    name: Mapped[str] = mapped_column("document_name")
    mime: Mapped[str] = mapped_column("document_mime")
    uploaded: Mapped[datetime] = mapped_column("document_uploaded")
    owner_id: Mapped[int] = mapped_column(ForeignKey("user.user_id"))
    owner: Mapped[User] = Relationship(back_populates="documents")


class Assessment(Base):
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
    criteria: Mapped[List["Criterion"]] = Relationship(back_populates="assessment")
    submissions: Mapped[List["Submission"]] = Relationship(back_populates="assessment")


class Criterion(Base):
    __tablename__ = "criterion"

    id: Mapped["int"] = mapped_column("criterion_id", primary_key=True)
    name: Mapped[str] = mapped_column("criterion_name")
    min: Mapped[int] = mapped_column("criterion_min")
    max: Mapped[int] = mapped_column("criterion_max")
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessment.assessment_id"))
    assessment: Mapped["Assessment"] = Relationship(back_populates="criteria")


class Submission(Base):
    """A submission. That is, the deliverable for an assessment."""
    __tablename__ = "submission"

    id: Mapped[int] = mapped_column("submission_id", primary_key=True)
    submitted: Mapped[datetime] = mapped_column("submission_submitted")
    modified: Mapped[Optional[datetime]] = mapped_column("submission_modified")
    assessment_id: Mapped[int] = mapped_column(ForeignKey("assessment.assessment_id"))
    assessment: Mapped["Assessment"] = Relationship(back_populates="submissions")
    authors: Mapped[List["Author"]] = Relationship(secondary=submission_author, back_populates="submissions")
    attachments: Mapped[List["Document"]] = Relationship(secondary=submission_attachment)




class Result(Base):
    __tablename__ = "result"

    submission_id: Mapped[int] = mapped_column(ForeignKey("submission.submission_id"), primary_key=True)
    criterion_id: Mapped[int] = mapped_column(ForeignKey("criterion.criterion_id"), primary_key=True)
    value: Mapped[int] = mapped_column("result_value")
    marker_id: Mapped[id] = mapped_column(ForeignKey("user.user_id"))
    marked: Mapped[datetime] = mapped_column("result_marked")
    submission: Mapped["Submission"] = Relationship()
    criterion: Mapped["Criterion"] = Relationship()
    marker: Mapped["User"] = Relationship()


if __name__ == "__main__":
    from sqlalchemy import create_engine
    from sqlalchemy.orm import Session
    engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
    # with Session(engine) as session:
    Base.metadata.create_all(engine)
    user1 = User(name="User 1", email="user1@example.com", password="password")
    author1 = Author(name="Author 1")
    author2 = Author(name="Author 2")
    document1 = Document(name="Document 1", mime="text/text", uploaded=datetime.now(), owner=user1)
    document2 = Document(name="Document 2", mime="text/text", uploaded=datetime.now(), owner=user1)
    document3 = Document(name="Document 3", mime="text/text", uploaded=datetime.now(), owner=user1)
    assessment1 = Assessment(name="Assessment 1", created=datetime.now(), owner=user1, rubric=document1)
    criterion1 = Criterion(name="Spelling", min=0, max=3)
    criterion2 = Criterion(name="Grammar", min=0, max=3)
    assessment1.criteria.extend((criterion1, criterion2))
    submission1 = Submission(assessment=assessment1, submitted=datetime.now(), authors=[author1, author2], attachments=[document2, document3])

    with Session(engine) as session:
        session.add(user1)
        session.add(author1)
        session.commit()