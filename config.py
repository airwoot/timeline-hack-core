class ProductionConfig():
    DEBUG = False

    MONGODB_HOSTS = 'localhost'
    MONGODB_REPLSET = 'rs0'
    MONGODB_DBNAME = 'their_tweets'


    SECRET_KEY = 'thisissecret'
    MULTIPLE_AUTH_HEADERS = ['access_token', 'device']

    PORT = 8000
    PROPOGATE_EXCEPTIONS = True


REDISHOST = 'localhost'
