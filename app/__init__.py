from flask import Flask, g
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine
from flask.ext import restful

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

db = MongoEngine(app)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_header(_id):
    from models import User
    return User.objects.get(id = _id)


api = restful.Api(app)

from resources import Login, TwitterAuth

api.add_resource(Login, '/login')
api.add_resource(TwitterAuth, '/twitter_auth')
api.add_resource(TwitterCallback, '/twitter_callback')
