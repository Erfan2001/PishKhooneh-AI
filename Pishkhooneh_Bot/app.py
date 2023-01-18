from flask import Flask
from main import crawler
import multiprocessing
import sqlite3
import requests
app = Flask(__name__)
def runFlaskApp():
    app.run(host='0.0.0.0',port=80)
@app.route('/')
def introduction():
    return 'HI My Name is BOT'
@app.route('/get')
def getInformation():
    rows=[]
    with sqlite3.connect('db.sqlite3') as connection:
        try:
            cur = connection.cursor()
            cur.execute('SELECT * FROM estimate_homes2')
            rows = cur.fetchall();
        except sqlite3.Error as er:
                    print('Error => ', er)
    return {'data':rows}

if __name__ == "__main__":
    process_1 = multiprocessing.Process(name='p1', target=crawler)
    process_2 = multiprocessing.Process(name='p', target=runFlaskApp)
    process_1.start()
    process_2.start()