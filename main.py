from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, SelectMultipleField, StringField, PasswordField, validators, RadioField, SelectField, ValidationError, FileField, SubmitField, TextAreaField, DateField
import firebase_admin
from firebase_admin import credentials, db, storage
import xlrd
import students as sClass

cred = credentials.Certificate('cred/bb99-a73bb-firebase-adminsdk-lmv85-534444e884.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bb99-a73bb.firebaseio.com/'
})

root = db.reference()
user_ref = db.reference('userbase')
stud_ref = db.reference('students')

app = Flask(__name__)
app.config['SECRET KEY'] = 'secret123'
app.secret_key = 'secret123'

class LoginForm(Form):
    username = StringField('Username:', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm(request.form)
    if request.method == 'POST':
        username = form.username.data
        password = form.password.data
        userbase = user_ref.get()
        for user in userbase.items():
            if user[1]['username'] == username and user[1]['password'] == password:
                session['user_data'] = user[1]
                session['role'] = user[1]['role']
                session['logged_in'] = True
                session['id'] = username
                session['admin'] = user[1]['admin']
                print(session['admin'])
                return redirect(url_for('index'))

        flash('Login is not valid!', 'danger')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


class RequiredIf(object):
    def __init__(self, *args, **kwargs):
        self.conditions = kwargs
    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)

@app.route('/students', methods=['GET', 'POST'])
def students():
    student_db = stud_ref.get()
    totalstud = []

    for eachstud in student_db.items():
        findstudent = sClass.Students(eachstud[1]['name'],eachstud[1]['sclass'], eachstud[1]['squad'], eachstud[1]['slevel'], eachstud[1]['tempcheck'])
        totalstud.append(findstudent)

        if request.method == 'POST':
            if request.form['action'] == 'Submit':
                pass
            if request.form['action'] == 'Load Excel':
                wb = xlrd.open_workbook("99th Coy Nominal Roll.xlsx")
                #Read first sheet
                worksheet = wb.sheet_by_index(0)
                total_cols = worksheet.ncols
                table = list()
                record = list()
                # Reads data from excel sheet
                for i in range(1,worksheet.nrows):
                    for j in range(total_cols):
                        record.append(worksheet.cell(i, j).value)
                    table.append(record)
                    record = []
                    i += 1
                #Reads the excel and assign appropriate values
                student_db = root.child('students')
                student_db.delete()
                for i in table:
                    name = i[3]
                    sclass =i[4]
                    slevel = i[8]
                    squad = i[7]
                    student_db.push({
                        'name': name,
                        'sclass': sclass,
                        'slevel': slevel,
                        'squad': squad,
                        'tempcheck': '0'
                    })
                return redirect(url_for('students'))
    return render_template('students.html', students=totalstud)


@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    student_db = stud_ref.get()
    totalstud = []
    attendancestudlist = []
    stotal = 0
    spresent = 0
    aList = []
    bList = []
    cList = []
    dList = []
    eList = []
    fList = []

    for eachstud in student_db.items():
        attendancestudlist.append(eachstud)
        findstudent = sClass.Students(eachstud[1]['name'],eachstud[1]['sclass'], eachstud[1]['squad'], eachstud[1]['slevel'], eachstud[1]['tempcheck'])
        if findstudent.get_tattend() == '1':
            spresent += 1
        if findstudent.get_squad()[:1] == 'A':
            aList.append(eachstud)
        elif findstudent.get_squad()[:1] == 'B':
            bList.append(eachstud)
        elif findstudent.get_squad()[:1] == 'C':
            cList.append(eachstud)
        elif findstudent.get_squad()[:1] == 'D':
            dList.append(eachstud)
        elif findstudent.get_squad()[:1] == 'E':
            eList.append(eachstud)
        elif findstudent.get_squad()[:1] == 'F':
            fList.append(eachstud)
        stotal += 1
        totalstud.append(findstudent)

    if request.method == 'POST':
        if request.form['action'] == 'Submit':
            present = request.form.getlist('check')
            if session['role'] == 'A':
                for eachstud in aList:
                    tempattendance = stud_ref.child(eachstud[0])
                    if eachstud[1]['name'] in present:
                        tempattendance.update({'tempcheck': '1'})
                    else:
                        tempattendance.update({'tempcheck': '0'})
                    print(eachstud[1]['name'])
            elif session['role'] == 'B':
                for eachstud in bList:
                    tempattendance = stud_ref.child(eachstud[0])
                    if eachstud[1]['name'] in present:
                        tempattendance.update({'tempcheck': '1'})
                    else:
                        tempattendance.update({'tempcheck': '0'})
                    print(eachstud[1]['name'])
            elif session['role'] == 'C':
                for eachstud in cList:
                    tempattendance = stud_ref.child(eachstud[0])
                    if eachstud[1]['name'] in present:
                        tempattendance.update({'tempcheck': '1'})
                    else:
                        tempattendance.update({'tempcheck': '0'})
                    print(eachstud[1]['name'])
            elif session['role'] == 'D':
                for eachstud in dList:
                    tempattendance = stud_ref.child(eachstud[0])
                    if eachstud[1]['name'] in present:
                        tempattendance.update({'tempcheck': '1'})
                    else:
                        tempattendance.update({'tempcheck': '0'})
                    print(eachstud[1]['name'])
            else:
                for eachstud in attendancestudlist:
                    tempattendance = stud_ref.child(eachstud[0])
                    if eachstud[1]['name'] in present:
                        tempattendance.update({'tempcheck': '1'})
                    else:
                        tempattendance.update({'tempcheck': '0'})
                    print(eachstud[1]['name'])

        elif request.form['action'] == 'Reset':
            for eachstud in student_db.items():
                tempattendance = stud_ref.child(eachstud[0])
                tempattendance.update({'tempcheck': '0'})

        return redirect(url_for('attendance'))
    return render_template('attendance.html', students=totalstud, present=spresent, total=stotal)

def validate_registration(form, field):
    userbase = user_ref.get()
    for user in userbase.items():
        if user[1]['username'] == field.data:
            raise ValidationError('Username exists!')

class RegistrationForm(Form):
    username = StringField('Username:', [validators.DataRequired(), validate_registration])
    role = StringField('Role: ', [validators.DataRequired()])

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = RegistrationForm(request.form)
    username = form.username.data
    role = form.role.data
    print('c')
    if request.method == 'POST' and form.validate():
        print('a')
        if request.form['action'] == 'Register':
            print('b')
            user_ref.push({
                'username' : username,
                'password' : 'qwerty',
                'admin': '1',
                'role' : role.upper()
            })
        flash('Successfully registered', 'success')
        return redirect(url_for('admin'))
    return render_template('admin.html', form=form)

if __name__ == '__main__':
    app.run(port='80')
