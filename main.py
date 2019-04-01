from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mysqldb import MySQL
from wtforms import Form, SelectMultipleField, StringField, PasswordField, validators, RadioField, SelectField, ValidationError, FileField, SubmitField, TextAreaField, DateField
import xlrd
import os
from werkzeug.utils import secure_filename
import datetime
import models


app = Flask(__name__)
app.config['SECRET KEY'] = 'secret123'
app.secret_key = 'secret123'
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

# Setup Database
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = '1234'
# app.config['MYSQL_DB'] = 'bb99'

# deployment database
app.config['MYSQL_HOST'] = 'Albert481.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = 'Albert481'
app.config['MYSQL_PASSWORD'] = 'qazwsxplm123'
app.config['MYSQL_DB'] = 'Albert481$bb99'

mysql = MySQL(app)



class LoginForm(Form):
    username = StringField('Username:', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm(request.form)

    if request.method == 'POST':
        username = form.username.data
        password = form.password.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE user_name=%s", [username])
        data = cur.fetchall()

        try:
            if (username == data[0][1]) and (password == data[0][3]):
                session['user_data'] = data[0]
                session['role'] = data[0][2]
                session['logged_in'] = True
                session['id'] = [0][0]
                cur.close()
                return redirect(url_for('index'))

            else:
                flash('Login failed: Incorrect username or password', 'danger')
                return render_template('index.html', form=form)

        except:
            flash('Login failed: Incorrect username or password', 'danger')
            return render_template('index.html', form=form)


    return render_template('index.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    flash('You are now logged out', 'success')
    return redirect(url_for('index'))


@app.route('/students', methods=['GET', 'POST'])
def students():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM students")
    data = cur.fetchall()

    totalStud = []

    for eachstud in data:
        # Student Class (studId, studClass, studName, studSquad
        findstudent = models.Students(eachstud[0], eachstud[1], eachstud[2], eachstud[3])
        totalStud.append(findstudent)



    # if request.method == 'POST':
    #     if request.form['action'] == 'Save':
    #         try:
    #             f = request.files['upload']
    #             f.save(secure_filename(f.filename))
    #             flash('File saved', 'success')
    #         except OSError:
    #             flash('Please upload a file named: 99th_Coy_Nominal_Roll in .xlsx format', 'danger')
    #
    #     if request.form['action'] == 'Load Excel':
    #         try:
    #             wb = xlrd.open_workbook("99th_Coy_Nominal_Roll.xlsx")
    #             # Read first sheet
    #             worksheet = wb.sheet_by_index(0)
    #             total_cols = worksheet.ncols
    #             table = list()
    #             record = list()
    #             # Reads data from excel sheet
    #             for i in range(1, worksheet.nrows):
    #                 for j in range(total_cols):
    #                     record.append(worksheet.cell(i, j).value)
    #                 table.append(record)
    #                 record = []
    #                 i += 1
    #             # Reads the excel and assign appropriate values
    #             student_db = root.child('students')
    #             student_db.delete()
    #             for i in table:
    #                 name = i[3]
    #                 sclass = i[4]
    #                 slevel = i[8]
    #                 squad = i[7]
    #                 student_db.push({
    #                     'name': name,
    #                     'sclass': sclass,
    #                     'slevel': slevel,
    #                     'squad': squad,
    #                     'tempcheck': '0',
    #                     'infraction': 0
    #                 })
    #             return redirect(url_for('students'))
    #         except OSError:
    #             flash('99th_Coy_Nominal_Roll.xlsx cannot be found', 'danger')
    cur.close()
    return render_template('students.html', students=totalStud)


@app.route('/attendance', methods=['GET', 'POST'])
def attendance():
    now = datetime.datetime.now()
    datenow = now.strftime("%d-%m-%Y")
    totalstud = []

    presentStrength = 0
    totalStrength = 0

    cur = mysql.connection.cursor()

    cur.execute("SELECT COUNT(*) FROM students s JOIN attendance a ON s.student_id=a.student_id WHERE a.date=%s", [datenow])

    data = cur.fetchone()

    # If attendance has not been taken for DATENOW (today)
    if data[0] == 0:
        cur.execute("SELECT student_id, student_class, student_name, student_squad FROM students")
        data = cur.fetchall()

        for eachstud in data:
            # Attendance Class (studId, studClass, studName, studSquad, attendancy, date)
            findstudent = models.Attendance(eachstud[0], eachstud[1], eachstud[2], eachstud[3], 0,
                                            datenow)

            totalstud.append(findstudent)

    # If atendance has already been taken for DATENOW (today)
    else:
        # Admin can view ALL students and choose specific date for attendance
        if session['role'] == 'Admin':
            cur.execute(
                "SELECT s.student_id, s.student_class, s.student_name, s.student_squad, a.attendancy, a.date FROM students s LEFT JOIN attendance a ON s.student_id=a.student_id WHERE a.date=%s",
                [datenow])
        # Other users can view students assigned by their role
        else:
            cur.execute(
                "SELECT s.student_id, s.student_class, s.student_name, s.student_squad, a.attendancy, a.date FROM students s LEFT JOIN attendance a ON s.student_id=a.student_id WHERE s.student_squad=%s AND a.date=%s",
                (session['role'], datenow))

        data = cur.fetchall()

        for eachstud in data:
            # Attendance Class (studId, studClass, studName, studSquad, attendancy, date)
            findstudent = models.Attendance(eachstud[0], eachstud[1], eachstud[2], eachstud[3], eachstud[4],
                                            eachstud[5])

            totalStrength += 1
            if findstudent.get_attendancy() == 1:
                presentStrength += 1

            totalstud.append(findstudent)


    if request.method == 'POST':
        datenow = now.strftime("%d-%m-%Y")
        if request.form['action'] == 'Submit':
            present = request.form.getlist('check')
            cur = mysql.connection.cursor()

            for eachstud in range(len(totalstud)):
                if totalstud[eachstud].get_studName() in present:
                    cur.execute("INSERT INTO attendance (student_id, attendancy, date) VALUES (%s, 1, %s) ON DUPLICATE KEY UPDATE attendancy=1", (totalstud[eachstud].get_studId(), datenow))
                else:
                    cur.execute("INSERT INTO attendance (student_id, attendancy, date) VALUES (%s, 0, %s) ON DUPLICATE KEY UPDATE attendancy=0", (totalstud[eachstud].get_studId(), datenow))

            flash("Attendance Updated Successfully", 'success')
            mysql.connection.commit()
            cur.close()

        if request.form['action'] == 'Reset':
            cur = mysql.connection.cursor()
            for eachstud in range(len(totalstud)):
                cur.execute("INSERT INTO attendance (student_id, attendancy, date) VALUES (%s, 0, %s) ON DUPLICATE KEY UPDATE attendancy=0", (totalstud[eachstud].get_studId(), datenow))
            flash("Attendance Reset Successful", 'success')
            mysql.connection.commit()
        return redirect(url_for('attendance'))

    cur.close()
    return render_template('attendance.html', students=totalstud , present=presentStrength, total=totalStrength)


if __name__ == '__main__':
    app.run(port='80')
