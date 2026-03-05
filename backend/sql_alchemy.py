import enum
from typing import List, Optional
from sqlalchemy import (
    create_engine, Column, ForeignKey, Table, Text, Boolean, String, Date, 
    Time, DateTime, Float, Integer, Enum
)
from sqlalchemy.orm import (
    column_property, DeclarativeBase, Mapped, mapped_column, relationship
)
from datetime import datetime as dt_datetime, time as dt_time, date as dt_date

class Base(DeclarativeBase):
    pass



# Tables definition for many-to-many relationships
author_institution = Table(
    "author_institution",
    Base.metadata,
    Column("institution", ForeignKey("institution.id"), primary_key=True),
    Column("author", ForeignKey("author.id"), primary_key=True),
)
author_publication = Table(
    "author_publication",
    Base.metadata,
    Column("publication_1", ForeignKey("publication.id"), primary_key=True),
    Column("author_1", ForeignKey("author.id"), primary_key=True),
)
publication_institution = Table(
    "publication_institution",
    Base.metadata,
    Column("institution_1", ForeignKey("institution.id"), primary_key=True),
    Column("publication", ForeignKey("publication.id"), primary_key=True),
)

# Tables definition
class Institution(Base):
    __tablename__ = "institution"
    id: Mapped[int] = mapped_column(primary_key=True)
    country: Mapped[str] = mapped_column(String(100))
    city: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

class Author(Base):
    __tablename__ = "author"
    id: Mapped[int] = mapped_column(primary_key=True)
    last_name: Mapped[str] = mapped_column(String(100))
    name: Mapped[str] = mapped_column(String(100))

class Publication(Base):
    __tablename__ = "publication"
    id: Mapped[int] = mapped_column(primary_key=True)
    year: Mapped[int] = mapped_column(Integer)
    title: Mapped[str] = mapped_column(String(100))
    type_spec: Mapped[str] = mapped_column(String(50))
    __mapper_args__ = {
        "polymorphic_identity": "publication",
        "polymorphic_on": "type_spec",
    }

class Conference(Publication):
    __tablename__ = "conference"
    id: Mapped[int] = mapped_column(ForeignKey("publication.id"), primary_key=True)
    editor: Mapped[str] = mapped_column(String(100))
    month: Mapped[str] = mapped_column(String(100))
    organization: Mapped[str] = mapped_column(String(100))
    booktitle: Mapped[str] = mapped_column(String(100))
    number: Mapped[str] = mapped_column(String(100))
    publisher: Mapped[str] = mapped_column(String(100))
    series: Mapped[str] = mapped_column(String(100))
    note: Mapped[str] = mapped_column(String(100))
    pages: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(100))
    __mapper_args__ = {
        "polymorphic_identity": "conference",
    }

class Proceedings(Publication):
    __tablename__ = "proceedings"
    id: Mapped[int] = mapped_column(ForeignKey("publication.id"), primary_key=True)
    address: Mapped[str] = mapped_column(String(100))
    editor: Mapped[str] = mapped_column(String(100))
    month: Mapped[str] = mapped_column(String(100))
    volume: Mapped[str] = mapped_column(String(100))
    organization: Mapped[str] = mapped_column(String(100))
    number: Mapped[str] = mapped_column(String(100))
    publisher: Mapped[str] = mapped_column(String(100))
    series: Mapped[str] = mapped_column(String(100))
    pages: Mapped[str] = mapped_column(String(100))
    booktitle: Mapped[str] = mapped_column(String(100))
    __mapper_args__ = {
        "polymorphic_identity": "proceedings",
    }

class Book(Publication):
    __tablename__ = "book"
    id: Mapped[int] = mapped_column(ForeignKey("publication.id"), primary_key=True)
    address: Mapped[str] = mapped_column(String(100))
    publisher: Mapped[str] = mapped_column(String(100))
    __mapper_args__ = {
        "polymorphic_identity": "book",
    }

class Thesis(Publication):
    __tablename__ = "thesis"
    id: Mapped[int] = mapped_column(ForeignKey("publication.id"), primary_key=True)
    month: Mapped[str] = mapped_column(String(100))
    address: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(100))
    note: Mapped[str] = mapped_column(String(100))
    __mapper_args__ = {
        "polymorphic_identity": "thesis",
    }

class Others(Publication):
    __tablename__ = "others"
    id: Mapped[int] = mapped_column(ForeignKey("publication.id"), primary_key=True)
    link: Mapped[str] = mapped_column(String(100))
    server: Mapped[str] = mapped_column(String(100))
    peer_reviewed: Mapped[bool] = mapped_column(Boolean)
    __mapper_args__ = {
        "polymorphic_identity": "others",
    }

class Journal(Publication):
    __tablename__ = "journal"
    id: Mapped[int] = mapped_column(ForeignKey("publication.id"), primary_key=True)
    pages: Mapped[str] = mapped_column(String(100))
    month: Mapped[str] = mapped_column(String(100))
    note: Mapped[str] = mapped_column(String(100))
    volume: Mapped[str] = mapped_column(String(100))
    journal: Mapped[str] = mapped_column(String(100))
    number: Mapped[str] = mapped_column(String(100))
    __mapper_args__ = {
        "polymorphic_identity": "journal",
    }


#--- Relationships of the institution table
Institution.author: Mapped[List["Author"]] = relationship("Author", secondary=author_institution, back_populates="institution")
Institution.publication: Mapped[List["Publication"]] = relationship("Publication", secondary=publication_institution, back_populates="institution_1")

#--- Relationships of the author table
Author.institution: Mapped[List["Institution"]] = relationship("Institution", secondary=author_institution, back_populates="author")
Author.publication_1: Mapped[List["Publication"]] = relationship("Publication", secondary=author_publication, back_populates="author_1")

#--- Relationships of the publication table
Publication.institution_1: Mapped[List["Institution"]] = relationship("Institution", secondary=publication_institution, back_populates="publication")
Publication.author_1: Mapped[List["Author"]] = relationship("Author", secondary=author_publication, back_populates="publication_1")

# Database connection
DATABASE_URL = "sqlite:///Class_Diagram.db"  # SQLite connection
engine = create_engine(DATABASE_URL, echo=True)

# Create tables in the database
Base.metadata.create_all(engine, checkfirst=True)