from unicodedata import name
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


##### Init class #####
db = SQLAlchemy()




##models###rr
class Castomers(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    profile_pic = db.Column(db.String(), nullable=True)
    national_id_face = db.Column(db.String(), nullable=True)
    national_id_back = db.Column(db.String(), nullable=True)
    isactivated = db.Column(db.String(80), nullable=False)
   
    def __init__(self,name,username,phone , email,password , profile_pic , national_id_face , national_id_back , isactivated):
        self.name = name
        self.username=username
        self.phone = phone
        self.email = email
        self.password = password
        self.profile_pic = profile_pic
        self.national_id_face = national_id_face
        self.national_id_back = national_id_back
        self.isactivated = isactivated
       
    @classmethod
    def insert(self,username,password , active ):

        sessions = Castomers(username = username ,password = password , active=active)

        # add to db and commit
        db.session.add(sessions)
        db.session.commit()


    @classmethod
    def getByUsername(self, username):
        query = self.query.filter_by(username=username).first()
        return query


    @classmethod
    def getByEmail(self, email):
        query = self.query.filter_by(email=email).first()
        return query


    @classmethod
    def get_active_value(self, id):
        query = self.query.filter_by(id=id).first()
        active_value = query.isactivated
        return active_value

    @classmethod
    def Get_all_users(self, username):
        query = self.query.filter_by(username=username).first()
        stsssusername = query.name

        return stsssusername

    @classmethod
    def update_active_value(self, id, isactivated):
        query = self.query.get(id)

        # update values in query
        query.isactivated = isactivated


        # commit the updates
        db.session.commit()
    @classmethod
    def get(self, id):

        query = self.query.get(id)

        return query

    @classmethod
    def get_id(self, username):
        query = self.query.filter_by(username=username).first()
        id = query.id

        return id

################admins ############
class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    username = db.Column(db.String(80), nullable=False)
    phone = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    password = db.Column(db.String(80), nullable=False)
    profile_pic = db.Column(db.String(), nullable=True)
    national_id_face = db.Column(db.String(), nullable=True)
    national_id_back = db.Column(db.String(), nullable=True)
   
    def __init__(self,name,username,phone , email,password , profile_pic , national_id_face , national_id_back):
        self.name = name
        self.username=username
        self.phone = phone
        self.email = email
        
        self.password = password
        self.profile_pic = profile_pic
        self.national_id_face = national_id_face
        self.national_id_back = national_id_back
       
    @classmethod
    def insert(self,username,password ):

        sessions = Castomers(username = username ,password = password)

        # add to db and commit
        db.session.add(sessions)
        db.session.commit()


    @classmethod
    def getByUsername(self, username):
        query = self.query.filter_by(username=username).first()
        return query


    @classmethod
    def getByEmail(self, email):
        query = self.query.filter_by(email=email).first()
        return query


   