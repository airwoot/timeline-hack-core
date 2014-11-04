from celery import Celery
from app.twitter_helpers import TwitterUser
import twitter
from twitter import TwitterError
from random import randint
import traceback

cel = Celery(broker = 'redis://localhost', backend = 'redis://localhost')
CONSUMER_KEY = 'bgEZ37ZUH2HeZ3aAyeh9VEsyb'
CONSUMER_SECRET = '9OQqbx5elvBb7eDwfHq4BEKBI9UqOFIUT72mkVsx0XuWhickR5'

@cel.task
def add_users_to_list(access_token, access_token_secret, list_id, owner_id, list_members):
    try:
        api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, access_token, access_token_secret)
        api.CreateListsMember(list_id, owner_id, list_members[0:29])
    except TwitterError as e:
        if e.message[0]['code'] == 88:
            add_users_to_list.apply_async(args = [access_token, access_token_secret, list_id, owner_id, list_members], countdown = randint(1200,1500))
        print traceback.format_exc(e)
