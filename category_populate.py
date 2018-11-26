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


# from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from category_database_setup import Base, Category, StockItem

engine = create_engine('sqlite:///categorylist.db')
Base.metadata.bind=engine
DBSession = sessionmaker(bind = engine)
session = DBSession()




basketball = Category(name = "Basketball")
session.add(basketball)
session.commit()


baseball = Category(name = "Baseball")
session.add(baseball)
session.commit()

bat = StockItem(name="Bat", description = "Simply Amazing", category=baseball)
session.add(bat)
session.commit()




frisbee = Category(name = "Frisbee")
session.add(frisbee)
session.commit()

frisbee_item = StockItem(name="Frisbee", description = "Simply Amazing", category=frisbee)
session.add(frisbee_item)
session.commit()




soccer = Category(name = "Soccer")
session.add(soccer)
session.commit()

shinguards = StockItem(name="Shinguards", description = "Simply Amazing", category=soccer)
session.add(shinguards)

twoshinguards = StockItem(name="Two Shinguards", description = "Simply Amazing", category=soccer)
session.add(twoshinguards)

jersey = StockItem(name="Jersey", description = "Simply Amazing", category=soccer)
session.add(jersey)

cleats = StockItem(name="Soccer Cleats", description = "Simply Amazing", category=soccer)
session.add(jersey)
session.commit()







snowboarding = Category(name = "Snowboarding")
session.add(snowboarding)
session.commit()

snowboard = StockItem(name="Snowboard", description = "Simply Amazing", category=snowboarding)
session.add(snowboard)

goggles = StockItem(name="Goggles", description = "Simply Amazing", category=snowboarding)
session.add(goggles)
session.commit()





rockclimbing = Category(name = "Rock Climbing")
session.add(rockclimbing)
session.commit()



foosball = Category(name = "Foosball")
session.add(foosball)
session.commit()






skating = Category(name = "Skating")
session.add(skating)
session.commit()




hockey = Category(name = "Hockey")
session.add(hockey)
session.commit()

stick = StockItem(name="Stick", description = "Simply Amazing", category=hockey)
session.add(stick)
session.commit()






firstResult = session.query(Category).first()
firstResult.name

items = session.query(StockItem).all()
for item in items:
    print item.name

