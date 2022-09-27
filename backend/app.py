# Imports
from gettext import translation
import marshal
from typing_extensions import Required
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

# Config
app = Flask(__name__)
api = Api(app)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db' # Location of DB
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
BASE_DOMAIN = "http://abc.sh/"

#######################
# FIRST RUN ONLY!!!!1 #
#######################
init_db = False

# Models
# class UrlModel(db.Model):
#     short_url = db.Column(db.String, primary_key=True)
#     long_url  = db.Column(db.String, nullable=False)
#     user_id   = db.Column(db.String) # empty if anonymous
    

# if init_db:
#     db.create_all()

translations = dict()

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

def abort_if_translation_doesnt_exist(short_url):
    if short_url not in translations.keys():
        abort(404, message=f"URL {BASE_DOMAIN}{short_url} doesn't exist")
        
        
def abort_if_translation_exists(short_url):
    if short_url in translations.keys():
        abort(409, message=f"URL {BASE_DOMAIN}{short_url} already exists")
    
    
class UrlTranslations(Resource):
    @marshal_with(translation_resource_fields) # Serialize it to json format 
    def get(self, short_url):
        abort_if_translation_doesnt_exist(short_url)
        return translations[short_url]

    @marshal_with(translation_resource_fields)
    def put(self, short_url):
        abort_if_translation_exists(short_url)
        args = translation_put_args.parse_args()
        translations[short_url] = args
        return translations[short_url], 201
    
    @marshal_with(translation_resource_fields)
    def delete(self, short_url):
        abort_if_translation_doesnt_exist(short_url)
        del translations[short_url]
        return '', 204



class GetUserURLs(Resource):
    # @marshal_with(translation_resource_fields) # Serialize it to json format 
    def get(self, user_id):
        user_urls = dict()
        for value in translations.values():
            print(value)
            if value['user_id'] == user_id:
                user_urls[value['short_url']] = value
        # if len(user_urls) == 0:
        #     return ""
        print(user_urls)
        return jsonify(user_urls)

api.add_resource(UrlTranslations, "/translate/<string:short_url>")
api.add_resource(GetUserURLs, "/get_user_urls/<string:user_id>")

if __name__ == "__main__":
    app.run(debug=True)
    
    