import uuid
from database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy import Column, ForeignKey, String, Boolean, Integer, Date, DateTime, func


class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), index=True, nullable=False, default=uuid.uuid4, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    address = Column(String)
    phone_number = Column(String)

    items = relationship('Item', back_populates='owner')

    def __repr__(self):
        return f'{User.id} -> {User.email}'


class Item(Base):
    __tablename__ = 'items'

    id = Column(UUID(as_uuid=True), index=True, nullable=False, default=uuid.uuid4, unique=True, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String)
    date_created = Column(DateTime, default=func.now())
    owner_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))

    owner = relationship('User', back_populates='items')

    def __repr__(self):
        return f'{Item.id} -> {Item.name}'


