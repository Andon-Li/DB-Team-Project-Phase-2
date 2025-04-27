import sqlite3
import csv
from hashlib import sha256

connection = sqlite3.connect('nittanybusiness.db')
cursor = connection.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS user (
    email           TEXT NOT NULL PRIMARY KEY,
    passwordHash    TEXT NOT NULL
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cardInfo (
    number  TEXT NOT NULL PRIMARY KEY,
    type    TEXT NOT NULL,
    expDate TEXT NOT NULL,
    securityCode TEXT NOT NULL
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS bankInfo (
    accountNum  TEXT NOT NULL PRIMARY KEY,
    routingNum  TEXT NOT NULL,
    balance     INTEGER NOT NULL
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS zipInfo (
    zipCode TEXT NOT NULL PRIMARY KEY,
    city    TEXT NOT NULL,
    state   TEXT NOT NULL
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS helpDesk (
    email       TEXT NOT NULL PRIMARY KEY,
    Position    TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES user(email)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS category (
    name   TEXT NOT NULL PRIMARY KEY,
    parent  TEXT NOT NULL
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS buyer (
    email       TEXT NOT NULL PRIMARY KEY,
    street      TEXT NOT NULL,
    zipCode     TEXT NOT NULL,
    businessName    TEXT NOT NULL,
    activeStatus    INTEGER NOT NULL,
    cardNum      TEXT NOT NULL,
    FOREIGN KEY (email) REFERENCES user(email),
    FOREIGN KEY (cardNum) REFERENCES cardInfo(number),
    FOREIGN KEY (zipCode) REFERENCES zipInfo(zipCode)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS seller (
    email       TEXT NOT NULL PRIMARY KEY,
    street      TEXT NOT NULL,
    zipCode     TEXT NOT NULL,
    businessName    TEXT NOT NULL,
    activeStatus    INTEGER NOT NULL,
    csNum           TEXT NOT NULL,
    bankAccountNum  TEXT NOT NULL,
    FOREIGN KEY (bankAccountNum) REFERENCES bankInfo(accountNum),
    FOREIGN KEY (email) REFERENCES user(email),
    FOREIGN KEY (zipCode) REFERENCES zipInfo(zipCode)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS listing (
    id          TEXT NOT NULL PRIMARY KEY,
    sellerEmail TEXT NOT NULL,
    category    TEXT NOT NULL,
    title       TEXT NOT NULL,
    name        TEXT NOT NULL,
    description     TEXT NOT NULL,
    quantity        INTEGER NOT NULL,
    price           REAL NOT NULL,
    activeStatus    INTEGER NOT NULL,
    FOREIGN KEY (sellerEmail) REFERENCES seller(email),
    FOREIGN KEY (category) REFERENCES category(name)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS rating (
    authorEmail     TEXT NOT NULL,
    recipientEmail  TEXT NOT NULL,
    rating          REAL NOT NULL,
    PRIMARY KEY (authorEmail, recipientEmail),
    FOREIGN KEY (authorEmail) REFERENCES user(email),
    FOREIGN KEY (recipientEmail) REFERENCES user(email)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS question (
    listingId   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    buyerEmail  TEXT NOT NULL,
    body        TEXT NOT NULL,
    answer      TEXT NOT NULL,
    FOREIGN KEY (listingId) REFERENCES listing(id),
    FOREIGN KEY (buyerEmail) REFERENCES buyer(email)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS purchase (
    id   INTEGER PRIMARY KEY AUTOINCREMENT,
    buyerEmail      TEXT NOT NULL,
    listingId       TEXT NOT NULL,
    quantity        INTEGER NOT NULL,
    unitPrice       REAL NOT NULL,
    activeStatus    INTEGER NOT NULL,
    FOREIGN KEY (buyerEmail) REFERENCES buyer(email),
    FOREIGN KEY (listingId) REFERENCES listing(id)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS review (
    buyerEmail  TEXT NOT NULL,
    purchaseId   TEXT NOT NULL,
    body TEXT NOT NULL,
    rating REAL NOT NULL,
    PRIMARY KEY (buyerEmail, listingId),
    FOREIGN KEY (buyerEmail) REFERENCES buyer(email),
    FOREIGN KEY (purchaseId) REFERENCES purchase(id)
);''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS cart (
    buyerEmail  TEXT NOT NULL,
    listingId   TEXT NOT NULL,
    quantity    INTEGER NOT NULL,
    PRIMARY KEY (buyerEmail, listingId),
    FOREIGN KEY (buyerEmail) REFERENCES buyer(email),
    FOREIGN KEY (listingId) REFERENCES listing(id)
);''')


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


with open('data/Categories.csv', newline='') as f:
    # parent_category,category_name
    
    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')

    for row in reader:
        cursor.execute('''
            INSERT INTO category VALUES (?, ?)
        ''', (row['category_name'], row['parent_category']))


with open('data/Product_Listings.csv', newline='') as f:
    # Seller_Email,Listing_ID,Category,Product_Title,Product_Name,Product_Description,Quantity,Product_Price,Status
    
    reader = csv.DictReader(f)
    reader.fieldnames[0] = reader.fieldnames[0].lstrip('\ufeff')
    for row in reader:
        for fieldname in reader.fieldnames:
            value = row[fieldname]

            if value[0] == '\"':
                value = value[1:-1]

            value = value.replace('\"\"', '\"')

            if value.find('$') >= 0:
                value = value.strip('$,')

            value = value.strip('?')
            value = value.strip()

            row[fieldname] = value
        

        cursor.execute('''
            INSERT INTO listing VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (row['Listing_ID'], row['Seller_Email'], row['Category'], row['Product_Title'], row['Product_Title'], 
                row['Product_Description'], row['Quantity'], row['Product_Price'], 1))




connection.commit()
