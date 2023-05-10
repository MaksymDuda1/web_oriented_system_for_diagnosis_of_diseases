from flask import session,request,render_template,redirect,Blueprint,current_app
from db.db import fetch_all_users,get_email,insertData
from werkzeug.utils import secure_filename
import os

registration = Blueprint('registration',__name__,template_folder='templates')


def registration_checker(req):

        result = get_email(req)
        if len(result) == 0:
            file = request.files['user-photo']
            filename = secure_filename(file.filename)
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
            session['filepath'] = filepath
            file.save(filepath)
            insertData(req, filename)
            session['logged_in'] = True
            return redirect('/')
        else:
            msg = "Email already exist"
            return msg


@registration.route('/registration',methods=['GET','POST'])
def registration_page():
    if request.method == 'POST':
        return registration_checker(request)
    return render_template('registration/registration.html', the_title="registration")
