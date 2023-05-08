from flask import Blueprint,render_template, request,session,redirect,current_app
from werkzeug.security import check_password_hash
from db.db import UseDatabase
import os




authorization = Blueprint('authorization', __name__, template_folder='templates', static_folder='static')


def get_filename(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """select profile_picture from user
           where email = %s"""
        cursor.execute(_SQL, (req.form['email'],))
        filename = cursor.fetchone()[0]
        return filename


def loggining_checker(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        email = req.form['email']
        password = req.form['password']
        _SQL = """SELECT password FROM user
                     WHERE email = %s 
                  """
        cursor.execute(_SQL, (email,))
        result = cursor.fetchone()[0]
        if result is not None:
            if check_password_hash(result, password):
                session['logged_in'] = True

                filename = get_filename(request)
                if filename:
                    filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                    session['filepath'] = filepath
                return redirect('/')

        return 'wrong pass'


@authorization.route('/login',methods=['GET', 'POST'])
def authorization_page():
    if request.method == "POST":
        return loggining_checker(request)
    return render_template('authorization/login.html')
