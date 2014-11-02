from flask import current_app, redirect, url_for
from flask.ext import restful
from flask.ext.login import login_required, current_user, login_user, logout_user
import tweepy
from request_parsers import *
from datetime import datetime
from models import *

class TwitterAuth(restful.Resource):
    @login_required
    def get(self):
        oauth = tweepy.OAuthHandler(current_app.config['CONSUMER_KEY'], current_app.config['CONSUMER_SECRET'], secure=True)
        oauth.callback = url_for('login', _external=True)
        auth_url = oauth.get_authorization_url()
        return redirect(auth_url)
       
class Login(restful.Resource):
    def get(self):
        return {'status':'Welcome'}
    
class TwitterCallback(restful.Resource):
    def post(self):
        try:
            oauth = tweepy.OAuthHandler(current_app.config['CONSUMER_KEY'], current_app.config['CONSUMER_SECRET'], secure=True)
            verifier = request.args.get('oauth_verifier')
            oauth.get_access_token(verifier)
            api = tweepy.Api(oauth.access_token())
            u = api.verify_credentails()
            if u:
                if not User.objects.get(twitter_id = u.id):
                    user = User(
                            twitter_id = u.id, 
                            twitter_token = oauth.access_token,
                            twitter_secret = oauth.access_token_secret,
                            screen_name = u.screen_name,
                            registered_on = datetime.now()
                            )
                    user.save()
            user = User.objects.get(twitter_id = '1')

            login_user(user)
            return
        except Exception as e:
            print e
            restful.abort(500, message = 'Internal Server Error.')

class MyLists(restful.Resource):
    @login_required
    def get(self):
        args = list_parser.parse_args()
        user = current_user
        try:
            pass
        except Exception as e:
            print e
            restful.abort(500, message = 'Internal Server Error.')
            
