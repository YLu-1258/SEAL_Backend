from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from model.users import User
from model.users import GPA
from model.users import ClassReview
from model.users import Tasks
from model.users import Classes as Schedules

user_api = Blueprint('user_api', __name__,
                   url_prefix='/api/users')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(user_api)

def gpa_obj_by_username(username):
    """finds User in table matching username """
    id = User.query.filter_by(_username=username).first().id
    return GPA.query.filter_by(id=id).first()

def classReview_obj_by_username(username, className):
    """finds User in table matching username """
    id = User.query.filter_by(_username=username).first().id
    print("Class review: " + str(ClassReview.query.filter_by(userID=id, className=className).first()))
    return ClassReview.query.filter_by(userID=id, className=className).first()

def getClassReview(classReview):
    # print("ORIGINAL" + str(self.classReviews))
    #classReviews = [classReview.read() for classReview in self.classReviews]
    # print("CLASSREVIEW: " + str(classReviews))
    # print("*******")
    # print("Size: " + str(len(classReviews)))
    # print("DATABASE: " + str(ClassReview.query.all()))

    # classReview = ClassReview.query.all()
    # print("VAR: " + str(classReview[0].className))

    # print("************")
    
    # listReview = []
    
    # for i in range (len(classReview)): 
    #     user_id = str(classReview[i].id)
    #     className = str(classReview[i].className)
    #     difficulty = str(classReview[i].difficulty )
    #     hoursOfHw = str(classReview[i].hoursOfHw)
    #     daysBtwTest = str(classReview[i].daysBtwTest)
    #     memorizationlevel = str(classReview[i].memorizationLevel)
    #     comments = str(classReview[i].comments)
        
    #     review = "{user_id: " + user_id + "}"
    #     print(jsonify(review))
    #     listReview.append(review)
    
    # print("listReview: " + str(listReview))

    #variable names = column name in database
    return {
        "id": classReview.id, 
        "user_id": classReview.userID,
        "className": classReview.className, 
        "difficulty": classReview.difficulty, 
        "hoursOfHw": classReview.hoursOfHw, 
        "daysBtwTest": classReview.daysBtwTest, 
        "memorizationLevel": classReview.memorizationLevel, 
        "comments": classReview.comments, 
            }

def findId(username): 
    id = User.query.filter_by(_username=username).first().id
    return id 

def findUser(username): 
    user = User.query.filter_by(_username=username).first()
    return user

def task_obj_by_username(username):
    """finds User in table matching username """
    id = User.query.filter_by(_username=username).first().id
    return Tasks.query.filter_by(id=id).first()

