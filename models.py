from app import db

class User(db.Document):
    twitter_id = db.StringField(required = True, unique = True)
    twitter_token = db.StringField(required = True)
    twitter_secret = db.StringField(required = True)
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
