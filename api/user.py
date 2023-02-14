from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime

from model.users import User
from model.users import GPA
from model.users import ClassReview
from model.users import Tasks

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

def gpa_obj_by_username(username):
    """finds User in table matching username """
    id = User.query.filter_by(_username=username).first().id
    return GPA.query.filter_by(id=id).first()

def classReview_obj_by_username(username):
    """finds User in table matching username """
    id = User.query.filter_by(_username=username).first().id
    return ClassReview.query.filter_by(id=id).first()


def tasks_obj_by_username(username):
    """finds User in table matching username """
    id = User.query.filter_by(_username=username).first().id
    return Tasks.query.filter_by(id=id).first()

def findId(username): 
    id = User.query.filter_by(_username=username).first().id
    return id 



class UserAPI:        
    class _Create(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            username = body.get('username')
            if username is None or len(username) < 2:
                return {'message': f'Username is missing, or is less than 2 characters'}, 210
            fullname = body.get('fullname')
            if fullname is None or len(fullname) < 2:
                return {'message': f'Fullname is missing, or is less than 2 characters'}, 210
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
    
    class _UpdateGPA(Resource):
        def put(self):
            body = request.get_json()
            username = body.get('username')
            fives = int(body.get('fives'))
            fours = int(body.get('fours'))
            threes = int(body.get('threes'))
            twos = int(body.get('twos'))
            ones = int(body.get('ones'))
            zeroes = int(body.get('zeroes'))
            if fives < 0:
                return {'message': f'Invalid number of fives'}, 210
            if fours < 0:
                return {'message': f'Invalid number of fours'}, 210
            if threes < 0:
                return {'message': f'Invalid number of threes'}, 210
            if twos < 0:
                return {'message': f'Invalid number of twos'}, 210
            if ones < 0:
                return {'message': f'Invalid number of ones'}, 210
            if zeroes < 0:
                return {'message': f'Invalid number of zeroes'}, 210

            user = gpa_obj_by_username(username)
            if user:
                user.update(fives, fours, threes, twos, ones, zeroes)
            else:
                return {'message': f"unable to find GPA entries of user '{username}'"}, 210
            return user.read()
    
    class _ShowClassReview(Resource):
        def get(self):
            users = User.query.all()
            json_ready = [user.showClassReview() for user in users]
            return jsonify(json_ready)

    class _UpdateClassReview(Resource):
        def put(self):
            body = request.get_json()
            username = body.get('username')
            className = body.get('className')
            difficulty = int(body.get('difficulty'))
            hoursOfHw = int(body.get('hoursOfHw'))
            daysBtwTest = int(body.get('daysBtwTest'))
            memorizationLevel = int(body.get('memorizationLevel'))
            comments = body.get('comments')
            if difficulty < 0:
                return {'message': f'Invalid number'}, 210
            if hoursOfHw < 0:
                return {'message': f'Invalid number'}, 210
            if daysBtwTest < 0:
                return {'message': f'Invalid number'}, 210
            if memorizationLevel < 0:
                return {'message': f'Invalid number'}, 210

            user = classReview_obj_by_username(username)
            if user:
                user.update(className, difficulty, hoursOfHw, daysBtwTest, memorizationLevel, comments)
            else:
                return {'message': f"unable to find GPA entries of user '{username}'"}, 210
            return user.read()

    class _CreateClassReview(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            

            username = body.get('username')
            className = body.get('className')
            difficulty = body.get('difficulty')
            hoursOfHw = body.get('hoursOfHw')
            daysBtwTest = body.get('daysBtwTest')
            memorizationLevel = body.get('memorizationLevel')
            comments = body.get('comments')
            
            if int(difficulty) < 0:
                return {'message': f'Invalid number'}, 210
            if int(hoursOfHw) < 0:
                return {'message': f'Invalid number'}, 210
            if int(daysBtwTest) < 0:
                return {'message': f'Invalid number'}, 210
            if int(memorizationLevel) < 0:
                return {'message': f'Invalid number'}, 210
            
            id = findId(username)
            
            review = ClassReview(id=id, className=className, difficulty=difficulty, hoursOfHw=hoursOfHw, daysBtwTest=daysBtwTest, memorizationLevel=memorizationLevel, comments=comments)

           
            
            #I HAVE TO CHANGE THIS VARIABLE NAME LOL
            reviews = review.create()
            if reviews:
                return jsonify(reviews.read())
            # failure returns error
            return {'message': f'Processed {username}, either a format error or duplicate'}, 210
            

    class _TotalTime(Resource):
        def get(self):
            users = User.query.all()
            json_ready = [user.total_time() for user in users]
            return jsonify(json_ready)
        
    class _UpdateTasks(Resource):
        def put(self):
            body = request.get_json()
            username = body.get('username')
            task = body.get('taskName')
            time = body.get('className')
            tasksCompleted = body.get('tasksCompleted')

            user = tasks_obj_by_username(username)
            if user:
                user.update(task, time, tasksCompleted)
            else:
                return {'message': f"unable to find task entries of user '{username}'"}, 210
            return jsonify(user.read())


    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_AverageGPA, '/gpa')
    api.add_resource(_UpdateGPA, '/gpa/update')
    api.add_resource(_TotalTime, '/time')
    api.add_resource(_ShowClassReview, '/classreview')
    api.add_resource(_UpdateClassReview, '/updateclassreview')
    api.add_resource(_CreateClassReview, '/createclassreview')