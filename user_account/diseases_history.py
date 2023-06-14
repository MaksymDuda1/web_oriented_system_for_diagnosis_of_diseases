from flask import Blueprint,render_template,session
from db.db import show_diseases_history


diseases_history = Blueprint('diseases_history',__name__, template_folder="templates")


@diseases_history.route('/diseases_history')
def do_history():
    user_id = ''.join(str(id) for id in session['user_id'])
    diseases = show_diseases_history(user_id)
    return render_template('user_account/diseases_history.html',diseases = diseases )

