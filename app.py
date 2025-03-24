from flask import Flask, render_template, session, request, redirect, url_for

import sqlite3


app = Flask(__name__)
app.secret_key = b'cef9080767e2306c'

connection = sqlite3.connect('nittanybusiness.db')
cursor = connection.cursor()


@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        entered_userID = request.form['username']
        entered_password = request.form['password']
        cursor.execute('''
            EXISTS(SELECT 1 FROM users WHERE)
        ''')
    return render_template('login.html')


@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run()
