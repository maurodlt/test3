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
    name: str
    city: str
    country: str
    author: List[int]  # N:M Relationship
    publication: List[int]  # N:M Relationship


class AuthorCreate(BaseModel):
    name: str
    last_name: str
    institution: List[int]  # N:M Relationship
    publication_1: List[int]  # N:M Relationship


class PublicationCreate(BaseModel):
    title: str
    year: int
    author_1: List[int]  # N:M Relationship
    institution_1: List[int]  # N:M Relationship


class ConferenceCreate(PublicationCreate):
    address: str
    series: str
    month: str
    pages: str
    publisher: str
    booktitle: str
    editor: str
    number: str
    note: str
    organization: str


class ProceedingsCreate(PublicationCreate):
    month: str
    volume: str
    booktitle: str
    publisher: str
    organization: str
    editor: str
    address: str
    series: str
    pages: str
    number: str


class BookCreate(PublicationCreate):
    address: str
    publisher: str


class ThesisCreate(PublicationCreate):
    address: str
    type: str
    month: str
    note: str


class OthersCreate(PublicationCreate):
    peer_reviewed: bool
    server: str
    link: str


class JournalCreate(PublicationCreate):
    number: str
    journal: str
    note: str
    pages: str
    month: str
    volume: str


