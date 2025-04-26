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

    inputs = request.form

    # Check certain inputs for uniqueness.
    non_unique_fields = unique_check(inputs)

    # Check certain inputs for corrent formatting.
    malformed_fields = format_check(inputs)

    if non_unique_fields or malformed_fields:
        return render_template('signup.html', nonUniqueFields=non_unique_fields, malformedFields=malformed_fields)
    
    # After this point, all inputs are valid.
    
    passwordHash = sha256(bytes(inputs['password'], 'utf-8')).hexdigest()
    query_db('''
                INSERT INTO user VALUES (?, ?);
            ''', (inputs['email'], passwordHash), commit=True)

    match inputs['accountType']:
        case 'seller':
            csN = inputs['csNum']

            query_db('''
                INSERT INTO seller VALUES (?, ?, ?, ?, ?, ?, ?);
            ''', (inputs['email'], inputs['addressStreet'], inputs['addressZip'], 
                    inputs['businessName'], 1, f'{csN[:3]}-{csN[3:6]}-{csN[6:]}', inputs['bankAccountNum']), commit=True)

            query_db('''
                INSERT INTO zipInfo VALUES (?, ?, ?)
            ''', (inputs['addressZip'], inputs['addressCity'], inputs['addressState']), commit=True)

            bRN = inputs['bankRoutingNum']
            
            query_db('''
                INSERT INTO bankInfo VALUES (?, ?, ?);
            ''', (inputs['bankAccountNum'], f'{bRN[:4]}-{bRN[4:8]}-{bRN[8]}', inputs['bankBalance']), commit=True)
        
        case 'buyer':
            cN = inputs['cardNum']

            query_db('''
                INSERT INTO buyer VALUES (?, ?, ?, ?, ?, ?);
            ''', (inputs['email'], inputs['addressStreet'], inputs['addressZip'], 
                    inputs['businessName'], 1, f'{cN[:4]}-{cN[4:8]}-{cN[8:12]}-{cN[12:]}'), commit=True)
            
            query_db('''
                INSERT INTO cardInfo VALUES (?, ?, ?, ?);
            ''', (f'{cN[:4]}-{cN[4:8]}-{cN[8:12]}-{cN[12:]}', inputs['cardType'], 
                    f'{inputs['cardExpMonth']}-{inputs['cardExpYear']}', 
                    inputs['cardSecurityCode']), commit=True)

            query_db('''
                INSERT INTO zipInfo VALUES (?, ?, ?)
            ''', (inputs['addressZip'], inputs['addressCity'], inputs['addressState']), commit=True)

        case 'helpDesk':
            query_db('''
                INSERT INTO helpDesk VALUES (?, ?);
            ''', (inputs['email'], inputs['position']), commit=True)

    return redirect(url_for('login'))

def unique_check(inputs):

    non_unique_fields = []
    if query_db('''
            SELECT 1 FROM user WHERE email=?;
            ''', (inputs['email'],), one=True):
        non_unique_fields.append('Email')
    
    if inputs['accountType'] == 'seller' and query_db('''
            SELECT 1 FROM bankInfo WHERE accountNum=?;
            ''', (inputs['bankAccountNum'],), one=True):
        non_unique_fields.append('Bank Account Number')

    if inputs['accountType'] == 'buyer' and query_db('''
            SELECT 1 FROM cardInfo WHERE number=?;
            ''', (f'{inputs['cardNum'][:4]}-{inputs['cardNum'][4:8]}-{inputs['cardNum'][8:12]}-{inputs['cardNum'][12:]}',), one=True):
        non_unique_fields.append('Card Number')
    
    return non_unique_fields

def format_check(inputs):

    malformed_fields = []

    if not re.fullmatch('([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(.[A-Z|a-z]{2,})+', inputs['email']):
        malformed_fields.append('Email')
    
    if not re.fullmatch('^(?=.*[A-Z])(?=.*[!@#$%^&*])(?=.*[0-9]).{8,60}$', inputs['password']):
        malformed_fields.append('Password')

    match inputs['accountType']:
        case 'seller':
            if not re.fullmatch('^[0-9]{3,6}$', inputs['addressZip']):
                malformed_fields.append('Zip Code')

            if not re.fullmatch('^[0-9]{10}$', inputs['csNum']):
                malformed_fields.append('Customer Service Number')

            if not re.fullmatch('^[0-9]{8}$', inputs['bankAccountNum']):
                malformed_fields.append('Bank Account Number')

            if not re.fullmatch('^[0-9]{9}$', inputs['bankRoutingNum']):
                malformed_fields.append('Bank Routing Number')

            if not re.fullmatch('^[0-9]+$', inputs['bankBalance']):
                malformed_fields.append('Bank Balance')

        case 'buyer':
            if not re.fullmatch('^[0-9]{3,6}$', inputs['addressZip']):
                malformed_fields.append('Zip Code')

            if not re.fullmatch('^[0-9]{16}$', inputs['cardNum']):
                malformed_fields.append('Card Number')

            if not re.fullmatch('^[0-9]{2,4}$', inputs['cardSecurityCode']):
                malformed_fields.append('Card Security Code')
    
    return malformed_fields


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


# helper function to read the categories for creation of tree
def read_categories(filepath):
    categories = []
    # open the csv and read every line from Categories.csv
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        reader.fieldnames = [field.strip() for field in reader.fieldnames]

        for row in reader:
            # append each category name and parent category to the dictionary so we can create a tree with this returned data
            categories.append(
                dict(category_name=row['category_name'].strip(), parent_category=row['parent_category'].strip()))
    return categories


# function to create the category tree hierarchy
def make_tree(categories, parent="Root"):
    tree = {}
    # iterate through the categories
    for row in categories:
        # if one of the rows in the parent_category is a parent then set the child category and recursively go through the tree
        # first iteration will be "Root", second will be first parent found, etc
        if row["parent_category"] == parent:
            category = row['category_name']
            tree[category] = make_tree(categories, parent=category)

    # return the tree
    return tree


def read_products(filepath):
    products = []
    # open the csv and read every line from Product_Listings.csv
    with open(filepath, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # append each product name, title, description, price, rating(hardcoded rn), and category to dictionary to return data
            products.append(dict(name=row['Product_Name'].strip(), title=row['Product_Title'].strip(),
                                 description=row['Product_Description'].strip(), price=row['Product_Price'].strip(),
                                 rating=5, category=row['Category'].strip()))
    return products


@app.route('/search')
def search():
    # implement this when signup is complete
    # if 'email' not in session:
    #    return redirect(url_for('login'))
    # else:

    # read the categories from the csv and make the tree based off of it
    categories = read_categories('data/Categories.csv')
    category_tree = make_tree(categories)
    # read the product listings from the csv
    products = read_products('data/Product_Listings.csv')
    # debug to see if the category tree is correct
    print("Category Tree:", category_tree)

    selected_category = request.args.get('category', '').strip()
    search_query = request.args.get('query', '').strip().lower()

    filtered_products = products
    # implement functionality for selecting a category and showing all of its products
    # if selected_category:

    # implement functionality for searching for an item
    # if search_query:

    return render_template('search.html', category_tree=category_tree, products=filtered_products,
                           selected_category=selected_category, search_query=search_query)


@app.route('/search-results')
def search_results():
    category = request.args.get('category')
    query = request.args.get('query')

    return f"Search results for '{query}' in category '{category}'"

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


def query_db(query, args=(), one=False, commit=False):
    db = get_db()
    cur = db.execute(query, args)
    if commit:
        db.commit()
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv
