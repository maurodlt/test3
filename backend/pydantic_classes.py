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
    name: str
    country: str
    publication: List[int]  # N:M Relationship
    author: List[int]  # N:M Relationship


class AuthorCreate(BaseModel):
    last_name: str
    name: str
    institution: List[int]  # N:M Relationship
    publication_1: List[int]  # N:M Relationship


class PublicationCreate(BaseModel):
    title: str
    year: int
    institution_1: List[int]  # N:M Relationship
    author_1: List[int]  # N:M Relationship


class ConferenceCreate(PublicationCreate):
    month: str
    organization: str
    address: str
    publisher: str
    booktitle: str
    number: str
    pages: str
    series: str
    note: str
    editor: str


class ProceedingsCreate(PublicationCreate):
    editor: str
    volume: str
    series: str
    organization: str
    month: str
    publisher: str
    address: str
    number: str
    pages: str
    booktitle: str


class BookCreate(PublicationCreate):
    address: str
    publisher: str


class ThesisCreate(PublicationCreate):
    month: str
    note: str
    address: str
    type: str


class OthersCreate(PublicationCreate):
    link: str
    peer_reviewed: bool
    server: str


class JournalCreate(PublicationCreate):
    month: str
    volume: str
    note: str
    pages: str
    journal: str
    number: str


