from flask.ext.restful import reqparse

# twitter parser
twitter_parser = reqparse.RequestParser()
twitter_parser.add_argument('external_access_token', type=str, location='json', required=True)
twitter_parser.add_argument('token_secret', type=str, location='json', required=True)
twitter_parser.add_argument('social_user_id', type=str, location='json', required=True)

#create list parser
create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('screen_name', type = str, location = 'args', required = True)
create_list_parser.add_argument('since_id', type = int , location = 'args')
