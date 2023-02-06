from ..__init__ import login_manager, db
from ..model.users import User 
from flask_login import current_user, login_user, logout_user

def login(username, password):
    # sequence of checks
    if current_user.is_authenticated:  # return true if user is currently logged in
        return True
    elif verify_credentials(username, password):  # return true if email and password match
        user_row = user_by_username(username)
        login_user(user_row)  # sets flask login_user
        return True
    else:  # default condition is any failure
        return False

@login_manager.user_loader
def user_loader(uuid):
    """Check if user login status on each page protected by @login_required."""
    if uuid is not None:
        return User.query.get(uuid)
    return None


def verify_credentials(username, password):
    user_record = user_by_username(username)
    return user_record and User.verify_password(user_record, password)

def user_by_username(username):
    return User.query.filter_by(username=username).first()