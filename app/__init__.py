from flask import Flask, g, send_file
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

from resources import Login, TwitterAuth, TwitterCallback, MyLists, CreateList, SubscribeList, DiscoverList, ListTimeline

api.add_resource(Login, '/login')
api.add_resource(TwitterAuth, '/twitter_auth')
api.add_resource(TwitterCallback, '/twitter_callback')
api.add_resource(MyLists, '/list/my')
api.add_resource(CreateList, '/list/create')
api.add_resource(SubscribeList, '/list/subscribe')
api.add_resource(DiscoverList, '/list/discover')
api.add_resource(ListTimeline, '/list/timeline')

@app.after_request
def add_access_control_headers(response):
    """Adds the required access control headers"""
    response.headers['Access-Control-Allow-Origin'] = '*' 
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Set-Cookie'
    response.headers['Access-Control-Allow-Methods'] = 'POST,GET,PUT,DELETE'
    response.headers['Cache-Control'] = 'No-Cache'
    return response

