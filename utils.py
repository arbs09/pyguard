from db import get_db_connection
import json

def is_owner(ctx):
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM owners WHERE owner_id = ?', (str(ctx.author.id),))
    owner = cursor.fetchone()
    connection.close()
    return str(ctx.author.id) in owner

def is_server_owner(ctx):
    return ctx.author.id == ctx.guild.owner_id

def get_statuses():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT type, status FROM statuses')
    rows = cursor.fetchall()
    connection.close()

    statuses = {}
    for row in rows:
        type_ = row[0]
        status = row[1]
        if type_ not in statuses:
            statuses[type_] = []
        statuses[type_].append(status)
    
    return json.dumps(statuses)

def user_data_export(ctx):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM users WHERE user_id = ?', (str(ctx.author.id),))
    user_data = cursor.fetchone()
    
    cursor.execute('SELECT * FROM global_xp WHERE user_id = ?', (str(ctx.author.id),))
    global_xp_data = cursor.fetchone()
    
    cursor.execute('SELECT * FROM server_xp WHERE user_id = ?', (str(ctx.author.id),))
    server_xp_data = cursor.fetchone()
    
    connection.close()
    
    def row_to_dict(row):
        return {key: row[key] for key in row.keys()}
    
    user_info = {
        'user_data': row_to_dict(user_data) if user_data else None,
        'global_xp_data': row_to_dict(global_xp_data) if global_xp_data else None,
        'server_xp_data': row_to_dict(server_xp_data) if server_xp_data else None
    }
    
    return json.dumps(user_info)

def import_memers_from_server(user_id, user_name, server_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('INSERT OR IGNORE INTO users (user_id, user_name) VALUES (?, ?)', (str(user_id), user_name))
    cursor.execute('INSERT OR IGNORE INTO server_xp (user_id, server_id) VALUES (?, ?)', (str(user_id), str(server_id)))
    cursor.execute('INSERT OR IGNORE INTO global_xp (user_id) VALUES (?)', (str(user_id),))
    
    connection.commit()
    connection.close()
    
    return "User imported successfully."

# xp

def calculate_level(xp):
    level = 0
    while xp >= (level + 1) * 100:
        level += 1
        xp -= level * 100
    return level

def give_global_level(user):
    connection = get_db_connection()
    cursor = connection.cursor()
    current_xp = cursor.execute('SELECT xp FROM global_xp WHERE user_id = ?', (str(user.id),)).fetchone()[0]
    level = calculate_level(current_xp)
    cursor.execute('UPDATE global_xp SET level = ? WHERE user_id = ?', (level, str(user.id)))
    connection.commit()
    connection.close()

def give_server_level(user, server_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    current_xp = cursor.execute('SELECT xp FROM server_xp WHERE user_id = ? AND server_id = ?', (str(user.id), str(server_id))).fetchone()[0]
    level = calculate_level(current_xp)
    cursor.execute('UPDATE server_xp SET level = ? WHERE user_id = ? AND server_id = ?', (level, str(user.id), str(server_id)))
    connection.commit()
    connection.close()

def give_global_xp(user, xp):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM global_xp WHERE user_id = ?', (str(user.id),))
    user_data = cursor.fetchone()
    
    if user_data:
        cursor.execute('UPDATE global_xp SET xp = xp + ? WHERE user_id = ?', (xp, str(user.id)))
    else:
        cursor.execute('INSERT INTO global_xp (user_id, xp) VALUES (?, ?)', (str(user.id), xp))
    
    connection.commit()
    connection.close()

    # now update level
    give_global_level(user)

def give_server_xp(user, server_id, xp):
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM server_xp WHERE user_id = ? AND server_id = ?', (str(user.id), str(server_id)))
    user_data = cursor.fetchone()

    if user_data:
        cursor.execute('UPDATE server_xp SET xp = xp + ? WHERE user_id = ? AND server_id = ?', (xp, str(user.id), str(server_id)))
    else:
        cursor.execute('INSERT INTO server_xp (user_id, server_id, xp) VALUES (?, ?, ?)', (str(user.id), str(server_id), xp))

    connection.commit()
    connection.close()

    # now update level
    give_server_level(user, server_id)

def get_global(user):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('SELECT xp, level FROM global_xp WHERE user_id = ?', (str(user.id),))
    result = cursor.fetchone()
    
    if result:
        data = {
            "xp": result[0],
            "level": result[1]
        }
    else:
        data = {
            "xp": 0,
            "level": 0
        }
    
    connection.close()
    return data

def get_server(user, server_id):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    cursor.execute('SELECT xp, level FROM server_xp WHERE user_id = ? AND server_id = ?', (str(user.id), str(server_id)))
    result = cursor.fetchone()
    
    if result:
        data = {
            "xp": result[0],
            "level": result[1]
        }
    else:
        data = {
            "xp": 0,
            "level": 0
        }
    
    connection.close()
    return data
