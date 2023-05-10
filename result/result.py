from flask import request,render_template,Blueprint,current_app
from db.db import get_diagnosis
from checker.checker import check__logged_in
import json

result = Blueprint('result',__name__,template_folder='templates',static_folder='static')





@result.route('/result',methods=['GET', 'POST'])
@check__logged_in
def show_result():
    symptoms = request.form.getlist('symptoms_input')
    symptoms_json = json.loads(symptoms[0])
    symptoms = [symptoms_json[1]]
    diagnosis_result = get_diagnosis(symptoms)
    return render_template('result/result.html', the_result=diagnosis_result)


