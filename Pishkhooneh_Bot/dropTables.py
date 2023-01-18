import sqlite3
with sqlite3.connect('db.sqlite3') as connection:
    try:
        cur = connection.cursor()
        cur.execute(f'delete from estimate_home')
        cur.execute(f'delete from estimate_homes2')
        connection.commit()
    except sqlite3.Error as er:
        print('Total Error => ', er)