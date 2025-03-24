from flask import Flask, render_template, request

import sqlite3


app = Flask(__name__)

if __name__ == '__main__':
    app.run()

@app.route("/")
def index():
    return render_template('login.html')

@app.route("/signuppage")
def signuppage():
    return render_template('signup.html')

@app.route("/loginpage")
def loginpage():
    return render_template('login.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        if not email or not password:
            errorMessage = "Ensure email and password fields are filled"
            return render_template('login.html', errorMessage=errorMessage)
        else:
            #database auth
            return

    return render_template('login.html')