def class_obj_by_username(username):
    """finds User in table matching username """
    id = User.query.filter_by(_username=username).first().id
    return Schedules.query.filter_by(id=id).first()


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
    
    class _DeleteGPA(Resource):                     # This resource aims to delete a gpa row in the db
        def delete(self):
            body = request.get_json()               # We grab our body
            username = body.get('username')         # Get the username of the user from the cookie, will process in frontend
            user = gpa_obj_by_username(username)
            if user:                                # Check if user exists
                user.delete()                       # call delete
            else:                                   # if user does not exist
                return {'message': f"unable to find GPA entries of user '{username}'"}, 210
            return user.read()
            

    class _UpdateGPA(Resource):
        def post(self):
            body = request.get_json()               # We grab our body
            username = body.get('username')         # Extract the username of the user from the frontend
            fives = int(body.get('fives'))          # get number of gpa entires for each grade
            fours = int(body.get('fours'))
            threes = int(body.get('threes'))
            twos = int(body.get('twos'))
            ones = int(body.get('ones'))
            zeroes = int(body.get('zeroes'))
            if fives < 0:                           # Error check the data recieved, make sure the values are positive numbers
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

            user = gpa_obj_by_username(username)                                                # Grab username
            if user:
                user.update(fives, fours, threes, twos, ones, zeroes)                           # Update the user entry in the database
            else:
                return {'message': f"unable to find GPA entries of user '{username}'"}, 210     # error msg
            return user.read()

    class _Authenticate(Resource):                  # Authenticates an user by checking the backend
        def post(self):
            body = request.get_json()               # grab info from frontend
            username = body.get('username')
            password = body.get('password')
            if len(username) < 1:
                return {'message': f'Invalid username'}, 210
            if len(password) < 1:
                return {'message': f'Empty Password'}, 210

            user = findUser(username)
            if user.is_password(password):          # Check if there is a password match
                return username                     # Return username if true
            return None


    class _ShowClassReview(Resource):
        def get(self):
            #original code commented out because only searched for one class review per user
            #(code below searches for all class reviews, even if one user posted many)
            #users = User.query.first()
            # json_ready = [user.showClassReview() for user in users]
            #json_ready = getClassReview()
            
            reviewList = []
            
            #get all class reviews
            classReview = ClassReview.query.all()
            #get an individual class review based on id, then add to reviewList
            for i in range (1, len(classReview) + 1): 
                review = getClassReview(ClassReview.query.filter_by(id=i).first())
                reviewList.append(review)
                #print("FOR LOOP: " + str(ClassReview.query.filter_by(id=i).first()))

            #print out reviewlist in json format
            return jsonify(reviewList)
            #return jsonify(json_ready)

    class _UpdateClassReview(Resource):
        def post(self):
            body = request.get_json()
            username = body.get('username')
            className = body.get('className')
            difficulty = int(body.get('difficulty'))
            hoursOfHw = int(body.get('hoursOfHw'))
            daysBtwTest = int(body.get('daysBtwTest'))
            memorizationLevel = int(body.get('memorizationLevel'))
            comments = body.get('comments')
            #error checking
            if difficulty < 0:
                return {'message': f'Invalid number'}, 210
            if hoursOfHw < 0:
                return {'message': f'Invalid number'}, 210
            if daysBtwTest < 0:
                return {'message': f'Invalid number'}, 210
            if memorizationLevel < 0:
                return {'message': f'Invalid number'}, 210

            #search for review based on username and classname
            user = classReview_obj_by_username(username, className)
            if user:
                user.update(className, difficulty, hoursOfHw, daysBtwTest, memorizationLevel, comments)
            else:
                return {'message': f"unable to find class review entries of user '{username}'"}, 210
            return user.read()

    class _DeleteClassReview(Resource):
        def post(self):
            body = request.get_json()
            username = body.get('username')
            className = body.get('className')

            #search for review to delete based on username and classname
            deleteClass = classReview_obj_by_username(username, className)
            print(deleteClass)
            
            
            if deleteClass:
                #NO NEED TO PASS CLASS AS ARGUMENT BECAUSE METHOD DEFAULT
                #TAKES IT IN AS self
                deleteClass.delete()
            else:
                return {'message': f"unable to find GPA entries of user '{username}'"}, 210
            return deleteClass.read()
            

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
            
            #create a review object based on user's input
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
            tasks = body.get('tasks')
            times = body.get('times')
            user = task_obj_by_username(username)
            if user:
                user.update(taskName=tasks, time=times)
            else:
                return {'message': f"unable to find user '{username}'"}, 210
            return user.read()

    class _Schedules (Resource):
        def get(self):
            users = Schedules.query.all()
            json_ready = [user.read() for user in users]
            return jsonify(json_ready)

    class _UpdateSchedules(Resource):
        def post(self):
            body = request.get_json()
            username = body.get('username')
            id = findId(username)
            per1 = body.get('per1')
            per2 = body.get('per2')
            per3 = body.get('per3')
            per4 = body.get('per4')
            per5 = body.get('per5')
            teach1 = body.get('teach1')
            teach2 = body.get('teach2')
            teach3 = body.get('teach3')
            teach4 = body.get('teach4')
            teach5 = body.get('teach5')
            user = class_obj_by_username(username)
            print(user)
            print(id)
            if user:
                user.update(id=id, per1=per1, per2=per2, per3=per3, per4=per4, per5=per5, teach1=teach1, teach2=teach2, teach3=teach3, teach4=teach4, teach5=teach5)
            else:
                return {'message': f"unable to find user '{username}'"}, 210
            return user.read()

    # building RESTapi endpoint
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')
    api.add_resource(_AverageGPA, '/gpa')
    api.add_resource(_DeleteGPA, '/gpa/delete')
    api.add_resource(_UpdateGPA, '/gpa/update')
    api.add_resource(_TotalTime, '/time')
    api.add_resource(_UpdateTasks, '/time/update')
    api.add_resource(_UpdateSchedules, '/schedules/update')
    api.add_resource(_Schedules, '/schedules')
    api.add_resource(_ShowClassReview, '/classreview')
    api.add_resource(_UpdateClassReview, '/updateclassreview')
    api.add_resource(_CreateClassReview, '/createclassreview')
    api.add_resource(_DeleteClassReview, '/deleteclassreview')
    api.add_resource(_Authenticate, '/auth')