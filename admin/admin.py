from flask import Blueprint, render_template,request,jsonify
from db.db import show_users,do_user_update_admin,do_user_delete,insertData,get_email,show_diseases#do_disease_update_admin


admin = Blueprint('admin', __name__,template_folder='templates')

@admin.route('/admin')
def show_main_page():
    return render_template('admin/home.html')


@admin.route('/users')
def do_users():
    users = show_users()
    return render_template('admin/users_page.html', users=users)
@admin.route('/update_users', methods=['POST'])
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        birthday = request.form['birthday']
        gender = request.form['gender']
        role = request.form['role']
        msg = do_user_update_admin(name,email,birthday,gender,role)
    return jsonify(msg)

@admin.route('/delete_users',methods =['POST'])
def delete_user():
    if request.method == 'POST':
        email = request.form.get('email')
        msg = do_user_delete(email)

        return msg

@admin.route('/add_users', methods=['POST'])
def add_user():
    if request.method == "POST":
        result = get_email(request)
        if result:
            msg = "Email already exists"
            return jsonify(msg)
        else:
            data = insertData(request, None)
            if data:
                msg = "User added successfully"
                return jsonify(msg)


@admin.route('/diseases')
def do_diseases():
     diseases = show_diseases()
     return render_template('admin/diseases_page.html',diseases = diseases)


# @admin.route('/update_diseases')
# def update_disease():
#     if request.method == "POST":
#         disease = request.form['disease']
#         description = request.form['description']
#         treatment = request.form['treatment']
#         symptoms = request.form['symptoms']
#         multiplier = request.form['multiplier']
#         msg = do_disease_update_admin(disease, description, treatment, symptoms, multiplier)
#     return jsonify(msg)

