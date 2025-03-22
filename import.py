import sqlite3
import csv
from hashlib import sha256


connection = sqlite3.connect("nittanybusiness.db")
cursor = connection.cursor()

print("Importing data into \"nittanybusiness.db\"")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        userID TEXT PRIMARY KEY,
        passwordHash TEXT
    );""")


with open("./data/Users.csv", newline='') as f:
    reader = csv.reader(f)
    
    title = True
    for row in reader:
        if title:
            title = False
            continue
        userID = row[0]
        passwordHash = sha256(bytes(row[1], "utf-8")).hexdigest()\
            
        cursor.execute(f"""
            INSERT INTO users VALUES ('{userID}', '{passwordHash}');
        """)

    connection.commit()

