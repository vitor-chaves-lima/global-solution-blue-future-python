import datetime
import uuid
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, String, Uuid, event, text
from sqlalchemy.orm import relationship, mapped_column
from sqlalchemy.sql import func

from . import Base


class CompanySegment(Base):
    __tablename__ = "company_segments"

    segment: str = Column(String(100), primary_key=True, default=uuid.uuid4)
   

class Company(Base):
    __tablename__ = "companies"

    id: uuid.UUID = Column(Uuid, primary_key=True, default=uuid.uuid4)
    shortname: str = Column(String(3), nullable=False)
    name: str = Column(String(100), nullable=False)
    segment_name = mapped_column(ForeignKey('company_segments.segment'), nullable=False)

    segment = relationship(CompanySegment)


class State(Base):
    __tablename__ = "states"

    shortname: str = Column(String(2), primary_key=True, default=uuid.uuid4)
    name: str = Column(String(100), nullable=False)


class ItemType(Base):
    __tablename__ = "item_types"

    type: str = Column(String(100),  primary_key=True, default=uuid.uuid4)


class Item(Base):
    __tablename__ = "items"

    token: uuid.UUID = Column(Uuid, primary_key=True)
    company_id = Column(ForeignKey('companies.id'), nullable=False)
    type_name = Column(ForeignKey('item_types.type'), nullable=False)
    state_shortname = Column(ForeignKey('states.shortname'), nullable=False)
    recycled: Boolean = Column(Boolean, nullable=False, default=False)
    created_at: datetime = Column(DateTime(timezone=True), default=func.now())
    updated_at: datetime = Column(DateTime(timezone=True), nullable=True)

    company = relationship("Company")
    type = relationship("ItemType")
    state = relationship("State", primaryjoin="and_(Item.state_shortname==State.shortname)")

@event.listens_for(State.__table__, "after_create")
def initialize_companies_table(target, connection, **_):
    connection.execute(target.insert(), [
    {
        'name': 'São Paulo',
        'shortname': 'sp',
    },
    {
        'name': 'Rio de janeiro',
        'shortname': 'rj',
    },
    {
        'name': 'Bahia',
        'shortname': 'ba'
    },
    {
        'name': 'Minas Gerais',
        'shortname': 'mg'
    },
])
    

@event.listens_for(CompanySegment.__table__, "after_create")
def initialize_companies_table(target, connection, **_):
    connection.execute(target.insert(), [
    {
        'segment': 'industrial',
    },
    {
        'segment': 'health',
    },
    {
        'segment': 'technology',
    },
])
    

@event.listens_for(Company.__table__, "after_create")
def initialize_companies_table(target, connection, **_):
    company_segments = connection.execute(text("SELECT * FROM company_segments")).fetchall()
    connection.execute(target.insert(), [
        {
            'shortname': 'gsl',
            'name': 'Global Solutions Ltd.',
            'segment_name': company_segments[0][0]
        },
        {
            'shortname': 'shs',
            'name': 'Stellar Health Services',
            'segment_name': company_segments[1][0]
        },
        {
            'shortname': 'fvt',
            'name': 'Future Vision Technologies',
            'segment_name': company_segments[2][0]
        }
    ])


@event.listens_for(ItemType.__table__, "after_create")
def initialize_companies_table(target, connection, **_):
    connection.execute(target.insert(), [
        {
            'type': 'plastic_box',
        },
        {
            'type': 'can',
        },
        {
            'type': 'plastic_bottle',
        },
        {
            'type': 'glass_bottle',
        }
    ])