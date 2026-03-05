from datetime import datetime, date, time
from typing import Any, List, Optional, Union, Set
from enum import Enum
from pydantic import BaseModel, field_validator


############################################
# Enumerations are defined here
############################################

############################################
# Classes are defined here
############################################
class InstitutionCreate(BaseModel):
    city: str
    country: str
    name: str
    author: List[int]  # N:M Relationship
    publication: List[int]  # N:M Relationship


class AuthorCreate(BaseModel):
    last_name: str
    name: str
    institution: List[int]  # N:M Relationship
    publication_1: List[int]  # N:M Relationship


class PublicationCreate(BaseModel):
    title: str
    year: int
    author_1: List[int]  # N:M Relationship
    institution_1: List[int]  # N:M Relationship


class ConferenceCreate(PublicationCreate):
    booktitle: str
    organization: str
    pages: str
    number: str
    note: str
    series: str
    address: str
    month: str
    publisher: str
    editor: str


class ProceedingsCreate(PublicationCreate):
    month: str
    volume: str
    booktitle: str
    publisher: str
    address: str
    series: str
    organization: str
    number: str
    pages: str
    editor: str


class BookCreate(PublicationCreate):
    publisher: str
    address: str


class ThesisCreate(PublicationCreate):
    address: str
    note: str
    month: str
    type: str


class OthersCreate(PublicationCreate):
    link: str
    server: str
    peer_reviewed: bool


class JournalCreate(PublicationCreate):
    month: str
    journal: str
    volume: str
    pages: str
    note: str
    number: str


