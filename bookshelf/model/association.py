from __future__ import annotations
from typing import TYPE_CHECKING
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import Column, ForeignKey, Table
from sqlalchemy.types import UUID

from .base import _TableBase, TableBase

if TYPE_CHECKING:
    from .book import Book
    from .creator import CreatorRole, Creator

class BookCreatorAssociation(_TableBase):
    __tablename__ = 'books_creators'

    book: Mapped['Book'] = relationship('Book', back_populates='creators')
    creator: Mapped['Creator'] = relationship('Creator', back_populates='books')
    creator_role: Mapped['CreatorRole'] = relationship('CreatorRole', back_populates='books')

    book_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('books.id'), primary_key=True)
    creator_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('creators.id'), primary_key=True)
    creator_role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('creator_roles.id'), primary_key=True)

books_genres = Table(
    'books_genres',
    TableBase.metadata,
    Column('book_id', UUID(as_uuid=True), ForeignKey('books.id'), primary_key=True),
    Column('genre_id', UUID(as_uuid=True), ForeignKey('genres.id'), primary_key=True)
)

circles_creators = Table(
    'circles_creators',
    TableBase.metadata,
    Column('circle_id', UUID(as_uuid=True), ForeignKey('circles.id'), primary_key=True),
    Column('creator_id', UUID(as_uuid=True), ForeignKey('creators.id'), primary_key=True)
)

creator_roles_creators = Table(
    'creator_roles_creators',
    TableBase.metadata,
    Column('creator_role_id', UUID(as_uuid=True), ForeignKey('creator_roles.id'), primary_key=True),
    Column('creator_id', UUID(as_uuid=True), ForeignKey('creators.id'), primary_key=True)
)

creators_series = Table(
    'creators_series',
    TableBase.metadata,
    Column('creator_id', UUID(as_uuid=True), ForeignKey('creators.id'), primary_key=True),
    Column('series_id', UUID(as_uuid=True), ForeignKey('series.id'), primary_key=True)
)
