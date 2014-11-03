from app import db

class User(db.Document):
    twitter_id = db.IntField(required = True, unique = True)
    access_token = db.StringField(required = True)
    access_token_secret = db.StringField(required = True)
    screen_name = db.StringField(required  = True)
    registered_on = db.DateTimeField(required = True)

    def is_authenticated(self):
        return True
 
    def is_active(self):
        return True
 
    def is_anonymous(self):
        return False
 
    def get_id(self):
        return unicode(self.id)
 
    def __repr__(self):
        return '<User %r>' % (self.username)

class TimelineList(db.Document):
    screen_name = db.StringField(required = True)
    owner_id = db.IntField(required = True)
    list_id = db.IntField(required = True)
