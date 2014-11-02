from reqparse import RequestParser

# twitter parser
twitter_parser = reqparse.RequestParser()
twitter_parser.add_argument('external_access_token', type=str, location='json', required=True)
twitter_parser.add_argument('token_secret', type=str, location='json', required=True)
twitter_parser.add_argument('social_user_id', type=str, location='json', required=True)
