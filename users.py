import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()

class User(Base):
	__tablename__ = "User"
	user_id = Column(String(30), primary_key=True)
	username = Column(String(3000), nullable = False)

engine = create_engine("postgres://stseevpchenioh:e6ca7007aa6177b1a8fd10f86773d4448935dc1df166c4eca587386f620e5f95@ec2-34-251-118-151.eu-west-1.compute.amazonaws.com:5432/d775prj7c951jk")

Session = sessionmaker(bind = engine)
session = Session()

def add(user):
	user.user_id = str(user.user_id)
	try:
		queryr = session.query(User).filter_by(user_id = user.user_id).first()
	
		if not bool(queryr):
			session.add(user)
			session.commit()
			return True
		else:
			queryr.username = user.username
			session.commit()
			return True
	except:
		session.rollback()
		raise
	return False

def get(username):
	try:
		queryr = session.query(User).filter_by(username = username).first()
		if bool(queryr):
			return queryr.user_id
	except:
		session.rollback()
		raise
	return False
