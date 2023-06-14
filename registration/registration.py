from flask import session, request, render_template, redirect, Blueprint, current_app
from db.db import get_email, insertData, get_id
from werkzeug.utils import secure_filename
import os

registration = Blueprint('registration', __name__, template_folder='templates')


def registration_checker(req):
    is_used = get_email(req)
    if not is_used:
        file = req.files['user-photo']
        email = req.form['email']
        session['password'] = req.form['password']
        filename = secure_filename(file.filename)
        if filename:
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            session['filepath'] = filepath
            file.save(filepath)
        insertData(req, filename)
        session['logged_in'] = True
        session['user_id'] = get_id(email)
        return redirect('/')
    else:
        msg = "Email already exists"
        return render_template('registration/registration.html', the_title="registration", message=msg)


@registration.route('/registration', methods=['GET', 'POST'])
def registration_page():
    if request.method == 'POST':
        return registration_checker(request)
    return render_template('registration/registration.html', the_title="registration", message=None)
