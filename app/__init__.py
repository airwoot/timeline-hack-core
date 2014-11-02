from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.mongoengine import MongoEngine
from flask.ext import restful
from redis import Redis
from config import *

app = Flask(__name__)
app.config.from_object('config.ProductionConfig')

db = MongoEngine(app)
db.connection.frankly.authenticate(config.MONGODB_USERNAME, config.MONGODB_PASSWORD)

login_manager = LoginManager()
login_manager.init_app(app)

redis_client = Redis(REDISHOST, db = REDISDB)

@login_manager.header_loader
def load_header(header_vals):
    print header_vals
    access_token = header_vals.get('X-Token')
    if not access_token:
        return None
    user_id = redis_client.get(access_token)
    if user_id:
        return User.objects.get(id = user_id)
    return None



api = restful.Api(app)


