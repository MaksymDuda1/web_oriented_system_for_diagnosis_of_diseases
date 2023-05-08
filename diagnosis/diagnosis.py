from flask import render_template,Blueprint

diagnosis = Blueprint('diagnosis',__name__,template_folder='templates')

@diagnosis.route('/diagnosis')
def diagnosis_page():

    return render_template('diagnosis/diagnosis.html')