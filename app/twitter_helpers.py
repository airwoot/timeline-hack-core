import twitter
from config import *

class TwitterUser():
    def __init__(self, access_token, access_token_secret, client):
        print client
        self.api = twitter.Api(
                    consumer_key = client_secrets[client]['key'],
                    consumer_secret = client_secrets[client]['secret'],
                    access_token_key = access_token,
                    access_token_secret = access_token_secret
                )

    def get_list_timeline(timeline_id, user_id, since_id, count = 10):
        count = 100 if count > 100 else count
        res = api.GetListTimeline(timeline_id , slug = None, owner_id = owner_id, count = count)
        return [r.AsDict() for r in res]
        
    def get_user_lists():
        res = api.GetLists()
        return [r.AsDict() for r in res]

    def create_list(screen_name):
        user = self.api.VerifyCredentials()
        timeline_for = self.api.GetUser(screen_name = screen_name)
        list_members = self.api.GetFriendIDs(timeline_for.id)
        list_members = map(str, listmembers)
        timeline_list = self.api.CreateList(timeline_for.screen_name + '_sees')
        self.api.CreateListsMember(timeline_list.id, user.id, list_members[:35])
        #create cel task to add all the members to the list
        return timeline_list

    def subscribe_list(list_id, owner_id):
        return self.api.CreateSubscription(owner_id = owner_id, list_id = list_id)

    def post_tweet(self, tweet):
        print 'posting:',tweet
        self.api.PostUpdate(tweet)

    def post_reply(self, tweet, tweet_id):
        print 'replying to:', tweet_id
        tweet = self.api.PostUpdate(tweet, in_reply_to_status_id = tweet_id)
        return str(tweet.id)

    def post_media(self, media, status = ''):
        print 'image:', media
        self.api.PostMedia(status, media)

    def post_retweet(self):
        from random import choice
        trends = self.get_trends()
        trend = choice(trends)
        tweets = self.get_search(trend.query)
        if tweets:
            tweet = choice(tweets)
            tweet_id = tweet.id
            print 'retweet:', tweet_id
            tweet = self.api.PostRetweet(original_id = tweet_id)
            print tweet.id
        else:
            self.post_retweet()

    def follow(self, screen_name):
        self.api.CreateFriendship(screen_name = screen_name)
    
    def get_trends(self):
        return self.api.GetTrendsCurrent()

    def get_search(self, query):
        return self.api.GetSearch(query)

    def follow_user(self, screen_name):
        self.api.CreateFriendship(screen_name = screen_name)

    def get_user_timeline(self, screen_name):
        timeline = self.api.GetUserTimeline(screen_name = screen_name)
        return timeline
    
    def favorite_tweet(self, tweet_id):
        self.api.CreateFavorite(id = tweet_id)

