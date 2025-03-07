import sqlite3

connection = sqlite3.connect('db/database.db')

with open('schema.sql') as f:
    connection.executescript(f.read())
    print("DB initialized")

# bot owners
connection.execute('INSERT OR IGNORE INTO bot_owners (user_id) VALUES (?)', ('706119023422603335',))

# statuses
connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('playing', 'with pycord'))
connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('playing', 'with pyguard'))
connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('playing', 'with Linux'))

connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('watching', 'youtube'))
connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('watching', 'a movie'))

connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('listening', 'to music'))
connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('listening', 'to a podcast'))
connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('listening', 'to a cd'))
connection.execute('INSERT OR IGNORE INTO statuses (type, status) VALUES (?, ?)', ('listening', 'to Darknet Diaries'))

connection.commit()
connection.close()