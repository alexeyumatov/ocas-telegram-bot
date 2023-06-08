import sqlite3


conn = sqlite3.connect("src/database/bot.db")
cursor = conn.cursor()


async def start_db(user_id):
    user = cursor.execute(
        f"SELECT * FROM users WHERE user_id = {user_id}").fetchone()
    if not user:
        cursor.execute(f"INSERT INTO users (user_id) VALUES ({user_id})")
        conn.commit()


async def get_username(user_id):
    res = cursor.execute(
        f"SELECT username FROM users WHERE user_id = {user_id}").fetchall()
    return res[0][0]


async def get_currency(user_id):
    res = cursor.execute(
        f"SELECT saved_currency FROM users WHERE user_id = {user_id}").fetchall()
    return res[0][0]


async def update_username(user_id, username):
    cursor.execute(
        f'UPDATE users SET username = "{username}" WHERE user_id = {user_id}')
    conn.commit()


async def update_currency(user_id, currency):
    cursor.execute(
        f'UPDATE users SET saved_currency = "{currency}" WHERE user_id = {user_id}')
    conn.commit()


async def update_last_used_currency(user_id, currency):
    cursor.execute(
        f'UPDATE users SET last_used_currency = "{currency}" WHERE user_id = {user_id}')
    conn.commit()


async def get_last_used_currency(user_id):
    res = cursor.execute(
        f"SELECT last_used_currency FROM users WHERE user_id = {user_id}").fetchall()
    return res[0][0]


async def get_number_of_requests(user_id):
    res = cursor.execute(f"SELECT number_of_requests FROM users WHERE user_id = {user_id}").fetchall()
    return res[0][0]


async def update_number_of_requests(user_id, reset=False):
    if not reset:
        cursor.execute(f"UPDATE users SET number_of_requests = number_of_requests + 1 WHERE user_id = {user_id}")
    else:
        cursor.execute(f"UPDATE users SET number_of_requests = 0 WHERE user_id = {user_id}")
    conn.commit()


async def clear_number_of_requests():
    cursor.execute("UPDATE users SET number_of_requests = 0")
    conn.commit()


async def ban_user(user_id, unban=False):
    if not unban:
        cursor.execute(f"UPDATE users SET is_banned = 1 WHERE user_id = {user_id}")
    else:
        cursor.execute(f"UPDATE users SET is_banned = 0 WHERE user_id = {user_id}")
    conn.commit()


async def get_user_state(user_id):
    res = cursor.execute(f"SELECT is_banned FROM users WHERE user_id = {user_id}").fetchall()
    return res[0][0]


async def set_banned_time(user_id, banned_time, delete=False):
    if not delete:
        cursor.execute(f'UPDATE users SET time_banned = "{banned_time}" WHERE user_id = {user_id}')
    else:
        cursor.execute(f'UPDATE users SET time_banned = "{None}" WHERE user_id = {user_id}')
    conn.commit()


async def get_banned_time(user_id):
    res = cursor.execute(f"SELECT time_banned FROM users WHERE user_id = {user_id}").fetchall()
    return res[0][0]
    