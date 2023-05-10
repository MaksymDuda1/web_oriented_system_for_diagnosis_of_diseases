import mysql.connector
from flask import current_app,Blueprint
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


def fetch_all_users():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT * FROM user"""
        cursor.execute(_SQL)
        users = cursor.fetchone()
        for row in users:
            user_id = str(row[0])
            user_name = str(row[1])
            return user_id, user_name
def fetch_all_symptoms():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """Select * from symptom"""
        cursor.execute(_SQL)
        symptoms = cursor.fetchall()
        return symptoms

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
        _SQL = """SELECT password,role FROM user
                     WHERE email = %s 
                  """
        cursor.execute(_SQL, (email,))
        row = cursor.fetchone()
        hashed_password = row[0]
        role = ''.join(row[1])
        return password,hashed_password,role

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
        result = cursor.fetchall()
        return result

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
        return 1

def show_users():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute("SELECT * FROM user ORDER BY user_id")
        users = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        users = [dict(zip(column_names, user)) for user in users]
        return users

def do_user_update(name,email,birthday,gender,role):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL ="""Update user 
        set name = %s,birthday = %s,gender = %s,role=%s
        where email = %s"""
        cursor.execute(_SQL,(name,birthday,gender,role,email))
        msg = 'Record successfully Updated'
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

