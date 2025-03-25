import csv
from flask import Flask, render_template, session, request, redirect, url_for

import sqlite3

app = Flask(__name__)
app.secret_key = b'cef9080767e2306c'

if __name__ == '__main__':
    app.run()

@app.route("/")
def index():
    if 'email' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('loginpage'))

@app.route("/signuppage")
def signup_page():
    return render_template('signup.html')

@app.route("/loginpage")
def login_page():
    return render_template('login.html')


def valid_user(email, password):
    with open('./data/Users.csv', mode='r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # debug to check specific user row of matching information
            #print("Row data:", row)
            if 'email' in row and 'password' in row:
                if row['email'] == email and row['password'] == password:
                    return True
    return False

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # check if the email or password fields are empty from the form (check again)
        if not email or not password:
            error_message = "Ensure email and password fields are filled"
            return render_template('login.html', errorMessage=error_message)

        # if the input's are valid, check if it matches a user in Users.csv
        if valid_user(email, password):
            print("Should direct to index")
            session['email'] = email
            return redirect(url_for('index'))
        else:
            # the login credentials were invalid
            error_message = "Incorrect email or password"
            print(error_message)
            return render_template('login.html', errorMessage=error_message)

    # if its a GET request then show the login form
    return render_template('login.html')

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    # checks if email is in session, if is then pop (remove from session) which logs out
    if 'email' in session:
        session.pop('email', None)
        print("Logged out")
        return redirect(url_for('login_page'))