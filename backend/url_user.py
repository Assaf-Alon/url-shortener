# Imports
from flask import Flask, jsonify
from flask_restful import Resource, reqparse
# from flask_sqlalchemy import SQLAlchemy, Table, Column

# import sqlalchemy
from sqlalchemy import exc, create_engine

import app_utils

USER_TABLE  = "user_tbl"

user_args = reqparse.RequestParser()
user_args.add_argument("user_id",  type=str, help="The username")
user_args.add_argument("password", type=str, help="The passowrd of the user")
user_args.add_argument("email",    type=str, help="The user's email address")

# REST API methods for the user page
class User(Resource):
    def get(self, user_id):
        engine = create_engine('sqlite:///database.db')
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
        engine = create_engine('sqlite:///database.db')
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