from flask import request,render_template,Blueprint,current_app,session
from db.db import get_diagnose,get_desc,get_treatment,insert_into_history, get_disease_filename
from checker.checker import check__logged_in
import json

result = Blueprint('result',__name__,template_folder='templates',static_folder='static')





@result.route('/result', methods=['GET', 'POST'])
@check__logged_in
def show_result():
    if request.method == "POST":
        symptoms = request.form.getlist('symptoms_input')
        symptoms_json = json.loads(symptoms[0])
        symptoms = [symptoms_json[0]]
        diagnosis_result, disease_id = get_diagnose(symptoms)
        if diagnosis_result:
            filename = get_disease_filename(diagnosis_result)
            user_id = ''.join(str(id) for id in session['user_id'])
            insert_into_history(user_id, disease_id)
            description = "".join(str(item) for item in get_desc(diagnosis_result))
            description = description.replace("'", "").replace("(", "").replace(")", "").replace('"', "")
            treatment = "".join(str(item) for item in get_treatment(diagnosis_result))
            treatment = treatment.replace("'", "").replace("(", "").replace(")", "").replace('"', "")
            return render_template('result/result.html', the_result=diagnosis_result, the_description=description,
                                   the_treatment=treatment, the_picture=filename)
        else:
            msg = 'Disease not found, try again'
            return render_template('diagnosis/diagnosis.html', data=msg)
    
    # Handle GET requests or other cases where the condition is not met
    return render_template('result/result.html')  # Provide an appropriate response







