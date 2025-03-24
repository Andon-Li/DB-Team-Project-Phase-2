from flask import Flask, render_template, request

import sqlite3


app = Flask(__name__)

if __name__ == '__main__':
    app.run()

@app.route("/")
def index():
    return render_template('login.html')

