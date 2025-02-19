from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING
import uuid

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import CheckConstraint, ForeignKey, UniqueConstraint
from sqlalchemy.types import CHAR, INTEGER, UUID, VARCHAR

from .base import TableBase

if TYPE_CHECKING:
    from .book import Magazine
    from .publisher import Publisher, Label

class CCode(TableBase):
    __tablename__ = 'c_codes'
    __table_args__ = (
        CheckConstraint("(length(target) == 1) AND (target BETWEEN '0' AND '9')"),
        CheckConstraint("(length(format) == 1) AND (format BETWEEN '0' AND '9')"),
        CheckConstraint("(length(content) == 2) AND (content BETWEEN '00' AND '99')"),
        UniqueConstraint('target', 'format', 'content'),
    )

    target: Mapped[str] = mapped_column(CHAR(1))
    format: Mapped[str] = mapped_column(CHAR(1))
    content: Mapped[str] = mapped_column(CHAR(2))

    jan_publications: Mapped[List['PublicationDetail']] = relationship('PublicationDetail', back_populates='c_code')

class Region(TableBase):
    __tablename__ = 'regions'

    image: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    name: Mapped[str] = mapped_column(VARCHAR(31), unique=True)

    registration_groups: Mapped[List['RegistrationGroup']] = relationship('RegistrationGroup', back_populates='region')

class Prefix(TableBase):
    __tablename__ = 'prefixes'
    __table_args__ = (
        CheckConstraint('length(element) == 3'),
        CheckConstraint("element BETWEEN '000' AND '999'"),
    )

    element: Mapped[str] = mapped_column(CHAR(3), unique=True)

    registration_groups: Mapped[List['RegistrationGroup']] = relationship('RegistrationGroup', back_populates='prefix')

class RegistrationGroup(TableBase):
    __tablename__ = 'registration_groups'
    __table_args__ = (
        CheckConstraint('length(element) BETWEEN 1 AND 7'),
        CheckConstraint("element BETWEEN '0000000' AND '9999999'"),
        UniqueConstraint('element', 'prefix_id'),
    )

    element: Mapped[str] = mapped_column(CHAR(7))

    prefix: Mapped[Optional['Prefix']] = relationship('Prefix', back_populates='registration_groups')
    region: Mapped['Region'] = relationship('Region', back_populates='registration_groups')
    registrants: Mapped[List['Registrant']] = relationship('Registrant', back_populates='registration_group')

    prefix_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('prefixes.id'))
    region_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('regions.id'))

class Registrant(TableBase):
    __tablename__ = 'registrants'
    __table_args__ = (
        CheckConstraint('length(element) BETWEEN 1 AND 7'),
        CheckConstraint("element BETWEEN '0000000' AND '9999999'"),
        UniqueConstraint('element', 'registration_group_id'),
    )

    element: Mapped[str] = mapped_column(CHAR(7))

    registration_group: Mapped['RegistrationGroup'] = relationship('RegistrationGroup', back_populates='registrants')
    publications: Mapped[List['Publication']] = relationship('Publication', back_populates='registrant')
    publisher: Mapped['Publisher'] = relationship('Publisher', back_populates='registrants')

    registration_group_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('registration_groups.id'))
    publisher_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('publishers.id'))

class Publication(TableBase):
    __tablename__ = 'publications'
    __table_args__ = (
        CheckConstraint('length(element) BETWEEN 1 AND 7'),
        CheckConstraint("element BETWEEN '0000000' AND '9999999'"),
        UniqueConstraint('element', 'registrant_id'),
    )

    element: Mapped[str] = mapped_column(CHAR(7))

    jan_publication: Mapped[Optional['PublicationDetail']] = relationship('PublicationDetail', back_populates='publication')
    registrant: Mapped['Registrant'] = relationship('Registrant', back_populates='publications')

    registrant_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('registrants.id'))

class PublicationDetail(TableBase):
    __tablename__ = 'publication_details'
    __table_args__ = (
        CheckConstraint('price >= 0'),
    )

    price: Mapped[int] = mapped_column(INTEGER)

    c_code: Mapped['CCode'] = relationship('CCode', back_populates='publication_details')
    label: Mapped[Optional['Label']] = relationship('Label', back_populates='publication_details')
    magazine: Mapped['Magazine'] = relationship('Magazine', back_populates='publication_detail')
    publication: Mapped['Publication'] = relationship('Publication', back_populates='publication_detail')
    
    c_code_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('c_codes.id'))
    label_id: Mapped[Optional[uuid.UUID]] = mapped_column(UUID(as_uuid=True), ForeignKey('labels.id'))
    magazine_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('magazines.id'), unique=True)
    publication_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey('publications.id'), unique=True)
