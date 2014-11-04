from flask import current_app, redirect, url_for, request, session, flash
from flask.ext import restful
from flask.ext.login import login_required, current_user, login_user, logout_user
import twitter
from request_parsers import *
from datetime import datetime
from models import *
from rauth.service import OAuth1Service
from rauth.utils import parse_utf8_qsl
from twitter_helpers import TwitterUser
import controllers



class TwitterAuth(restful.Resource):
    def get(self):
        twitter_auth_loader = OAuth1Service(
	    name='twitter',
	    consumer_key=current_app.config['CONSUMER_KEY'],
	    consumer_secret=current_app.config['CONSUMER_SECRET'],
	    request_token_url='https://api.twitter.com/oauth/request_token',
	    access_token_url='https://api.twitter.com/oauth/access_token',
	    authorize_url='https://api.twitter.com/oauth/authorize',
	    base_url='https://api.twitter.com/1.1/'
		)
        oauth_callback = url_for('twittercallback', _external=True)
        params = {'oauth_callback': oauth_callback}
        auth_url = twitter_auth_loader.get_raw_request_token(params=params)
        data = parse_utf8_qsl(auth_url.content)

        session['twitter_oauth'] = (data['oauth_token'],
                                data['oauth_token_secret'])
        return redirect(twitter_auth_loader.get_authorize_url(data['oauth_token'], **params))
       
class Login(restful.Resource):
    @login_required
    def get(self):
        return {'status':'Welcome'}
    
class TwitterCallback(restful.Resource):
    def get(self):
        try:
            print session
            request_token, request_token_secret = session.pop('twitter_oauth')
            twitter_auth_loader = OAuth1Service(
		    name='twitter',
		    consumer_key=current_app.config['CONSUMER_KEY'],
		    consumer_secret=current_app.config['CONSUMER_SECRET'],
		    request_token_url='https://api.twitter.com/oauth/request_token',
		    access_token_url='https://api.twitter.com/oauth/access_token',
		    authorize_url='https://api.twitter.com/oauth/authorize',
		    base_url='https://api.twitter.com/1.1/'
			)
            if not 'oauth_token' in request.args:
                print 'You did not authorize the request'
                return redirect(url_for('index'))
            
            try:
                creds = {'request_token': request_token,
                        'request_token_secret': request_token_secret}
                params = {'oauth_verifier': request.args['oauth_verifier']}
                sess = twitter_auth_loader.get_auth_session(params=params, **creds)
                print sess.access_token
            except Exception, e:
                flash('There was a problem logging into Twitter: ' + str(e))
                return redirect(url_for('index'))
            api = twitter.Api(
                current_app.config['CONSUMER_KEY'],
                current_app.config['CONSUMER_SECRET'],
                sess.access_token,
                sess.access_token_secret
			)            
            u = api.VerifyCredentials()
            user = User.objects(twitter_id = u.id).first()
            if not user:
                user = User(twitter_id = u.id, screen_name = u.screen_name, registered_on = datetime.now(), access_token = sess.access_token, access_token_secret = sess.access_token_secret)
                user.save()
            else:
                user.update(set__access_token = sess.access_token, set__access_token_secret = sess.access_token_secret)
            login_user(user)
            return redirect('/login')
        except Exception as e:
            import traceback
            print traceback.format_exc(e)
            restful.abort(500, message = 'Internal Server Error.')

class MyLists(restful.Resource):
    @login_required
    def get(self):
        #args = list_parser.parse_args()
        #TODO also return subscribed lists
        user = current_user
        try:
            return controllers.get_logged_in_users_list(user)
            pass
        except Exception as e:
            import traceback
            print traceback.format_exc(e)
            restful.abort(500, message = 'internal server error.')
            
class CreateList(restful.Resource):
    @login_required
    def get(self):
        args = create_list_parser.parse_args()
        user = current_user
        try:
            return controllers.create_list(user, args['screen_name'])
            pass
        except Exception as e:
            import traceback
            print traceback.format_exc(e)
            restful.abort(500, message = 'internal server error.')

class SubscribeList(restful.Resource):
    @login_required
    def get(self):
        args = subscribe_list_parser.parse_args()
        user = current_user
        try:
            return controllers.subscribe_list(user, args['list_id'], args['owner_id'])
        except Exception as e:
            import traceback
            print traceback.format_exc(e)
            restful.abort(500, message = 'internal server error.')

class DiscoverList(restful.Resource):
    @login_required
    def get(self):
        args = discover_list_parser.parse_args()
        try:
            list_objs = list(TimelineList._get_collection().find({'exists' : True}).skip(args['skip']).limit(args['limit']))
            map(lambda x:x.pop('_id'),list_objs)
            return list_objs
        except Exception as e:
            import traceback
            print traceback.format_exc(e)
            restful.abort(500, message = 'internal server error.')

class ListTimeline(restful.Resource):
    @login_required
    def get(self):
        args = list_timeline_parser.parse_args()
        user = current_user
        try:
            return controllers.list_timeline(user, args['list_id'], args['owner_id'], args['since_id'], args['count'])
        except Exception as e:
            import traceback
            print traceback.format_exc(e)
            restful.abort(500, message = 'internal server error.')
        
