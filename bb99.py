from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, SelectMultipleField, StringField, PasswordField, validators, RadioField, SelectField, \
    ValidationError, FileField, SubmitField, TextAreaField, DateField
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate('cred/bb99-a73bb-firebase-adminsdk-lmv85-534444e884.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://bb99-a73bb.firebaseio.com/'
})

root = db.reference()
user_ref = db.reference('userbase')
stud = db.reference('students')

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
                session['logged_in'] = True
                session['id'] = username

                return redirect(url_for('home'))
            else:
                flash('Login is not valid!', 'danger')
        return render_template('index.html', form=form)
    return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

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
    squad = SelectField('Squad', choices=[('a', 'Alpha'), ('b', 'Bravo'), ('c', 'Charlie'), ('d', 'Delta'), ('e', 'Echo'), ('f', 'Foxtrot')])
    slevel = RadioField('Level', choices=[('1', 'Sec1'), ('2', 'Sec 2'), ('3', 'Sec 3'), ('4', 'Sec 4'), ('5', 'Sec 5')])
    l1class = RadioField('Level', choices=[('1e1', '1E1'), ('1e2', '!E2'), ('1e3', '1E3'), ('1e4', '1E4'),
                                         ('1n1', '1N1'), ('1n2', '1N2'), ('1n3', '1N3'), ('1n4', '1N4'), ('1t1', '1T1') ])
    # l2class =
    # l3class =
    # l4class =
    # l5class =
    submit = SubmitField('Submit')

@app.route('/students', methods=['GET', 'POST'])
def students():
    form = AddStudent(request.form)
    if request.method == 'POST':
        if request.form['action'] == 'Submit':
            student_db = root.child('students')
            student_db.push({
                'name': form.name.data,
                'squad': form.squad.data,
            })
    return render_template('students.html', form=form)


if __name__ == '__main__':
    app.run()
