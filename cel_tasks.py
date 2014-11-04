from celery import Celery
from app.twitter_helpers import TwitterUser
from twitter import TwitterError
from random import randint
import traceback

cel = Celery(broker = 'redis://localhost', backend = 'redis://localhost')

@cel.task
def add_users_to_list(access_token, access_token_secret, list_id, list_members):
    try:
        user = TwitterUser(access_token, access_token_secret)
        user.add_list_members(list_id, list_members)
    except TwitterError as e:
        if e.message['messsage'] == 88:
            add_users_to_list.apply_async(args = [access_token, access_token_secret, list_id, list_members], countdown = randint(1200,1500))
        print traceback.format_exc(e)
