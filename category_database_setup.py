import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        allItems = session.query(StockItem).filter_by(category_name=self.name)
        stockItems = [r.serialize for r in allItems]
        return {
            'id': self.id,
            'name': self.name,
            'items': stockItems
        }

class StockItem(Base):
    __tablename__ = 'stock_item'

    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    created_by = Column(String(250))
    category_name = Column(Integer, ForeignKey('category.name'))
    category = relationship(Category)

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_by': self.created_by,
            'category_name': self.category_name
        }

class UserTable(Base):
    __tablename__ = 'user_table'

    email = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        allResults = session.query(UserTable).all()
        loggedInUsers = [r.serialize for r in allResults]

        return {
            'loggedInUsers': loggedInUsers
        }


engine = create_engine('sqlite:///categorylist.db')
Base.metadata.create_all(engine)
