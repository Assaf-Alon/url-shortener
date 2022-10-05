# Imports
from flask import Flask, jsonify
from flask_restful import Resource, reqparse
# from flask_sqlalchemy import SQLAlchemy, Table, Column

# import sqlalchemy
from sqlalchemy import exc, create_engine

import app_utils

USER_TABLE  = "user_tbl"
VERBOSE = False

user_args = reqparse.RequestParser()
user_args.add_argument("user_id",  type=str, help="The username")
user_args.add_argument("password", type=str, help="The passowrd of the user")
user_args.add_argument("email",    type=str, help="The user's email address")

# REST API methods for the user page
class User(Resource):
    def get(self, user_id):
        args = user_args.parse_args()
        engine = create_engine('sqlite:///database.db')
        if "user_id" == "Anonymous":
            return jsonify({"message": "Anonymous login permitted",
                            "success": True})
        
        output = None
        with engine.connect() as con:
            sql_query = f"SELECT * FROM {USER_TABLE} WHERE user_id = \"{user_id}\";"
            output = con.execute(sql_query)
            output = [dict(row) for row in output]
            if VERBOSE:
                print(f"[VERBOSE] Ran SQL query: {sql_query}")
                print(f"[VERBOSE] SQL query output: {output}")
            if (len(output) == 0):
                return {"message": "username not found",
                        "success": False}, 404
            
            
            output = output[0]
            if args['password'] == output['password']:
                return {"message": f"{user_id} login permitted",
                        "success": True}, 200
            
            
            if args['password'] == None:
                return {"message": "Password not specified",
                                "success": False}, 403
            
            
            return {"message": "Invalid password",
                    "success": False}, 403
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
        engine = create_engine('sqlite:///database.db')
        with engine.connect() as con:
            con.execute(f"DELETE FROM {USER_TABLE} WHERE user_id = \"{user_id}\";")
            # TODO - Check it's deleted
        return '', 204
    
