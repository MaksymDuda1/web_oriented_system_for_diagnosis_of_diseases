from flask import Blueprint, render_template,redirect,request,jsonify
from db.db import show_users,do_user_update,do_user_delete,insertData,get_email


admin = Blueprint('admin', __name__,template_folder='templates')

@admin.route('/admin')
def show_main_page():
    return render_template('admin/home.html')


@admin.route('/admin/users')
def admin_panel():
    users = show_users()
    return render_template('admin/users_page.html', users=users)


@admin.route('/update', methods=['POST'])
def update_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        birthday = request.form['birthday']
        gender = request.form['gender']
        role = request.form['role']
        msg = do_user_update(name,email,birthday,gender,role)
    return jsonify(msg)

@admin.route('/delete',methods =['POST'])
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








