""" Module for creating ORM. """
import sqlalchemy as db

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base

from .configs import POSTGRES_USER, POSTGRES_DB, POSTGRES_PASSWORD

engine_config = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@postgres:5432/{POSTGRES_DB}'
engine = create_engine(engine_config)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


class UserReceipt(Base):
    __tablename__ = 'user_receipts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    environment = db.Column(db.String(20), nullable=False)
    is_retryable = db.Column(db.Boolean, nullable=False)
    latest_receipt = db.Column(db.JSON, nullable=False)
    latest_receipt_info = db.Column(db.JSON, nullable=False)
    pending_renewal_info = db.Column(db.JSON, nullable=False)
    receipt = db.Column(db.JSON, nullable=False)
    status = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'{self.user_id} - {self.receipt_data} - {self.status}'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(Base):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    user_data = relationship('UserReceipt', backref='user', lazy=True)

    def __repr__(self):
        return f'{self.id} - {self.name} - {self.email}'

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
