from flask import render_template,Blueprint
from db.db import get_symptoms
diagnosis = Blueprint('diagnosis',__name__,template_folder='templates')

@diagnosis.route('/diagnosis')
def diagnosis_page():
    symptoms = get_symptoms()
    return render_template('diagnosis/diagnosis.html',symptoms =symptoms)

@diagnosis.route('/get_symptoms')
def get_symptom():
    return get_symptoms()


