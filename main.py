from flask import Flask, render_template, session, request, redirect, url_for, g

import csv
import sqlite3
from hashlib import sha256
import re

from numpy import error_message

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

    # Check that all inputs are valid.
    existing_user, invalid_fields = verify_inputs(request.form)

    if existing_user or invalid_fields:
        return render_template('signup.html', existingUser=existing_user, invalidFields=invalid_fields)
    
    # After this point, all inputs are valid.
    # TODO: Insert data into database.
    match account_type:
        case 'seller':
            query_db('''
                    INSERT INTO seller VALUES (?, ?, ?, ?, )
            ''')

    return redirect(url_for('login'))

def verify_inputs(inputs):

    invalid_fields = []

    if query_db('''
            SELECT 1 FROM users WHERE email=?;
            ''', (inputs['email'],), one=True):
        existing_user = True
    else:
        existing_user = False

    if not re.fullmatch('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+', inputs['email']):
        invalid_fields.append('Email')
    
    if not re.fullmatch('^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*[0-9]).{8,60}$', inputs['password']):
        invalid_fields.append('Password')

    match inputs['accountType']
    case 'seller':
        if not re.fullmatch('^[0-9]{3,6}$', inputs['addressZip']):
            invalid_fields.append('Zip Code')

        if not re.fullmatch('^[0-9]{10}$', inputs['csNum']):
            invalid_fields.append('Customer Service Number')

        if not re.fullmatch('^[0-9]{8}$', inputs['bankAccountNum']):
            invalid_fields.append('Bank Account Number')

        if not re.fullmatch('^[0-9]{9}$', inputs['bankRoutingNumber']):
            invalid_fields.append('Bank Routing Number')

        if not re.fullmatch('^[0-9]+$', inputs['bankBalance']):
            invalid_fields.append('Bank Balance')

    case 'buyer':
        if not re.fullmatch('^[0-9]{3,6}$', inputs['addressZip']):
            invalid_fields.append('Zip Code')

        if not re.fullmatch('^[0-9]{16}$', inputs['cardNumber']):
            invalid_fields.append('Card Number')

        if not re.fullmatch('^[0-9]{2,4}$', inputs['cardSecurityCode']):
            invalid_fields.append('Card Security Code')
    
    return existing_user, invalid_fields


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

def valid_user(email, password):
    hashed_password = sha256(bytes(password, 'utf-8')).hexdigest()
    if query_db('''
                SELECT 1 FROM user WHERE email=? AND passwordHash=?;
                ''', (email, hashed_password), one=True):
        return True
    return False


@app.route('/logout', methods=['POST', 'GET'])
def logout():
    # checks if email is in session, if is then pop (remove from session) which logs out
    if 'email' in session:
        session.pop('email', None)
        print('Logged out')
    return redirect(url_for('login'))


@app.route('/search')
def search():
    '''if 'email' not in session:
        return redirect(url_for('login'))
    else:'''
    return render_template('search.html')

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



# Helper functions for simpler DB querying
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
