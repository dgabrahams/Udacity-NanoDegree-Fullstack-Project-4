import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from flask import jsonify






# added here
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

# added here
# DBSession = sessionmaker(bind=engine)
# session = DBSession()

class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):

        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        # items = session.query(Category).all()
        allItems = session.query(StockItem).filter_by(category_name=self.name)
        # print items
        # print '***' + self.name + '***'
        # stockItems = {}

        # stockItems = jsonify(items=[r.serialize for r in allItems])
        stockItems = [r.serialize for r in allItems]
        # print stockItems


    # categories = session.query(Category).all()
    # return jsonify(categories=[r.serialize for r in categories])



        for x in allItems:
          # currentItem = {}
          # currentItem.
          print(x.name)

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
    # category_id = Column(Integer, ForeignKey('category.id'))
    category_name = Column(Integer, ForeignKey('category.name'))
    category = relationship(Category)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'category_name': '',
            'category': ''
        }



engine = create_engine('sqlite:///categorylist.db')


Base.metadata.create_all(engine)