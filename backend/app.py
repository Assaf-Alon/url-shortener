# Imports
from sqlite3 import IntegrityError
from flask import Flask, jsonify
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
# from flask_sqlalchemy import SQLAlchemy, Table, Column

# import sqlalchemy
from sqlalchemy import Table, Column, String, Boolean, MetaData, create_engine
from sqlalchemy.sql import select
from sqlalchemy import exc

# import etc
from os.path import exists
import app_utils
from url_user import USER_TABLE, User
from url_translation import URL_TABLE, UrlTranslations

# Config
app = Flask(__name__)
cors = CORS(app, origins=['http://localhost:8080'])
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Location of DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BASE_DOMAIN = "http://abc.sh/"





class GetUserURLs(Resource):
    def get(self, user_id):
        
        engine = create_engine('sqlite:///database.db')
        output = None
        with engine.connect() as con:

            output = con.execute(f"SELECT * FROM {URL_TABLE} WHERE user_id = \"{user_id}\";")
            output = jsonify([dict(row) for row in output])
        return output

                

api.add_resource(UrlTranslations, "/translate/<string:short_url>")
api.add_resource(GetUserURLs, "/get_user_urls/<string:user_id>")
api.add_resource(User, "/user/<string:user_id>")

if __name__ == "__main__":
    
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
    
    app.run(debug=True)
    
    
    