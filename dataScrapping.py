
import requests
import json
import sqlite3


#connection to sqlite
sqliteConnection = sqlite3.connect('mainPython.db')
connection = sqliteConnection.cursor()

connection.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='DummyAPiDetails' ''')

if connection.fetchone()[0] != 1 : 

    tableSqlite = '''CREATE TABLE DummyAPiDetails(
        id varchar PRIMARY KEY,
        title text,
        firstName text(2,50) Not Null ,
        lastName text(2,50) Not Null ,
        gender text,
        email varchar Not Null,
        dateOfBirth date,
        registerDate date,
        phone varchar,
        picture varchar,
        street varchar,
        city text,
        state text,
        Country text,
        Timezone time);'''

    connection= sqliteConnection.execute(tableSqlite)
    sqliteConnection.commit()

   

response = requests.get("https://dummyapi.io/data/v1/user?limit=10",headers = {'app-id':'626ad0dce744fc5d0beb4c33'})


data = response.text
p = json.loads(data)
for i in range(10):
    r = requests.get("https://dummyapi.io/data/v1/user/"+(p['data'][i]['id']),headers = {'app-id':'626ad0dce744fc5d0beb4c33'})
    d = r.text
    parse_data = json.loads(d)
    insertQuery = """INSERT INTO DummyApiDetails  VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""
    details = (parse_data['id'],parse_data['title'],parse_data['firstName'],parse_data['lastName'],parse_data['gender'],
            parse_data['email'],parse_data['dateOfBirth'],parse_data['registerDate'],parse_data['phone'],parse_data['picture'],
            parse_data['location']["street"],parse_data['location']["city"],parse_data['location']["state"],parse_data['location']["country"],parse_data['location']["timezone"])
    connection.execute(insertQuery,details)
    sqliteConnection.commit()


#post details
check = connection.execute('''SELECT count(name) FROM sqlite_master WHERE type='table' AND name='PostDetails' ''')

if check.fetchone()[0] != 1: 

    tableSqlite = '''CREATE TABLE PostDetails(
        photoid varchar,
        image varchar,
        likes varchar,
      
        Text_Mentioned text,
        publishDate date,
        id varchar,
        foreign key (id) references DummyApiDetails(id)
        );'''

    connection= sqliteConnection.execute(tableSqlite)
    sqliteConnection.commit()

selectId = connection.execute('''SELECT id from DummyApiDetails''')
extractId = selectId.fetchall()
for i in extractId:
    r = requests.get("https://dummyapi.io/data/v1/user/"+(i[0])+"/post?limit=10",headers = {'app-id':'626ad0dce744fc5d0beb4c33'})
    d = r.text
    parse_data = json.loads(d)
    lengthPost = len(parse_data['data'])
    
  
    j = 0

    while j < lengthPost :
        insertQuery = """INSERT INTO PostDetails  VALUES (?,?,?,?,?,?);"""
        details = (parse_data['data'][j]['id'],parse_data['data'][j]['image'],parse_data['data'][j]['likes'],parse_data['data'][j]['text'],
                parse_data['data'][j]['publishDate'],parse_data['data'][j]['owner']['id'])
        connection.execute(insertQuery,details)
        sqliteConnection.commit()
        j += 1
        print(j)
    

    

    
