import sqlite3
with sqlite3.connect('Pishkhooneh_Bot\db3.sqlite3') as connection:
    try:
        cur = connection.cursor()
        cur.execute(f'delete from estimate_home')
        cur.execute(f'SELECT * from estimate_homes2')
        connection.commit()
    except sqlite3.Error as er:
        print('Total Error => ', er)