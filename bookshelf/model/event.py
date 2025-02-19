from __future__ import annotations
from datetime import date
from typing import List, Optional, TYPE_CHECKING
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.types import DATE, Integer, UUID, JSON, VARCHAR

from .base import TableBase

if TYPE_CHECKING:
    from .book import Fanzine

class Event(TableBase):
    __tablename__ = 'events'
    __table_args__ = (
        CheckConstraint('date_from <= date_to'),
        CheckConstraint('number >= 0'),
        UniqueConstraint('name', 'number'),
    )

    date_from: Mapped[date] = mapped_column(DATE)
    date_to: Mapped[date] = mapped_column(DATE)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    name_ruby: Mapped[str] = mapped_column(VARCHAR(255))
    number: Mapped[int] = mapped_column(Integer, default=0)

    event_series: Mapped['EventSeries'] = relationship('EventSeries', back_populates='events')
    fanzines: Mapped[List['Fanzine']] = relationship('Fanzine', back_populates='event')

    event_series_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('event_series.id'))

class EventSeries(TableBase):
    __tablename__ = 'event_series'

    image: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    links: Mapped[dict[str, str]] = mapped_column(JSON, default=dict)
    name: Mapped[str] = mapped_column(VARCHAR(255))
    name_ruby: Mapped[str] = mapped_column(VARCHAR(255))

    events: Mapped[List['Event']] = relationship('Event', back_populates='event_series')
