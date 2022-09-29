# Imports
from sqlite3 import IntegrityError
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from url_user import USER_TABLE, User
# from flask_sqlalchemy import SQLAlchemy, Table, Column

# import sqlalchemy
from sqlalchemy import Table, Column, String, Boolean, MetaData, create_engine
from sqlalchemy.sql import select
from sqlalchemy import exc

# import etc
from os.path import exists
import app_utils


URL_TABLE   = "url_tbl"


# Arguments expected to get from POST requests
translation_args = reqparse.RequestParser()
translation_args.add_argument("short_url", type=str, help="The short url is required", required=True)
translation_args.add_argument("long_url", type=str, help="The long url is required", required=True)
translation_args.add_argument("user_id", type=str, help="The id of the user")


# REST API methods for the translate page
# {BASE_DOMAIN}/translate/<string:short_url>"
class UrlTranslations(Resource):
    # @marshal_with(translation_resource_fields) # Serialize it to json format 
    def get(self, short_url):
        engine = create_engine('sqlite:///database.db')
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
        engine = create_engine('sqlite:///database.db')
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
        engine = create_engine('sqlite:///database.db')
        with engine.connect() as con:
            # TODO - Check it's deleted
            con.execute(f"DELETE FROM {URL_TABLE} WHERE short_url = \"{short_url}\";")
        return '', 204
