from flask import Flask
from authorization.login import authorization
from checker.checker import checker
from result.result import result
from diagnosis.diagnosis import diagnosis
from registration.registration import registration
from logout.logout import logout
from index.index import index
from admin.admin import admin
from user_account.user_account import user_account
from user_account.diseases_history import diseases_history



app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/images/uploads'
app.secret_key = 'Deodorantstick1'
app.config['dbconfig'] = {'host': '127.0.0.1',
            'user': 'root',
            'password': 'Deodorantstick1',
            'database': 'web_oriented_system_for_diagnosis_of_diseases', }


app.register_blueprint(index)
app.register_blueprint(authorization)
app.register_blueprint(registration)
app.register_blueprint(checker)
app.register_blueprint(diagnosis)
app.register_blueprint(result)
app.register_blueprint(logout)
app.register_blueprint(admin)
app.register_blueprint(user_account)
app.register_blueprint(diseases_history)


if __name__ == '__main__':
    app.run(debug=True)
