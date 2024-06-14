import sqlite3

def get_db_connection():
    return sqlite3.connect('pet_bot.db')

def view_pets():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pets")
    rows = cursor.fetchall()
    
    print("Pets Table:")
    for row in rows:
        print(row)
    
    conn.close()

def view_users():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    
    print("Users Table:")
    for row in rows:
        print(row)
    
    conn.close()

def view_reminders():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM reminders")
    rows = cursor.fetchall()
    
    print("Reminders Table:")
    for row in rows:
        print(row)
    
    conn.close()


if __name__ == "__main__":
    view_pets()
    view_users()
    view_reminders()