# import os
# import sys
# from sqlalchemy import Column, ForeignKey, Integer, String
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import relationship
# from sqlalchemy import create_engine

# engine = create_engine('sqlite:///categorylist.db')

# connection = engine.connect()
# result = connection.execute("select username from users")
# for row in result:
#     print("username:", row['username'])
# connection.close()




from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///categorylist.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()



myFirstRestaurant = Categories(name = "Pizza Palace")
session.add(myFirstRestaurant)
sesssion.commit()


cheesepizza = StockItem(name="Cheese Pizza", description = "Made with all natural ingredients and fresh mozzarella", course="Entree", price="$8.99", category=myFirstRestaurant)
session.add(cheesepizza)
session.commit()


firstResult = session.query(Restaurant).first()
firstResult.name

items = session.query(MenuItem).all()
for item in items:
    print item.name

