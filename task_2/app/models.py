from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID
import uuid

Base = declarative_base()

user_organisation_table = Table('user_organisation', Base.metadata,
    Column('user_id', ForeignKey('users.userId')),
    Column('organisation_id', ForeignKey('organisations.orgId'))
)

class User(Base):
    __tablename__ = "users"
    userId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password= Column(String, nullable=False)
    phone = Column(String)

    organisations = relationship("Organisation", secondary=user_organisation_table, back_populates="users")

class Organisation(Base):
    __tablename__ = "organisations"
    orgId = Column(String, primary_key=True, default=str(uuid.uuid4()))
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
    users = relationship("User", secondary=user_organisation_table, back_populates="organisations")
