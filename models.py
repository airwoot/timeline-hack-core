from app import db

class User(db.Document):
    twitter_id = db.StringField(required = True, unique = True)
    twitter_token = db.StringField(required = True)
    twitter_secret = db.StringField(required = True)
