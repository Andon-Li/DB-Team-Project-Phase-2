import sqlite3
import csv
from hashlib import sha256

cur.executescript('''
CREATE TABLE IF NOT EXISTS user (
    email           TEXT PRIMARY KEY,
    passwordHash    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS helpDesk (
    email       TEXT PRIMARY KEY,
    Position    TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES user(email)
);

CREATE TABLE IF NOT EXISTS cardInfo (
    number  TEXT PRIMARY KEY,
    type    TEXT NOT NULL,
    expDate TEXT NOT NULL
    securityCode TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS zipInfo (
    zipCode TEXT PRIMARY KEY,
    city    TEXT NOT NULL,
    state   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS buyer (
    email       TEXT PRIMARY KEY,
    street      TEXT NOT NULL,
    zipCode     TEXT NOT NULL,
    businessName    TEXT NOT NULL,
    activeStatus    INTEGER NOT NULL,
    cardNumber      TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES user(email),
    FOREIGN KEY (cardNumber) REFERENCES cardInfo(number),
    FOREIGN KEY (zipCode) REFERENCES zipInfo(zipCode)
);

CREATE TABLE IF NOT EXISTS seller (
    email       TEXT PRIMARY KEY,
    street      TEXT NOT NULL,
    zipCode     TEXT NOT NULL,
    businessName    TEXT NOT NULL,
    activeStatus    INTEGER NOT NULL,
    CSNum           TEXT NOT NULL,
    bankRoutingNum  TEXT NOT NULL,
    bankAccountNum  TEXT NOT NULL,
    bankBalance     INTEGER NOT NULL,
    FOREIGN KEY (email) REFERENCES user(email),
    FOREIGN KEY (cardNumber) REFERENCES cardInfo(number),
    FOREIGN KEY (zipCode) REFERENCES zipInfo(zipCode)
);
''')


with open('./data/Users.csv', newline='') as f:
    reader = csv.reader(f)
    reader.__next__()  # skip first line containing column titles

    for row in reader:
        email = row[0]
        passwordHash = sha256(bytes(row[1], 'utf-8')).hexdigest()
            
        cursor.execute('''
            INSERT INTO user VALUES (?, ?);
        ''', (email, passwordHash))


with open('./data/Zipcode_Info.csv', newline='') as f:
    reader = csv.reader(f)
    reader.__next__()  # skip first line containing column titles

    for row in reader:
        zipcode = row[0]
        city = row[1]
        state = row[2]
        cursor.execute('''
            INSERT INTO zipInfo VALUES (?, ?, ?);
        ''', (zipcode, city, state))


with open('./data/Helpdesk.csv', newline='') as f:
    reader = csv.reader(f)
    reader.__next__()  # skip first line containing column titles

    for row in reader:
        email = row[0]
        position = row[1]
        cursor.execute('''
            INSERT INTO helpDesk VALUES (?, ?);
        ''', (email, position))


cards = {}
with open('./data/Credit_Cards.csv', newline='') as f:
    reader = csv.reader(f)
    reader.__next__()  # skip first line containing column titles

    for row in reader:
        number = row[0]
        cardType = row[1].strip()
        expDate = f'{row[2].zfill(2)}-{row[3]}'
        securityCode = row[4]
        cards.update({row[5]: number})
        cursor.execute('''
            INSERT INTO cardInfo VALUES (?, ?, ?, ?);
        ''', (number, cardType, expDate, securityCode))


addresses = {}
with open('./data/Address.csv', newline='') as f:
    reader = csv.reader(f)
    reader.__next__()  # skip first line containing column titles

    for row in reader:
        addressID = row[0]
        zipcode = row[1]
        street_num = row[2]
        street_name = row[3]
        addresses.update({addressID: (f'{street_num} {street_name}', zipcode)})


with open('./data/Buyers.csv', newline='') as f:
    reader = csv.reader(f)
    reader.__next__()  # skip first line containing column titles

    for row in reader:
        email = row[0]
        businessName = row[1]
        addressID = row[2]
        cursor.execute('''
            INSERT INTO buyer VALUES (?, ?, ?, ?, ?, ?)
        ''', (email, addresses[addressID][0], addresses[addressID][1], businessName, 1, cards[email]))


with open('./data/Sellers.csv', newline='') as f:
    reader = csv.reader(f)
    reader.__next__()  # skip first line containing column titles

    for row in reader:
        email = row[0]
        businessName = row[1]
        addressID = row[2]
        bankRoutingNum = row[3]
        bankAccountNum = row[4]
        bankBalance = row[5]
        cursor.execute('''
            INSERT INTO seller VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (email, addresses[addressID][0], addresses[addressID][1], businessName, 1, 
                    '000-000-0000', bankRoutingNum, bankAccountNum, bankBalance))  # No CSNum is provided in csv data.

connection.commit()
