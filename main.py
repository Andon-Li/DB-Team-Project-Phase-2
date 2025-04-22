from flask import Flask, render_template, session, request, redirect, url_for, g

import csv
import sqlite3
from hashlib import sha256
import re


app = Flask(__name__)
app.secret_key = b'cef9080767e2306c'

if __name__ == '__main__':
    app.run()


@app.route('/')
def index():
    if 'email' in session:
        return redirect(url_for('anon_profile'))
    else:
        return redirect(url_for('login'))


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    assert(request.method == 'POST')

    # Pull out data from request.form
    email = request.form['email']
    password = request.form['password']
    account_type = request.form['account_type']  # seller, buyer, help_desk
    business_name = request.form['business_name']
    CS_num = request.form['CS_num']
    address_state = request.form['address_state']
    address_zip = request.form['address_zip']

    # Check if email is already registered. If not, display error message.
    if query_db('''
                SELECT 1 FROM users WHERE email=?;
                ''', (email,), one=True):
        return render_template('signup.html', error_message='This email has already been registered.')

    invalid_fields=[]
    error_message = 'Input(s) for '

    # Check that email and password are valid. If not, display error message.
    if not re.fullmatch('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', email):
        invalid_fields.append('email')
    
    if not re.fullmatch('^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*[0-9]).{8,60}$', password):
        invalid_fields.append('password')

    for field_name in invalid_fields:
        error_message += field_name + ' '

    error_message += 'have errors.'

    if invalid_fields:
        return render_template('signup.html', errorMessage=error_message)
    
    # At this point, all inputs are valid.
    # TODO: Insert data into database.


    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():

    # if its a GET request then show the login form
    if request.method == 'GET':
        return render_template('login.html')
    assert(request.method == 'POST')

    print(request.form)
    email = request.form['email']
    password = request.form['password']

    # check if the email or password fields are empty from the form (check again)
    if not email or not password:
        error_message = 'Ensure email and password fields are filled'
        return render_template('login.html', errorMessage=error_message)

    # if the input's are valid, check if it matches a user in Users.csv
    if valid_user(email, password):
        print('Should direct to index')
        session['email'] = email
        return redirect(url_for('index'))
    else:
        # the login credentials were invalid
        error_message = 'Incorrect email or password'
        print(error_message)
        return render_template('login.html', errorMessage=error_message)


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    # checks if email is in session, if is then pop (remove from session) which logs out
    if 'email' in session:
        session.pop('email', None)
        print('Logged out')
    return redirect(url_for('login'))


@app.route('/profile')
def anon_profile():
    if 'email' not in session:
        return redirect(url_for('login'))

    return redirect(url_for('profile', email=session['email']))


@app.route('/profile/<email>')
def profile(email):
    if 'email' not in session:
        return redirect(url_for('login'))

    return f'you are logged in with the email: {email}'


@app.route('/error')
def error():
    return render_template('error.html', errorMessage=request.args.get('errorMessage'))


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('nittanybusiness.db')
    db.row_factory = sqlite3.Row
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def valid_user(email, password):
    hashed_password = sha256(bytes(password, 'utf-8')).hexdigest()
    if query_db('''
                SELECT 1 FROM users WHERE email=? AND passwordHash=?;
                ''', (email, hashed_password), one=True):
        return True
    return False