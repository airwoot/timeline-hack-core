from flask.ext import restful
from flask.ext.login import login_required, current_user
import twitter
from app import redis_cleint

class Login(restful.Resource):
    def get():
        return {'status':'Welcome'}
    
    def post():
        args = twitter_parser.parse_args()
        try:
            api = twitter.Api('aaNDJcxdHadQTxBW8P7B42yoy','AAOwvDBHlci4WmJANTmgOLJg28v3HSx0SogBEfQY9TGamsF9CS', args['access_token'], args['token_secret'])
            u = api.VerifyCredentials()
            if str(u.id) == args['twitter_user_id']:
                try:
                    user = User.objects.only('twitter_token', 'twitter_secret').get(twitter_id = u.id)
                    redis_client.set(args['access_token'], u.id, ex = 86400)
                    if user.twitter_token != args['token_secret']:
                        user.update(set__twitter_token = args['access_token'], set__twitter_secret = args['twitter_secret'])
                return {
                    'sucess' : True, 
                    'new_user' : False
                }
                except:
                    user = User(twitter_id = u.id, twitter_token = args['access_token'], twitter_secret = args['social_use'])
                    user.save()
                return {
                    'sucess' : True,
                    'new_user' : True    
                }
            else:
                raise UserCredentialsDontMatch()
        except UserCredentailsDontMatch:
                restful.abort(403,message = 'twitter creds dont match.')
        except Exception as e:
                restful.abort(500, message = 'Internal Server Error.')
