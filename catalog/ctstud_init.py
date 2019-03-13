from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from data_setup import *

engine = create_engine('sqlite:///bags.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

# Delete BykesCompanyName if exisitng.
session.query(BagCompanyName).delete()
# Delete BykeName if exisitng.
session.query(BagName).delete()
# Delete User if exisitng.
session.query(emailUser).delete()

# Create sample users data
sampleuser = emailUser(
    name="Likhitha Muppalla", email="likhitha1998m@gmail.com")
session.add(sampleuser)
session.commit()

print ("Successfully Add First email User")
# Create sample byke companys
bag1 = BagCompanyName(
    name="skybags", user_id=1)
session.add(bag1)
session.commit()

bag2 = BagCompanyName(
    name="wespa", user_id=1)
session.add(bag2)
session.commit

bag3 = BagCompanyName(
    name="polosky", user_id=1)
session.add(bag3)
session.commit()


# Populare a bykes with models for testing
# Using different users for bykes names year also
item1 = BagName(
    itemname="handbags",
    description="looks stylish", price="250", rating="superb",
    date=datetime.datetime.now(), bagcompanynameid=1, emailuser_id=1)
session.add(item1)
session.commit()

item2 = BagName(
    itemname="schoolbags", description="specially designed for children",
    price="260", rating="excellent", date=datetime.datetime.now(),
    bagcompanynameid=2, emailuser_id=1)
session.add(item2)
session.commit()

item3 = BagName(
    itemname="laguagebags", description="comfortable", price="250",
    rating="superb", date=datetime.datetime.now(),
    bagcompanynameid=3, emailuser_id=1)
session.add(item3)
session.commit()
print("Your bags database has been inserted!")
