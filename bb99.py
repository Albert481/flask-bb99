from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, SelectMultipleField, StringField, PasswordField, validators, RadioField, SelectField, \
    ValidationError, FileField, SubmitField, TextAreaField, DateField
import firebase_admin
from firebase_admin import credentials, db, storage


app = Flask(__name__)


@app.route('/')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run()
