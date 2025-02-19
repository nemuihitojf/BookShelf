from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import VARCHAR, JSON

from .base import TableBase

if TYPE_CHECKING:
    from .association import BookCreatorAssociation
    from .book import Fanzine, Series

class CreatorRole(TableBase):
    __tablename__ = 'creator_roles'

    name: Mapped[str] = mapped_column(VARCHAR(31), unique=True)

    creators: Mapped[List['Creator']] = relationship('Creator', secondary='creator_roles_creators', back_populates='creator_roles')

class Creator(TableBase):
    __tablename__ = 'creators'

    image: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    links: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    name_ruby: Mapped[str] = mapped_column(VARCHAR(255))

    books: Mapped[List['BookCreatorAssociation']] = relationship('BookCreatorAssociation', back_populates='creator')
    circles: Mapped[List['Circle']] = relationship('Circle', secondary='circles_creators', back_populates='creators')
    creator_roles: Mapped[List['CreatorRole']] = relationship('CreatorRole', secondary='creator_roles_creators', back_populates='creators')
    series: Mapped[List['Series']] = relationship('Series', secondary='creators_series', back_populates='creators')

class Circle(TableBase):
    __tablename__ = 'circles'

    image: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    links: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    name_ruby: Mapped[str] = mapped_column(VARCHAR(255))

    creators: Mapped[List['Creator']] = relationship('Creator', secondary='circles_creators', back_populates='circles')
    fanzines: Mapped[List['Fanzine']] = relationship('Fanzine', back_populates='circle')
