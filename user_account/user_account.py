from flask import render_template,redirect,Blueprint,session,request,current_app
from db.db import get_user,do_user_update_user,update_picture
from werkzeug.utils import secure_filename
import os



user_account = Blueprint('user_account',__name__,template_folder='templates')

@user_account.route('/user_page')
def user_page():
    filepath = session.get('filepath')
    password = session['password']
    user_id = ''.join(str(id) for id in session['user_id'])
    user_data = get_user(user_id)
    return render_template('user_account/user_account.html', filepath=filepath,user=user_data,password = password)
@user_account.route('/update_user', methods=['POST'])
def do_user_update():
    if request.method == 'POST':
        email = request.form['email']
        checker = get_user(email)
        user_id = ''.join(str(id) for id in session['user_id'])
        if checker and checker['user_id'] != user_id:
            msg = "Email already exists"
            return msg
        else:
            result = do_user_update_user(request)
            return result
@user_account.route('/update-profile-picture',methods = ['POST'])
def do_profile_picture_update():
    user_id = ''.join(str(id) for id in session['user_id'])
    file = request.files['avatar']
    filename = secure_filename(file.filename)
    if filename:
        filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        session['filepath'] = filepath
        file.save(filepath)
        return update_picture(filename,user_id)
    return "Error: Invalid request"


