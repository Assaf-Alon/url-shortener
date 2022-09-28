# Imports
from sqlite3 import IntegrityError
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy, Table, Column

# import sqlalchemy
from sqlalchemy import Table, Column, String, Boolean, MetaData, create_engine
from sqlalchemy.sql import select
from sqlalchemy import exc
from os.path import exists

import app_utils

# Config
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Location of DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BASE_DOMAIN = "http://abc.sh/"
URL_TABLE   = "url_tbl"
USER_TABLE  = "user_tbl"

# Database related operations
user_metadata = MetaData()
users = Table(USER_TABLE, user_metadata,
  Column('user_id', String, primary_key=True),
  Column('email', String, unique=True),
  Column('password', String),
  Column('is_admin', Boolean),
)

url_metadata = MetaData()
urls = Table(URL_TABLE, url_metadata,
  Column('short_url', String, primary_key=True),
  Column('long_url', String),
  Column('user_id', String),
)

engine = create_engine('sqlite:///database.db')

if not exists("./database.db"):
    user_metadata.create_all(engine)
    url_metadata.create_all(engine)


# Arguments expected to get from POST requests
translation_args = reqparse.RequestParser()
translation_args.add_argument("short_url", type=str, help="The short url is required", required=True)
translation_args.add_argument("long_url", type=str, help="The long url is required", required=True)
translation_args.add_argument("user_id", type=str, help="The id of the user")


user_args = reqparse.RequestParser()
user_args.add_argument("user_id",  type=str, help="The username")
user_args.add_argument("password", type=str, help="The passowrd of the user")
user_args.add_argument("email",    type=str, help="The user's email address")

# REST API methods for the translate page
# {BASE_DOMAIN}/translate/<string:short_url>"
class UrlTranslations(Resource):
    # @marshal_with(translation_resource_fields) # Serialize it to json format 
    def get(self, short_url):
        output = None
        
        with engine.connect() as con:
            output = con.execute(f"SELECT * FROM {URL_TABLE} WHERE short_url = \"{short_url}\";")
            listify = [dict(row) for row in output]
            
            if (len(listify) == 0):
                abort(404)
            else:
                dictify = {short_url: listify[0]}
                output = jsonify(dictify)
            
        return output
    

    def post(self, short_url):
        args = translation_args.parse_args()
        trans_dict = app_utils.get_translation_dict(args)
        
        # Input validation
        if not app_utils.is_short_url_valid(trans_dict['short_url']):
            trans_dict['message'] = f"ERROR - {short_url} is an invalid URL. Please choose a different one"
            
        # if not app_utils.is_user_id_valid(trans_dict['user_id']):
        #     trans_dict['message'] = f"ERROR - {trans_dict['user_id']} is an invalid username."
        
        with engine.connect() as con:
            try:
                con.execute(f"INSERT INTO {URL_TABLE} (short_url, long_url, user_id) VALUES (\"{short_url}\", \"{trans_dict['long_url']}\", \"{trans_dict['user_id']}\");")
                
            except exc.IntegrityError:
                trans_dict['message'] = f"ERROR - {short_url} already exists"
                return trans_dict, 409
                    
        return trans_dict, 201 # TODO - Verify it actually worked
    
    
    
    def delete(self, short_url):
        with engine.connect() as con:
            # TODO - Check it's deleted
            con.execute(f"DELETE FROM {URL_TABLE} WHERE short_url = \"{short_url}\";")
        return '', 204


# REST API methods for the user page
class User(Resource):
    def get(self, user_id):
        args = user_args.parse_args()
        
        if "user_id" not in args.keys():
            return jsonify({"message": "Anonymous login permitted"})
        
        
        output = None
        with engine.connect() as con:

            output = con.execute(f"SELECT * FROM {USER_TABLE} WHERE user_id = \"{args['user_id']}\";")
            output = [dict(row) for row in output]
            if (len(output) == 0):
                return {"message": "username not found"}, 404
            output = output[0]
            if args['password'] == output['password']:
                return {"message": f"{args['user_id']} login permitted"}, 200
            
            return {"message": "Invalid password"}, 403
        #     output = jsonify(output)
        # return output
        
    def post(self, user_id):
        args = user_args.parse_args()
        
        # Input validation
        if "user_id" not in args.keys() or "password" not in args.keys() or "email" not in args.keys():
            args['message'] = f"Required argument not specified. Required args: user_id, password, email"
            return args, 405
        
        if not app_utils.is_user_id_valid(args['user_id']):
            args['message'] = f"username {args['user_id']} is invalid. Please choose a different one."
            return args, 405

        with engine.connect() as con:
            try:
                con.execute(f"INSERT INTO {USER_TABLE} (user_id, password, email) VALUES (\"{args['user_id']}\", \"{args['password']}\", \"{args['email']}\");")
            except exc.IntegrityError:
                args['message'] = f"ERROR - user {user_id} already exists"
                return args, 409
        return args, 201 # TODO - VERIFY IT ACTUALLY WORKED

    def delete(self, user_id):
        pass

class GetUserURLs(Resource):
    def get(self, user_id):
        
        output = None
        with engine.connect() as con:

            output = con.execute(f"SELECT * FROM {URL_TABLE} WHERE user_id = \"{user_id}\";")
            output = jsonify({'output': [dict(row) for row in output]})
        return output

                

api.add_resource(UrlTranslations, "/translate/<string:short_url>")
api.add_resource(GetUserURLs, "/get_user_urls/<string:user_id>")
api.add_resource(User, "/user/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
    
    