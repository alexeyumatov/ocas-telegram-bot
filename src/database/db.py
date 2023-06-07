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
    res = cursor.execute(f"SELECT username FROM users WHERE user_id = {user_id}").fetchall()
    return res[0][0]


async def update_username(user_id, username):
    cursor.execute(
        f'UPDATE users SET username = "{username}" WHERE user_id = {user_id}')
    conn.commit()


async def update_currency(user_id, currency):
    cursor.execute(
        f'UPDATE users SET saved_currency = "{currency}" WHERE user_id = {user_id}')
    conn.commit()
