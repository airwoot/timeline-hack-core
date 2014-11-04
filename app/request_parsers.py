from flask.ext.restful import reqparse

#create list parser
create_list_parser = reqparse.RequestParser()
create_list_parser.add_argument('screen_name', type = str, location = 'args', required = True)
create_list_parser.add_argument('since_id', type = int , location = 'args')

#subscribe list parser
subscribe_list_parser = reqparse.RequestParser()
subscribe_list_parser.add_argument('list_id', type = int, location='args', required  = True)
subscribe_list_parser.add_argument('owner_id', type = int, location='args', required  = True)

#discover list parser
discover_list_parser = reqparse.RequestParser()
discover_list_parser.add_argument('skip', type= int, location = 'args', default = 0)
discover_list_parser.add_argument('limit', type= int, location = 'args', default = 10)

#list timeline parser
list_timeline_parser = reqparse.RequestParser()
list_timeline_parser.add_argument('list_id', type = int, location='args', required  = True)
list_timeline_parser.add_argument('owner_id', type = int, location='args', required  = True)
list_timeline_parser.add_argument('since_id', type = int, location='args', default = None)
list_timeline_parser.add_argument('count', type = int, location='args', default = 10)

