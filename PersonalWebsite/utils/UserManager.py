import hashlib
import sqlite3


def hashPass(pWord):
    return hashlib.sha512(pWord.encode()).hexdigest()



'''
Not used for production.  Just use it to add admin
'''
def addDefaultAdmin():
    conn = sqlite3.connect("../database.db")
    c = conn.cursor()
    x = hashPass("admin")


    st = "INSERT INTO users (user, password) VALUES ('admin','"+x+"');"
    c.execute(st)
    conn.commit()
