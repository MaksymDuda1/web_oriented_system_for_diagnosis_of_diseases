from flask import Blueprint,render_template,session

index = Blueprint('index',__name__,template_folder='templates')


@index.route('/',methods=['GET', 'POST'])
def main_page():
    filepath = session.get('filepath')
    return render_template('index/index.html', filepath=filepath)