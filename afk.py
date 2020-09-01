import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
 
Base = declarative_base()

class AFK(Base):
	__tablename__ = "AFK"
	user_id = Column(String(30), primary_key=True)
	reason = Column(String(3000), nullable = False)

engine = create_engine("postgres://stseevpchenioh:e6ca7007aa6177b1a8fd10f86773d4448935dc1df166c4eca587386f620e5f95@ec2-34-251-118-151.eu-west-1.compute.amazonaws.com:5432/d775prj7c951jk")

Session = sessionmaker(bind = engine)
session = Session()

def add(afk):
	afk.user_id = str(afk.user_id)
	try:
		queryr = session.query(AFK).filter_by(user_id = user_id).first()
	
		if not bool(queryr):
			session.add(afk)
			session.commit()
			return True
		else:
			queryr.reason = afk.reason
			session.commit()
			return True
	except:
		session.rollback()
		raise
	return False

def get(user_id):
	user_id = str(user_id)
	try:
		queryr = session.query(AFK).filter_by(user_id = user_id).first()
		if bool(queryr):
			return queryr.reason
	except:
		session.rollback()
		raise
	return False

def rm(user_id):
	user_id = str(user_id)
	if not get(user_id):
		return False
	try:
		queryr = session.query(AFK).filter_by(user_id = user_id)
		queryr.delete()
		session.commit()
		return True
	except:
		session.rollback()
		raise
	return False
