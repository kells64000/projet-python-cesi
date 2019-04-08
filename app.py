from flask import Flask, render_template
import mysql.connector
from mysql.connector import Error
import pymysql

app = Flask(__name__)

class Database:
    def __init__(self):
        host = "127.0.0.1"
        user = "root"
        password = ""
        db = "cesimad"
        self.con = pymysql.connect(host=host, user=user, password=password, db=db, cursorclass=pymysql.cursors.
                                   DictCursor)
        self.cur = self.con.cursor()
    def list_employees(self):
        self.cur.execute("SELECT cli_prenom,cli_nom FROM customer LIMIT 50")
        result = self.cur.fetchall()
        return result

@app.route('/')
def employees():
    def db_query():
        db = Database()
        emps = db.list_employees()
        return emps
    res = db_query()
    return render_template('index.html', result=res, content_type='application/json')


if __name__ == '__main__':
    app.run()





