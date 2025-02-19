from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import ForeignKey
from sqlalchemy.types import VARCHAR, JSON, UUID

from .base import TableBase

if TYPE_CHECKING:
    from .isbn import Registrant, PublicationDetail

class Publisher(TableBase):
    __tablename__ = 'publishers'

    image: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    links: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    name_ruby: Mapped[str] = mapped_column(VARCHAR(255))

    labels: Mapped[List['Label']] = relationship('Label', back_populates='publisher')
    registrants: Mapped[List['Registrant']] = relationship('Registrant', back_populates='publisher')

class Label(TableBase):
    __tablename__ = 'labels'

    image: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    links: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    name_ruby: Mapped[str] = mapped_column(VARCHAR(255))

    publication_details: Mapped[List['PublicationDetail']] = relationship('PublicationDetail', back_populates='label')
    publisher: Mapped['Publisher'] = relationship('Publisher', back_populates='labels')

    publisher_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('publishers.id'))
