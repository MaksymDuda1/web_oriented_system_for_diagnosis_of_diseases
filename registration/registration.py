from flask import session,request,render_template,redirect,Blueprint,current_app
from db.db import UseDatabase
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
import os

registration = Blueprint('registration',__name__,template_folder='templates')

def insertData(req,file):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        password = req.form['password']
        hashed_password = generate_password_hash(password)
        _SQL = """insert into user
        (name,email,gender,birthday,profile_picture,password)
        values
        (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(_SQL, (req.form['name'],
                              req.form['email'],
                              req.form['gender'],
                              req.form['birthday'],
                              file,
                              hashed_password))

def registration_checker(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        email = req.form['email']
        _SQL = """select email from user
                  where email = %s
               """
        cursor.execute(_SQL, (email,))
        result = cursor.fetchall()
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
            return 'email already exist'


@registration.route('/registration',methods=['GET','POST'])
def registration_page():
    if request.method == 'POST':
        return registration_checker(request)
    return render_template('registration/registration.html', the_title="registration")
