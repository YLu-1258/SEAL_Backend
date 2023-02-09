from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

class UserAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            username = body.get('username')
            if username is None or len(username) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            fullname = body.get('fullname')
            if username is None or len(fullname) < 2:
                return {'message': f'Name is missing, or is less than 2 characters'}, 210
            # validate grade
            grade = body.get('grade')
            if grade is None:
                return {'message': f'User ID is missing, or is less than 2 characters'}, 210
            # look for password and dob
            password = body.get('password')

            ''' #1: Key code block, setup USER OBJECT '''
            uo = User(username=username, fullname=fullname, password=password,  grade=grade)
            
            ''' Additional garbage error checking '''
            # set password if provided
            if password is not None:
                uo.set_password(password)
            # convert to date type
            
            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(user.read())
            # failure returns error
            return {'message': f'Processed {username}, either a format error or duplicate'}, 210

    class _Read(Resource):
        def get(self):
            users = User.query.all()    # read/extract all users from database
            json_ready = [user.read() for user in users]  # prepare output in json
            return jsonify(json_ready)  # jsonify creates Flask response object, more specific to APIs than json.dumps

    class _AverageGPA(Resource):
        def get(self):
            users = User.query.all()
            json_ready = [user.avg_gpa() for user in users]
            return jsonify(json_ready)

    class _TotalTime(Resource):
        def get(self):
            users = User.query.all()
            json_ready = [user.total_time() for user in users]
            return jsonify(json_ready)

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_AverageGPA, '/gpa')
    api.add_resource(_TotalTime, '/time')