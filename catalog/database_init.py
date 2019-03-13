from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import datetime
from Data_Setup import *

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

# Delete BagsCompanyName if exisitng.
session.query(BagCompanyName).delete()
# Delete BagsName if exisitng.
session.query(BagName).delete()
# Delete User if exisitng.
session.query(GmailUser).delete()

# Create sample users data
User1 = GmailUser(name="Gouse Mastan Vali Shaik",
                  email="gousemastan7867@gmail.com",
                  )
session.add(User1)
session.commit()
print ("Successfully Add First User")
# Create sample bags companys
BagCompany1 = BagCompanyName(name="The North Face",
                             user_id=1)
session.add(BagCompany1)
session.commit()

BagCompany2 = BagCompanyName(name="American Tourist",
                             user_id=1)
session.add(BagCompany2)
session.commit

BagCompany3 = BagCompanyName(name="Wildcraft",
                             user_id=1)
session.add(BagCompany3)
session.commit()

BagCompany4 = BagCompanyName(name="Fasttrack",
                             user_id=1)
session.add(BagCompany4)
session.commit()

BagCompany5 = BagCompanyName(name="Skybags",
                             user_id=1)
session.add(BagCompany5)
session.commit()

BagCompany6 = BagCompanyName(name="Gear",
                             user_id=1)
session.add(BagCompany6)
session.commit()

# Populare a bags with models for testing
# Using different users for names names year also
Bag1 = BagName(bagname=" Serial Backpack 002",
                       color="Red",
                       rating="9.2",
                       price="17650/-",
                       bagtype="backpack",
                       date=datetime.datetime.now(),
                       bagcompanynameid=1,
                       gmailuser_id=1)
session.add(Bag1)
session.commit()

Bag2 = BagName(bagname="Aegis Core Travel",
                       color="black",
                       rating="8.9",
                       price="7,089/-",
                       bagtype="Duffel Bag",
                       date=datetime.datetime.now(),
                       bagcompanynameid=2,
                       gmailuser_id=1)
session.add(Bag2)
session.commit()

Bag3 = BagName(bagname="Flip Ruck",
                       color="blue",
                       rating="9.7",
                       price="5,500/-",
                       bagtype="Rucksack",
                       date=datetime.datetime.now(),
                       bagcompanynameid=3,
                       gmailuser_id=1)
session.add(Bag3)
session.commit()

Bag4 = BagName(bagname="Shoulder Bag",
                       color="pink",
                       rating="9",
                       price="2,950/-",
                       bagtype="Sling Bag ",
                       date=datetime.datetime.now(),
                       bagcompanynameid=4,
                       gmailuser_id=1)
session.add(Bag4)
session.commit()

Bag5 = BagName(bagname="Tic Tok Duffel",
                       color="yellow",
                       rating="9.5",
                       price="8,065/-",
                       bagtype="Travel Duffel",
                       date=datetime.datetime.now(),
                       bagcompanynameid=5,
                       gmailuser_id=1)
session.add(Bag5)
session.commit()

Bag6 = BagName(bagname="columbia expandable",
                       color="green",
                       rating="8.5",
                       price="4,730/-",
                       bagtype="trolley",
                       date=datetime.datetime.now(),
                       bagcompanynameid=6,
                       gmailuser_id=1)
session.add(Bag6)
session.commit()

print("Your bags database has been inserted!")
