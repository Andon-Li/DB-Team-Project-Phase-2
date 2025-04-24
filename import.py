import sqlite3
import csv
from hashlib import sha256

connection = sqlite3.connect('nittanybusiness.db')
cursor = connection.cursor()

cursor.executescript('''
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
    expDate TEXT NOT NULL,
    securityCode TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS bankInfo (
    accountNum  TEXT NOT NULL,
    routingNum  TEXT NOT NULL,
    balance     INTEGER NOT NULL
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
    bankAccountNum  TEXT NOT NULL,
    FOREIGN KEY (bankAccountNum) REFERENCES bankInfo(accountNum)
    FOREIGN KEY (email) REFERENCES user(email),
    FOREIGN KEY (zipCode) REFERENCES zipInfo(zipCode)
);
''')


with open('./data/Users.csv', newline='') as f:
    # email,password

    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

    for row in reader:
        passwordHash = sha256(bytes(row['password'], 'utf-8')).hexdigest()
            
        cursor.execute('''
            INSERT INTO user VALUES (?, ?);
        ''', (row['email'], passwordHash))


with open('./data/Zipcode_Info.csv', newline='') as f:
    # zipcode,city,state

    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

    for row in reader:
        cursor.execute('''
            INSERT INTO zipInfo VALUES (?, ?, ?);
        ''', (row['zipcode'], row['city'], row['state']))


with open('./data/Helpdesk.csv', newline='') as f:
    # email,Position

    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

    for row in reader:
        cursor.execute('''
            INSERT INTO helpDesk VALUES (?, ?);
        ''', (row['email'], row['Position']))


cards = {}
with open('./data/Credit_Cards.csv', newline='') as f:
    # credit_card_num,card_type,expire_month,expire_year,security_code,Owner_email

    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

    for row in reader:
        expDate = f'{row['expire_month'].zfill(2)}-{row['expire_year']}'
        cards.update({row['Owner_email']: row['credit_card_num']})
        cursor.execute('''
            INSERT INTO cardInfo VALUES (?, ?, ?, ?);
        ''', (row['credit_card_num'], row['card_type'].strip(), expDate, row['security_code']))


addresses = {}
with open('./data/Address.csv', newline='') as f:
    # address_id,zipcode,street_num,street_name

    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

    for row in reader:
        addresses.update({row['address_id']: 
                        (f'{row['street_num']} {row['street_name']}', row['zipcode'])})


with open('./data/Buyers.csv', newline='') as f:
    # email,business_name,buyer_address_id

    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

    for row in reader:
        cursor.execute('''
            INSERT INTO buyer VALUES (?, ?, ?, ?, ?, ?)
        ''', (row['email'], addresses[row['buyer_address_id']][0], addresses[row['buyer_address_id']][1], 
                row['business_name'], 1, cards[row['email']]))


with open('./data/Sellers.csv', newline='') as f:
    # email,business_name,Business_Address_ID,bank_routing_number,bank_account_number,balance
    
    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

    for row in reader:
        cursor.execute('''
            INSERT INTO seller VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (row['email'], addresses[row['Business_Address_ID']][0], addresses[row['Business_Address_ID']][1], 
                row['business_name'], 1, '000-000-0000', row['bank_account_number']))
        
        cursor.execute('''
            INSERT INTO bankInfo VALUES (?, ?, ?)
        ''', (row['bank_account_number'], row['bank_routing_number'], row['balance']))

connection.commit()
