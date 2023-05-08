from flask import Blueprint,redirect,session

logout = Blueprint('logout',__name__)

def do_logout():
    session.clear()
    if 'logged_in' not in session:
        return redirect('/login')

@logout.route('/logout')
def logout_page():
    return do_logout()