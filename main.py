from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, SelectMultipleField, StringField, PasswordField, validators, RadioField, SelectField, \
    ValidationError, FileField, SubmitField, TextAreaField, DateField
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
    role = StringField('Role: ', [validators.DataRequired()])


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

class AddStudent(Form):
    name = StringField('Enter Full Name')
    squad = SelectField('Squad', choices=[('A', 'Alpha'), ('B', 'Bravo'), ('C', 'Charlie'), ('D', 'Delta'), ('E', 'Echo'), ('F', 'Foxtrot')])
    slevel = RadioField('Level', choices=[('Sec 1', 'Sec 1'), ('Sec 2', 'Sec 2'), ('Sec 3', 'Sec 3'), ('Sec 4', 'Sec 4'), ('Sec 5', 'Sec 5')])
    l1class = RadioField('Level', choices=[('1E1', '1E1'), ('1E2', '1E2'), ('1E3', '1E3'), ('1E4', '1E4'),
                                         ('1N1', '1N1'), ('1N2', '1N2'), ('1N3', '1N3'), ('1N4', '1N4'), ('1T1', '1T1') ])
    l2class = RadioField('Level', choices=[('2E1', '2E1'), ('2E2', '2E2'), ('2E3', '2E3'), ('2E4', '2E4'),
                                         ('2N1', '2N1'), ('2N2', '2N2'), ('2N3', '2N3'), ('2N4', '2N4'), ('2T1', '2T1') ])
    l3class = RadioField('Level', choices=[('3E1', '3E1'), ('2E2', '3E2'), ('3E3', '3E3'), ('3E4', '3E4'),
                                           ('3N1', '3N1'), ('3N2', '3N2'), ('3N3', '3N3'), ('3N4', '3N4'),
                                           ('3T1', '3T1')])
    l4class = RadioField('Level', choices=[('4E1', '4E1'), ('4E2', '4E2'), ('4E3', '4E3'), ('4E4', '4E4'),
                                           ('4N1', '4N1'), ('4N2', '4N2'), ('4N3', '4N3'), ('4N4', '4N4'),
                                           ('4T1', '4T1')])
    l5class = RadioField('Level', choices=[('5N1', '5N1'), ('5N2', '5N2')])
    submit = SubmitField('Submit')


@app.route('/students', methods=['GET', 'POST'])
def students():
    form = AddStudent(request.form)
    student_db = stud_ref.get()
    totalstud = []

    for eachstud in student_db.items():
        findstudent = sClass.Students(eachstud[1]['name'],eachstud[1]['sclass'], eachstud[1]['squad'], eachstud[1]['slevel'], eachstud[1]['tempcheck'])
        totalstud.append(findstudent)

    # if request.method == 'POST':
    #     if request.form['action'] == 'Submit':
    #         if form.l1class.data != 'None':
    #             selectclass = form.l1class.data
    #         elif form.l2class.data != 'None':
    #             selectclass = form.l2class.data
    #         elif form.l3class.data != 'None':
    #             selectclass = form.l3class.data
    #         elif form.l4class.data != 'None':
    #             selectclass = form.l4class.data
    #         elif form.l5class.data != 'None':
    #             selectclass = form.l5class.data
    #
    #         student_db = root.child('students')
    #         student_db.push({
    #             'name': form.name.data,
    #             'sclass' : selectclass,
    #             'slevel' : form.slevel.data,
    #             'squad': form.squad.data,
    #             'tempcheck' : '0'
    #         })
    #         return redirect(url_for('students'))
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
    return render_template('students.html', form=form, students=totalstud)


@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    student_db = stud_ref.get()
    totalstud = []
    attendancestudlist = []

    for eachstud in student_db.items():
        attendancestudlist.append(eachstud)
        findstudent = sClass.Students(eachstud[1]['name'],eachstud[1]['sclass'], eachstud[1]['squad'], eachstud[1]['slevel'], eachstud[1]['tempcheck'])
        totalstud.append(findstudent)
    print(attendancestudlist)
    if request.method == 'POST':
        if request.form['action'] == 'Submit':
            present = request.form.getlist('check')
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
    return render_template('attendance.html', students=totalstud)

class registration:
    def __init__(self,username, password):
        self.__username = username
        self.__password = password

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    form = LoginForm(request.form)
    username = form.username.data
    role = form.role.data
    if request.method == 'POST':
        if request.form['action'] == 'Register':
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
