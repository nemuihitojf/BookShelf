from __future__ import annotations
from datetime import date
from typing import List, Optional, TYPE_CHECKING
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.types import DATE, FLOAT, INTEGER, JSON, UUID, VARCHAR

from .base import TableBase

if TYPE_CHECKING:
    from .association import BookCreatorAssociation
    from .creator import Creator, Circle
    from .event import Event
    from .isbn import PublicationDetail

class Format(TableBase):
    __tablename__ = 'formats'
    __table_args__ = (
        CheckConstraint('length > 0'),
        CheckConstraint('width > 0'),
        UniqueConstraint('length', 'name', 'width'),
    )

    length: Mapped[int] = mapped_column(INTEGER)
    name: Mapped[str] = mapped_column(VARCHAR(31))
    width: Mapped[int] = mapped_column(INTEGER)

    books: Mapped[List['Book']] = relationship('Book', back_populates='format')

class Genre(TableBase):
    __tablename__ = 'genres'
    __table_args__ = (
        CheckConstraint('depth >= 0'),
    )

    name: Mapped[str] = mapped_column(VARCHAR(63))
    depth: Mapped[int] = mapped_column(INTEGER)

    books: Mapped[List['Book']] = relationship('Book', secondary='books_genres', back_populates='genres')
    children: Mapped[List['Genre']] = relationship('Genre', back_populates='parent')
    parent: Mapped[Optional['Genre']] = relationship('Genre', back_populates='children')

    parent_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('genres.id'))

class Book(TableBase):
    __tablename__ = 'books'
    __table_args__ = (
        CheckConstraint('length > 0'),
        CheckConstraint('(fanzine_id IS NOT NULL AND magazine_id IS NULL) OR (fanzine_id IS NULL AND magazine_id IS NOT NULL)'),
    )

    links: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    image: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    length: Mapped[int] = mapped_column(INTEGER)
    release_date: Mapped[date] = mapped_column(DATE)
    subtitle: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    subtitle_ruby: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    title: Mapped[str] = mapped_column(VARCHAR(255))
    title_ruby: Mapped[str] = mapped_column(VARCHAR(255))
    volume: Mapped[Optional[float]] = mapped_column(FLOAT)

    creators: Mapped[List['BookCreatorAssociation']] = relationship('BookCreatorAssociation', back_populates='book')
    fanzine: Mapped[Optional['Fanzine']] = relationship('Fanzine', back_populates='books')
    format: Mapped['Format'] = relationship('Format', back_populates='books')
    genres: Mapped[List['Genre']] = relationship('Genre', secondary='books_genres', back_populates='books')
    magazine: Mapped[Optional['Magazine']] = relationship('Magazine', back_populates='books')
    series: Mapped[Optional['Series']] = relationship('Series', back_populates='books')

    fanzine_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('fanzines.id'), unique=True)
    format_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('formats.id'))
    magazine_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('magazines.id'), unique=True)
    series_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('series.id'))

class Fanzine(TableBase):
    __tablename__ = 'fanzines'

    book: Mapped['Book'] = relationship('Book', back_populates='fanzine')
    circle: Mapped[Optional['Circle']] = relationship('Circle', back_populates='fanzines')
    event: Mapped[Optional['Event']] = relationship('Event', back_populates='fanzines')

    circle_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('circles.id'))
    event_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('events.id'))

class Magazine(TableBase):
    __tablename__ = 'magazines'

    book: Mapped['Book'] = relationship('Book', back_populates='magazine')
    publication_details: Mapped[List['PublicationDetail']] = relationship('PublicationDetail', back_populates='label')

class Series(TableBase):
    __tablename__ = 'series'

    links: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    title: Mapped[str] = mapped_column(VARCHAR(255))
    title_ruby: Mapped[str] = mapped_column(VARCHAR(255))

    books: Mapped[List['Book']] = relationship('Book', back_populates='series')

    creators: Mapped[List['Creator']] = relationship('Creator', secondary='creators_series', back_populates='series')
