# Imports
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy, Table, Column

# import sqlalchemy
from sqlalchemy import Table, Column, String, Boolean, MetaData, create_engine
from sqlalchemy.sql import select
from sqlalchemy import exc
from os.path import exists

# Config
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Location of DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BASE_DOMAIN = "http://abc.sh/"
URL_TABLE   = "url_tbl"

# Database related operations
metadata1 = MetaData()
users = Table('user_tbl', metadata1,
  Column('user_id', String, primary_key=True),
  Column('email', String, unique=True),
  Column('password', String),
  Column('is_admin', Boolean),
)

metadata2 = MetaData()
urls = Table(URL_TABLE, metadata2,
  Column('short_url', String, primary_key=True),
  Column('long_url', String),
  Column('user_id', String),
)

engine = create_engine('sqlite:///database.db')

if not exists("./database.db"):
    metadata1.create_all(engine)
    metadata2.create_all(engine)

conn = engine.connect()


# Arguments expected to get from PUT requests
translation_put_args = reqparse.RequestParser()
translation_put_args.add_argument("short_url", type=str, help="The short url is required", required=True)
translation_put_args.add_argument("long_url", type=str, help="The long url is required", required=True)
translation_put_args.add_argument("user_id", type=str, help="The id of the user")


# For the marshall
# translation_resource_fields = {
#     'short_url': fields.String,
#     'long_url': fields.String,
#     'user_id': fields.String,
# }


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
                output = jsonify({short_url: {"short_url": short_url, "long_url": f"ERROR - {short_url} not found", "user_id": "ERROR"}})
            else:
                dictify = {short_url: listify[0]}
                output = jsonify(dictify)
            
        return output
    

    def put(self, short_url):
        args = translation_put_args.parse_args()
        user_id  = args["user_id"] if args["user_id"] != None else "anonymous"
        long_url = args["long_url"]
        
        dictify = {short_url: {"short_url": short_url,
                                "long_url":  long_url,
                                "user_id":  user_id}}
        
        # TODO - validate input
        
        with engine.connect() as con:
            try:
                con.execute(f"INSERT INTO {URL_TABLE} (short_url, long_url, user_id) VALUES (\"{short_url}\", \"{long_url}\", \"{user_id}\");")
                
            except exc.IntegrityError:
                dictify[short_url]['long_url'] = f"ERROR - {short_url} already exists"
                dictify[short_url]['user_id']  = "ERROR"
                return dictify, 409
                    
        return dictify, 201 # TODO - Verify it actually worked
    
    def delete(self, short_url):
        with engine.connect() as con:
            con.execute(f"DELETE FROM {URL_TABLE} WHERE short_url = \"{short_url}\";")
        return '', 204



class GetUserURLs(Resource):
    def get(self, user_id):
        
        output = None
        with engine.connect() as con:

            output = con.execute(f"SELECT * FROM {URL_TABLE} WHERE user_id = \"{user_id}\";")
            output = jsonify({'output': [dict(row) for row in output]})
        return output

                

api.add_resource(UrlTranslations, "/translate/<string:short_url>")
api.add_resource(GetUserURLs, "/get_user_urls/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
    
    