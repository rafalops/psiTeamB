import sqlite3
import hashlib


def createDatabase():
    """
    Creates the database for the website
    """
    conn = sqlite3.connect('server.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                    log VARCHAR(255) NOT NULL,
                    pass VARCHAR(255) NOT NULL);''')

    conn.commit()
    conn.close()


def insertDetails(user, passw):
    conn = sqlite3.connect('server.db')
    conn.execute(
        "INSERT INTO users (log,pass) VALUES (?,?)", (user, passw,))
    conn.commit()
    conn.close()


def getDetails():
    login = ""
    password = ""
    listN = []
    conn = sqlite3.connect('server.db')
    cursor = conn.execute("SELECT log,pass FROM users ")
    for row in cursor:
        login = row[0]
        listN.append(row[0])
        password = row[1]
    conn.close()
    return login, password, listN

def insertMany():
    users = ["cmsilva","dcabaceira","psilva","rlopes"]
    for i in range(len(users)):
        insertDetails(users[i], hashlib.sha3_224("password".encode("utf-8")).hexdigest())
        
def getPassword(user):
    password = ""
    conn = sqlite3.connect('server.db')
    cursor = conn.execute("SELECT pass FROM users WHERE log=?", (user,))
    for row in cursor:
        password = row[0]
    conn.close()
    return password
