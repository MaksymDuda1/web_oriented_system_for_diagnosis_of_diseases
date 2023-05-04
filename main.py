import json
from checker import check__logged_in
from flask import Flask, render_template, request, session,redirect
from db import UseDatabase
app = Flask(__name__)


app.secret_key = 'Deodorantstick1'


app.config['dbconfig'] = {'host': '127.0.0.1',
            'user': 'root',
            'password': 'Deodorantstick1',
            'database': 'diagnosis1', }


def get_diagnosis(symptoms):
    with  UseDatabase(app.config['dbconfig']) as cursor:
            placeholders = ', '.join(['%s'] * len(symptoms))
            query = """SELECT disease.name v
            FROM disease
            JOIN disease_symptoms ON disease.disease_id = disease_symptoms.disease_id
            JOIN symptoms ON symptoms.symptoms_id = disease_symptoms.symptoms_id
            WHERE symptoms.name IN ({})""".format(placeholders)
            cursor.execute(query, tuple(symptoms))
            results = cursor.fetchall()
    return results


@app.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template('index.html')


@app.route('/login',methods=['GET','POST'])
def loggining():
    if request.method == 'POST':
        session['logged_in'] = True
        return redirect('/')
    return render_template('login.html', the_title='Login')


@app.route('/registration',methods=['GET','POST'])
def registration():
    if request.method == 'POST':
        session['logged_in'] = True
        return redirect('/')
    return render_template('registration.html', the_title="registration")


@app.route('/logout')
def do_logout():
    session.pop('logged_in')
    if 'logged_in' not in session:
        return redirect('/login')


@app.route('/diagnosis', methods=['GET', 'POST'])
def diagnosis():
    return render_template('diagnosis.html')


@app.route('/result', methods=['GET','POST'])
@check__logged_in
def result():
    symptoms = request.form.getlist('symptoms_input')
    symptoms_json = json.loads(symptoms[0])
    symptoms = [symptoms_json[1]]
    diagnosis_result = get_diagnosis(symptoms)
    return render_template('result.html', the_result=diagnosis_result)
    
@app.route('/checker')
def do_check():
    if 'logged_in' in session:
        return 'Youre logged in'
    elif 'logged_in' not in session:
        return 'Yooure not logged in'
    return str(request.method)


if __name__ == '__main__':
    app.run(debug=True)
