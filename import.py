import sqlite3
import csv
from hashlib import sha256


connection = sqlite3.connect("nittanybusiness.db")
cursor = connection.cursor()


print("Importing Users.csv data the users table of nittanybusiness.db")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userID TEXT PRIMARY KEY,
        passwordHash TEXT
    );""")


with open("./data/Users.csv", newline='') as f:
    reader = csv.reader(f)
    
    reader.__next__()  # skip first line containing column titles
    for row in reader:
        userID = row[0]
        passwordHash = sha256(bytes(row[1], "utf-8")).hexdigest()
            
        cursor.execute(f"""
            INSERT INTO users VALUES ('{userID}', '{passwordHash}');
        """)

    connection.commit()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        userID TEXT PRIMARY KEY,
        cardNumber INTEGER,
        street TEXT,
        zipCode INTEGER,
        businessName TEXT,
        activeStatus INTEGER
    );""")
# activeStatus: 1 is active, 0 is inactive
