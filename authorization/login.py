from flask import Blueprint,render_template, request,session,redirect,current_app
from werkzeug.security import check_password_hash
from db.db import UseDatabase,get_filename,get_login_data,get_id
import os




authorization = Blueprint('authorization', __name__, template_folder='templates', static_folder='static')


def loggining_checker(req):
    password,hashed_password,role,email = get_login_data(req)
    if hashed_password is not None and check_password_hash(hashed_password, password):
        session['logged_in'] = True
        session['email'] = email
        session['password'] = req.form['password']
        session['user_id']= get_id(email)
        filename = get_filename(req)
        if filename:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            session['filepath'] = filepath
        if "".join(role) == 'admin':
            session['role'] = "".join(role)
            return redirect('/admin')
        else:
            return redirect('/')

    else:
        return "wrong pass"


@authorization.route('/login',methods=['GET', 'POST'])
def authorization_page():
    if request.method == "POST":
        return loggining_checker(request)
    return render_template('authorization/login.html')
