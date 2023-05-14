import mysql.connector
from flask import current_app,Blueprint,session
from werkzeug.security import generate_password_hash

db = Blueprint('db',__name__)

class UseDatabase:
    def __init__(self,config):
        self.configuration = config
    def __enter__(self):
        self.conn =mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self.cursor
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()



def fetch_all_diseases():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT disease.name, symptom.name,symptom.multiplier
                  FROM disease
                  JOIN disease_symptom ON disease.disease_id = disease_symptom.disease_id
                  JOIN symptom ON symptom.symptom_id = disease_symptom.symptom_id;
               """
        cursor.execute(_SQL)
        diseases = cursor.fetchall()
        #column_names = [desc[0] for desc in cursor.description]
        #diseases = [dict(zip(column_names, disease)) for disease in diseases]
        return diseases

def get_filename(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """select profile_picture from user
           where email = %s"""
        cursor.execute(_SQL, (req.form['email'],))
        filename = cursor.fetchone()[0]
        return filename

def get_login_data(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        email = req.form['email']
        password = req.form['password']
        _SQL = """SELECT password, role FROM user
                  WHERE email = %s"""
        cursor.execute(_SQL, (email,))
        row = cursor.fetchone()
        if row:
            hashed_password = row[0]
            role = row[1]
            return password, hashed_password, role,email
        return None, None, None,None


def get_diagnosis(symptoms):
    with  UseDatabase(current_app.config['dbconfig']) as cursor:
            placeholders = ', '.join(['%s'] * len(symptoms))
            query = """SELECT disease.name 
            FROM disease
            JOIN disease_symptom ON disease.disease_id = disease_symptom.disease_id
            JOIN symptom ON symptom.symptom_id = disease_symptom.symptom_id
            WHERE symptom.name IN ({})""".format(placeholders)
            cursor.execute(query, tuple(symptoms))
            results = cursor.fetchone()[0]
    return results
def get_email(req):
 with UseDatabase(current_app.config['dbconfig']) as cursor:
        email = req.form['email']
        _SQL = """select email from user
                  where email = %s
               """
        cursor.execute(_SQL, (email,))
        result = cursor.fetchone()
        return result

def insertData(req,file):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        password = req.form['password']
        session['email'] = req.form['email']
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
        return 1

def show_users():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute("SELECT * FROM user ORDER BY user_id")
        users = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        users = [dict(zip(column_names, user)) for user in users]
        return users


def get_user(id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "SELECT * FROM user WHERE user_id = %s"
        cursor.execute(_SQL, (id,))
        user_data = cursor.fetchone()
        if user_data:
            column_names = [desc[0] for desc in cursor.description]
            user_data = dict(zip(column_names, user_data))
        return user_data

def get_id(email):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "SELECT user_id FROM user WHERE email = %s"
        cursor.execute(_SQL, (email,))
        user_id = cursor.fetchone()
        return user_id

def do_user_update_admin(name,email,birthday,gender,role):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL ="""Update user 
        set name = %s,birthday = %s,gender = %s,role=%s
        where email = %s"""
        cursor.execute(_SQL,(name,birthday,gender,role,email))
        msg = 'Record successfully Updated'
        return msg


def do_user_update_user(req):
    user_id = ''.join(str(id) for id in session['user_id'])
    name = req.form['name']
    email = req.form['email']
    birthday = req.form['birthday']
    gender = req.form['gender']
    password = req.form['password']
    hashed_password = generate_password_hash(password)

    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """
        UPDATE user
        SET name = %s, email = %s, birthday = %s, gender = %s, password = %s
        WHERE user_id = %s
        """
        cursor.execute(_SQL, (name, email, birthday, gender, hashed_password, user_id))  # Convert to tuple

        msg = 'Record successfully updated'

    return msg




def do_user_delete(email):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """delete from user
        where email = %s"""
        cursor.execute(_SQL,(email,))
        msg = 'User deleted successfully'
        return msg
def do_user_add(name,email,birthday,gender,password,role):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """insert into user
        (name,email,birthday,gender,password,role)
        values
        (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(_SQL, (name,email,birthday,gender,password,role))
        msg = 'User added successfully'
        return msg


def update_picture(filename,user_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL="""update user
        set profile_picture = %s
        where user_id = %s"""
        cursor.execute(_SQL,(filename,user_id))
        msg = 'profile photo updated successfully'
        return msg


