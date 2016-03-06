#!flask/bin/python 
from app import db,models

a  = models.User(nickname = "Anna", id = 0)
b  = models.User(nickname = "Felix", id = 1)
db.session.add(b)
db.session.add(a)
db.session.commit()