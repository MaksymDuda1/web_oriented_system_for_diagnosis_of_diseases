from flask import request,render_template,Blueprint,current_app
from db.db import UseDatabase
from checker.checker import check__logged_in
import json

result = Blueprint('result',__name__,template_folder='templates',static_folder='static')

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




@result.route('/result',methods=['GET', 'POST'])
@check__logged_in
def show_result():
    symptoms = request.form.getlist('symptoms_input')
    symptoms_json = json.loads(symptoms[0])
    symptoms = [symptoms_json[1]]
    diagnosis_result = get_diagnosis(symptoms)
    return render_template('result/result.html', the_result=diagnosis_result)


