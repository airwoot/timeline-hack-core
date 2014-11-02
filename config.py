class ProductionConfig():
    DEBUG = False

    MONGODB_HOST = 'localhost'
    MONGODB_DBNAME = 'their_tweets'
    MONGODB_SETTINGS = {
        'host' : 'localhost',
        'DB' : 'new',
        'port' : 27017
    }


    SECRET_KEY = 'thisissecret'
    MULTIPLE_AUTH_HEADERS = ['access_token', 'device']

    PORT = 8000
    PROPOGATE_EXCEPTIONS = True
    CONSUMER_KEY = 'bgEZ37ZUH2HeZ3aAyeh9VEsyb'
    CONSUMER_SECRET = '9OQqbx5elvBb7eDwfHq4BEKBI9UqOFIUT72mkVsx0XuWhickR5'
    REDISHOST = 'localhost'
    REDISDB = 1


