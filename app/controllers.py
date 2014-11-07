from flask import current_app
from twitter_helpers import TwitterUser
import twitter
from models import TimelineList, User

def get_logged_in_users_list(user):
    """
        Get lists of the loggedin user from twitter.
        TODO : return lists that are celeb timelines
    """
    t = TwitterUser(user.access_token, user.access_token_secret)
    lists = t.get_user_lists()
    res_lists = filter(lambda x:x if '_sees' in x['name'] else None, lists)
    return res_lists

def get_list(user, list_obj):
    """
        return existing list details
    """
    try:
        t = TwitterUser(user.access_token, user.access_token_secret)
        return t.get_list(list_obj.list_id, list_obj.owner_id)
    except twitter.TwitterError as e:
        if e.message[0]['code'] == 34:
            list_obj.update(set__exists = False)
            return False
    
def create_list(user , screen_name):
    """
        Create list in twitter by finding user by screenname
    """
    t = TwitterUser(user.access_token, user.access_token_secret)
    list_objs = TimelineList.objects(screen_name = screen_name.lower(), exists = True)
    if list_objs:
        list_obj = list_objs[0]
        list_details = get_list(user, list_obj.list_id, list_obj.owner_id)
        if list_details:
            return list_details
    timeline_list = t.create_list(screen_name)
    list_db_obj = TimelineList(list_id = timeline_list.id, owner_id = t.user.id, screen_name = screen_name.lower())
    list_db_obj.save()
    return timeline_list.AsDict()

def subscribe_list(user, list_id, owner_id):
    """
        Subscribe user to existing list
    """
    t = TwitterUser(user.access_token, user.access_token_secret)
    list_obj = TimelineList.objects(list_id = list_id).first()
    if not list_obj:
        raise Exception('LIST NOT FOUND')
    t.subscribe_list(list_id = list_obj.list_id, owner_id = list_obj.owner_id)
    return {
            'success' : True
        }
    
def list_timeline(user, list_id, owner_id, since_id, count):
    """
        Get timeline of a list from twitter.
        TODO If list is deleted create a new one on behalf of user and send timeline
    """
    try:
        t = TwitterUser(user.access_token, user.access_token_secret)
        return t.get_list_timeline(list_id, owner_id, since_id, count)
    except twitter.TwitterError as e:
        from random import choice, randint
        if e.message[0]['code'] == 88:
            user = list(User.objects(access_token_active = True).skip(randint(0,1)).limit(10))
            user = choice(user)
            return list_timeline(user, list_id, owner_id, since_id, count)
        else:
            raise e
def update_list_status(list_id, exists):
    print exists
    TimelineList._get_collection().update({'list_id':list_id},{'$set':{'exists':False}})
