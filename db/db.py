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
        _SQL = """SELECT diseases.name, symptoms.name,symptoms.multiplier
                  FROM diseases
                  JOIN diseases_symptoms ON diseases.disease_id = diseases_symptoms.disease_id
                  JOIN symptoms ON symptoms.symptom_id = diseases_symptoms.symptom_id;
               """
        cursor.execute(_SQL)
        diseases = cursor.fetchall()
        return diseases

def get_filename(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """select profile_picture from users
           where email = %s"""
        cursor.execute(_SQL, (req.form['email'],))
        filename = cursor.fetchone()[0]
        return filename


def get_disease_filename(name):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL ="""select disease_picture from diseases
            where name = %s"""
        cursor.execute(_SQL,(name,))
        filename = cursor.fetchone()[0]
        return filename

def get_login_data(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        email = req.form['email']
        password = req.form['password']
        _SQL = """SELECT password, role FROM users
                  WHERE email = %s"""
        cursor.execute(_SQL, (email,))
        row = cursor.fetchone()
        if row:
            hashed_password = row[0]
            role = row[1]
            return password, hashed_password, role,email
        return None, None, None,None



def get_diagnose(symptoms):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        placeholders = ', '.join(['%s'] * len(symptoms))
        query = """SELECT diseases.name, diseases.disease_id
                   FROM diseases
                   JOIN diseases_symptoms ON diseases.disease_id = diseases_symptoms.disease_id
                   JOIN symptoms ON symptoms.symptom_id = diseases_symptoms.symptom_id
                   WHERE symptoms.name IN ({})""".format(placeholders)
        cursor.execute(query, list(symptoms))  # Convert tuple to list
        row = cursor.fetchall()
        if row:
            results, disease_id = row[0][0], row[0][1]
        else:
            results, disease_id = None, None

    return results, disease_id



def get_desc(disease):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL="""select description from diseases
             where name = %s"""
        cursor.execute(_SQL,(disease,))
        desc = cursor.fetchall()
        return desc

def get_treatment(disease):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT treatment FROM diseases WHERE name = %s"""
        cursor.execute(_SQL, (disease,))
        treatment = cursor.fetchone()
        if treatment:
            return treatment[0]
        else:
            return None


def get_treatment(disease):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT treatment FROM diseases WHERE name = %s"""
        cursor.execute(_SQL, (disease,))
        treatment = cursor.fetchone()
        if treatment:
            return treatment[0]
        else:
            return None

def get_email(req):
 with UseDatabase(current_app.config['dbconfig']) as cursor:
        email = req.form['email']
        _SQL = """select email from users
                  where email = %s
               """
        cursor.execute(_SQL, (email,))
        result = cursor.fetchone()
        return result

def get_symptom(req):
 with UseDatabase(current_app.config['dbconfig']) as cursor:
        name = req.form['symptom']
        _SQL = """select name from symptoms
                  where name = %s
               """
        cursor.execute(_SQL, (name,))
        result = cursor.fetchone()
        return result




def insertData(req,file):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        password = req.form['password']
        session['email'] = req.form['email']
        hashed_password = generate_password_hash(password)
        _SQL = """insert into users
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

def insert_symptom_data(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        symptom = req.form['symptom']
        multiplier = req.form['multiplier']
        _SQL = """insert into symptoms
           (name,multiplier)
           values
           (%s, %s)
           """
        cursor.execute(_SQL,(symptom,multiplier))

def show_users():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute("SELECT * FROM users ORDER BY user_id")
        users = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        users = [dict(zip(column_names, user)) for user in users]
        return users
def show_diseases_history(user_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT diseases.name, DATE(users_diseases.arrival_date) AS arrival_date 
                    FROM diseases
                    JOIN users_diseases ON diseases.disease_id = users_diseases.disease_id
                    JOIN users ON users_diseases.user_id = users.user_id
                    WHERE users.user_id = %s
                    ORDER BY arrival_date DESC"""
        cursor.execute(_SQL, (user_id,))
        diseases = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        diseases = [dict(zip(column_names, disease)) for disease in diseases]
        return diseases


def get_user(id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "SELECT * FROM users WHERE user_id = %s"
        cursor.execute(_SQL, (id,))
        user_data = cursor.fetchone()
        if user_data:
            column_names = [desc[0] for desc in cursor.description]
            user_data = dict(zip(column_names, user_data))
        return user_data

def get_id(email):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "SELECT user_id FROM users WHERE email = %s"
        cursor.execute(_SQL, (email,))
        user_id = cursor.fetchone()
        return user_id

def do_user_update_admin(name,email,birthday,gender,role):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL ="""Update users 
        set name = %s,birthday = %s,gender = %s,role=%s
        where email = %s"""
        cursor.execute(_SQL,(name,birthday,gender,role,email))
        msg = 'Record successfully Updated'
        return msg


def do_symptom_update(req):

    with UseDatabase(current_app.config['dbconfig']) as cursor:
        name = req.form['symptom']
        multiplier = req.form['multiplier']
        id = get_symptom_id(name)
        _SQL ="""Update symptoms 
        set name = %s, multiplier = %s
        where name = %s"""
        cursor.execute(_SQL, (name,multiplier,name,))
        msg = 'Record successfully Updated'
        return msg

def delete_from_disease_symptom(disease_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """delete from diseases_symptoms
        where disease_id = %s"""
        cursor.execute(_SQL, (disease_id,))

def insert_into_diseases_symptoms(disease_id, symptom_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """insert into diseases_symptoms 
                  (disease_id, symptom_id)
                  values (%s, %s)"""
        cursor.execute(_SQL, (disease_id, symptom_id))
        return "Disease added successfully"

def insert_into_diseases(req):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        name = req.form['disease']
        description = req.form['description']
        treatment= req.form['treatment']
        _SQL ="""insert into diseases
            (name,description,treatment)
            values
            (%s,%s,%s)"""
        cursor.execute(_SQL,(name,description,treatment))
        cursor.fetchall()

def update_disease_symptom(disease_id, symptom_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """insert into diseases_symptoms
            (disease_id,symptom_id)
            values
            (%s,%s)"""
        cursor.execute(_SQL, (disease_id,symptom_id))
        return 'Updated successfully'




def do_disease_update(name,description,treatment):
    do_disease_symptom_delete(name)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """Update diseases
        set name = %s, description = %s,treatment = %s
        where name = %s"""
        cursor.execute(_SQL, (name, description, treatment,name))
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
        UPDATE users
        SET name = %s, email = %s, birthday = %s, gender = %s, password = %s
        WHERE user_id = %s
        """
        cursor.execute(_SQL, (name, email, birthday, gender, hashed_password, user_id))  # Convert to tuple

        msg = 'Record successfully updated'

    return msg



def do_user_disease_delete(email):
    id=get_id(email)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """delete from users_diseases
        where user_id = %s"""
        cursor.execute(_SQL,(id))

def do_user_delete(email):
    do_user_disease_delete(email)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """delete from users
        where email = %s"""
        cursor.execute(_SQL,(email,))
        msg = 'User deleted successfully'
        return msg

def delete_from_user_disease(id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL ="delete from users_diseases where disease_id = %s"
        cursor.execute(_SQL,(id,))
def do_disease_delete(name):
    id = get_disease_id(name)
    delete_from_user_disease(id)
    delete_from_disease_symptom(id)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """delete from diseases
        where name = %s"""
        cursor.execute(_SQL,(name,))
        msg = 'Deleted successfully'
        return msg

def get_symptom_id(name):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """select symptom_id from symptoms 
                  where name = %s"""
        cursor.execute(_SQL, (name,))
        id_tuple = cursor.fetchone()
        if id_tuple:
            return id_tuple[0]
        return None


def get_disease_id(name):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """select disease_id from diseases 
                  where name = %s"""
        cursor.execute(_SQL, (name,))
        id_tuple = cursor.fetchone()
        if id_tuple:
            return id_tuple[0]
        return None
def do_disease_symptom_delete(name):
    id = get_symptom_id(name)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """delete from diseases_symptoms
        where symptom_id = %s"""
        cursor.execute(_SQL, (id,))


def do_symptom_delete(name):
    do_disease_symptom_delete(name)
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """delete from symptoms
        where name = %s"""
        cursor.execute(_SQL,(name,))
        msg = 'Deleted successfully'
        return msg

def do_user_add(name,email,birthday,gender,password,role):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """insert into users
        (name,email,birthday,gender,password,role)
        values
        (%s,%s,%s,%s,%s,%s)"""
        cursor.execute(_SQL, (name,email,birthday,gender,password,role))
        msg = 'User added successfully'
        return msg


def update_picture(filename,user_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL="""update users
        set profile_picture = %s
        where user_id = %s"""
        cursor.execute(_SQL,(filename,user_id))
        msg = 'profile photo updated successfully'
        return msg
def save_disease_picture(filename, disease_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """
        UPDATE diseases
        SET disease_picture = %s
        WHERE disease_id = %s
        """
        cursor.execute(_SQL, (filename, disease_id))
        msg = 'Disease picture updated successfully'
        return msg
def get_symptoms():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL ="""select name from symptoms"""
        cursor.execute(_SQL)
        symptoms = cursor.fetchall()
        return symptoms

def insert_into_history(user_id, disease_id):
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "INSERT INTO users_diseases (user_id, disease_id) VALUES (%s, %s)"
        cursor.execute(_SQL, (user_id, disease_id))




def show_diseases():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT diseases.name, diseases.description, diseases.treatment, 
                GROUP_CONCAT(DISTINCT symptoms.name) AS symptoms,diseases.disease_picture
                FROM diseases
                JOIN diseases_symptoms ON diseases.disease_id = diseases_symptoms.disease_id
                JOIN symptoms ON diseases_symptoms.symptom_id = symptoms.symptom_id
                GROUP BY diseases.name, diseases.description, diseases.treatment,diseases.disease_picture;
                """
        cursor.execute(_SQL)
        rows = cursor.fetchall()
        column_names = [nam[0] for nam in cursor.description]
        diseases = [dict(zip(column_names, row)) for row in rows]
        return diseases

def show_symptoms():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        cursor.execute("SELECT * FROM symptoms ORDER BY symptom_id")
        symptoms = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        symptoms = [dict(zip(column_names, symptom)) for symptom in symptoms]
        return symptoms
def users_count():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL="select count(user_id) from users"
        cursor.execute(_SQL)
        result =  cursor.fetchone()
        return  result

def most_popular_disease():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT d.name, COUNT(ud.disease_id) AS disease_count
         FROM diseases AS d
        JOIN users_diseases AS ud ON ud.disease_id = d.disease_id
        GROUP BY d.name
        ORDER BY disease_count DESC
        LIMIT 1"""
        cursor.execute(_SQL)
        results = cursor.fetchall()
        if results:
            disease_name = results[0][0]
            amount = results[0][1]
            return disease_name, amount

def diagnosis_count():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = "select count(user_disease_id) from users_diseases"
        cursor.execute(_SQL)
        result = cursor.fetchone()
        return result

def last_diagnose():
    with UseDatabase(current_app.config['dbconfig']) as cursor:
        _SQL = """SELECT users.name  as u, diseases.name, GROUP_CONCAT(symptoms.name),
                 DATE(users_diseases.arrival_date) as date
                 FROM users
                 JOIN users_diseases ON users.user_id = users_diseases.user_id
                 JOIN diseases ON users_diseases.disease_id = diseases.disease_id
                 JOIN diseases_symptoms ON diseases.disease_id = diseases_symptoms.disease_id
                 JOIN symptoms ON diseases_symptoms.symptom_id = symptoms.symptom_id
                 WHERE users_diseases.user_disease_id = (
                 SELECT MAX(user_disease_id)
                 FROM users_diseases)
                 GROUP BY u, diseases.name, date
                 """
        cursor.execute(_SQL)
        data = cursor.fetchall()
        column_names = [desc[0] for desc in cursor.description]
        last_diagnosis = [dict(zip(column_names, row)) for row in data]
        return last_diagnosis





