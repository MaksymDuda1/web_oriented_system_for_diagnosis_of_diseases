from flask import session,Blueprint
from functools import wraps

checker = Blueprint('checker',__name__)

def check__logged_in(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if 'logged_in' in session:
            return func(*args,**kwargs)
        return  'you are not logged in'
    return wrapper

def check_role(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session['role'] == 'admin':
            return func(*args, **kwargs)
        return 'You are not admin'

    return wrapper