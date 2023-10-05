import sqlite3

def connect_to_db(db_name):
    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()
    return connection, cursor

def init_user_db():
    conn, cursor = connect_to_db("users.db")
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT,
                      telegram_id TEXT)""")
    conn.commit()
    conn.close()

def init_tasks_db():
    conn, cursor = connect_to_db("tasks.db")
    cursor.execute("""CREATE TABLE IF NOT EXISTS tasks (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      question TEXT,
                      correct_answer TEXT,
                      correct_answer1 TEXT,
                      correct_answer2 TEXT,
                      correct_answer3 TEXT)""")
    conn.commit()
    conn.close()

def add_new_user(username, telegram_id):
    conn, cursor = connect_to_db("users.db")
    cursor.execute("INSERT INTO users (username, telegram_id) VALUES (?, ?)", (username, telegram_id))
    conn.commit()
    conn.close()

def get_task(task_id):
    conn, cursor = connect_to_db("tasks.db")
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task = cursor.fetchone()
    conn.close()
    return task