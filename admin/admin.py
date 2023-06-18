from flask import Blueprint, render_template,request,jsonify
from db.db import do_symptom_update,get_symptom,do_symptom_delete,insert_symptom_data,get_symptoms,show_users,do_user_update_admin,do_user_delete,insertData,get_email,show_diseases,users_count,show_symptoms, most_popular_disease,diagnosis_count,last_diagnose
#do_disease_update_admin


admin = Blueprint('admin', __name__,template_folder='templates')

@admin.route('/admin')
def show_main_page():
    users_amount = users_count()
    disease , amount = most_popular_disease()
    diagnosis_amount = diagnosis_count()
    last = last_diagnose()
    return render_template('admin/home.html', the_users_amount=str(users_amount[0]), the_disease = disease,
                           the_disease_amount = amount,the_diagnosis_amount = diagnosis_amount[0] ,last = last)


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


@admin.route('/symptoms')
def do_symptoms():
    symptoms = show_symptoms()
    return render_template('admin/symptoms_page.html', symptoms=symptoms)


@admin.route('/add_symptoms', methods=['POST'])
def add_symptom():
    if request.method == "POST":
        name = request.form['symptom']
        result = get_symptom(request)
        if result:
            msg = "Symptom already exists"
            return jsonify(msg)
        else:
            data = insert_symptom_data(request)
            if data:
                msg = "Symptom added successfully"
                return jsonify(msg)
            else:
                msg = "Failed to add symptom"
                return jsonify(msg)

    # Handle invalid requests or other conditions if needed
    msg = "Invalid request"
    return jsonify(msg)



@admin.route('/delete_symptoms',methods =['POST'])
def delete_symptom():
    if request.method == 'POST':
        symptom = request.form['symptom']
        msg = do_symptom_delete(symptom)
        return msg
@admin.route('/update_symptoms', methods=['POST'])
def update_symptom():
    if request.method == 'POST':
        name = request.form['symptom']
        multiplier = request.form['multiplier']
        msg = do_symptom_update(name,multiplier)
    return jsonify(msg)


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

