"""Model for dogs."""
from enum import Enum
from uuid import uuid4, UUID
from sqlalchemy import LargeBinary
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.dialects.postgresql import ENUM


class ColorEnum(Enum):
    """Enum for color."""

    BLACK = 'black'
    WHITE = 'white'
    BROWN = 'brown'
    RED = 'red'


class BreedEnum(Enum):
    """Enum for breed."""

    LABRADOR = 'labrador retriever'
    PUG = 'pug'
    DOBERMAN = 'doberman'
    GERMAN_SHEPHERD = 'german shepherd'


class Base(DeclarativeBase):
    """Base class for declarative models."""

    pass


class IDMixin:
    """Mixin class for adding an ID field to SQLAlchemy models."""

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)


class Dog(IDMixin, Base):
    """A dog in a database."""

    __tablename__ = 'dogs'
    color: Mapped[ENUM] = mapped_column(ENUM(ColorEnum))
    breed: Mapped[ENUM] = mapped_column(ENUM(BreedEnum))
    image = mapped_column(LargeBinary)
