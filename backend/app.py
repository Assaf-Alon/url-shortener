# Imports
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy, Table, Column

# import sqlalchemy
from sqlalchemy import Table, Column, String, Boolean, MetaData, create_engine
from sqlalchemy.sql import select
from os.path import exists

# Config
app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Location of DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
BASE_DOMAIN = "http://abc.sh/"



# # Models
# class UrlModel(db.Model):
#     short_url = db.Column(db.String, primary_key=True)
#     long_url  = db.Column(db.String, nullable=False)
#     user_id   = db.Column(db.String) # empty if anonymous
    
#     def __repr__(self):
#         return f"short_url = {short_url}, long_url = {long_url}, user_id = {user_id}"
    

# class UserModel(db.Model):
#     user_id  = db.Column(db.String, primary_key=True)
#     email    = db.Column(db.String, unique=True)
#     password = db.Column(db.String)
#     is_admin = db.Column(db.Boolean)
    
#     def __repr__(self):
#         return f"user_id = {user_id}, email = {email}{', admin' if is_admin else ''} "

metadata1 = MetaData()
users = Table('user_tbl', metadata1,
  Column('user_id', String, primary_key=True),
  Column('email', String, unique=True),
  Column('password', String),
  Column('is_admin', Boolean),
)

metadata2 = MetaData()
urls = Table('url_tbl', metadata2,
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
translation_resource_fields = {
    'short_url': fields.String,
    'long_url': fields.String,
    'user_id': fields.String,
}

# def abort_if_translation_doesnt_exist(short_url):
#     if short_url not in translations.keys():
#         abort(404, message=f"URL {BASE_DOMAIN}{short_url} doesn't exist")
        
        
# def abort_if_translation_exists(short_url):
#     if short_url in translations.keys():
#         abort(409, message=f"URL {BASE_DOMAIN}{short_url} already exists")
    
    
class UrlTranslations(Resource):
    @marshal_with(translation_resource_fields) # Serialize it to json format 
    def get(self, short_url):
        res = UrlModel.query.get(short_url=short_url)
        return res

    @marshal_with(translation_resource_fields)
    def put(self, short_url):
        args = translation_put_args.parse_args()
        user_id  = args["user_id"] if args["user_id"] != None else "anonymous"
        long_url = args["long_url"]
        
        # validate input
        
        with engine.connect() as con:

            output = con.execute(f"INSERT INTO url_tbl (short_url, long_url, user_id) VALUES (\"{short_url}\", \"{long_url}\", \"{user_id}\");")
        
        return output, 201 # TODO - FIX
    
    @marshal_with(translation_resource_fields)
    def delete(self, short_url):
        abort_if_translation_doesnt_exist(short_url)
        del translations[short_url]
        return '', 204



class GetUserURLs(Resource):
    # @marshal_with(translation_resource_fields) # Serialize it to json format 
    def get(self, user_id):
        
        output = None
        with engine.connect() as con:

            output = con.execute(f"SELECT * FROM url_tbl WHERE user_id = \"{user_id}\";")
            output = jsonify({'output': [dict(row) for row in output]})
        return output
        # print()
        # print()
        # print()
        # print()
        # print(output.first)
        # print(dir(output))
        # return 1
        # return jsonify({[dict(row) for row in output]})
        
        
        
        print(result)
        print()
        print()
        print()
        return result

                

api.add_resource(UrlTranslations, "/translate/<string:short_url>")
api.add_resource(GetUserURLs, "/get_user_urls/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
    
    