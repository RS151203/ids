import sqlite3
import hashlib


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(conn, username, password):
    hashed_password = hash_password(password)
    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO user_authentication (username, password) VALUES (?, ?)",
                       (username, hashed_password))
        conn.commit()
        print("User added successfully")
    except sqlite3.IntegrityError:
        print("Username already exists")
    except sqlite3.Error as e:
        print(e)


def check_user(conn, username, password):
    hashed_password = hash_password(password)
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM user_authentication WHERE username=? AND password=?", (username, hashed_password))
        user = cursor.fetchone()
        # return True
        if user:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(e)


def change_user_credentials(conn, current_username, current_password, new_username=None, new_password=None):
    try:
        cursor = conn.cursor()
        username = current_username
        if new_username:
            cursor.execute("UPDATE user_authentication SET username=? WHERE username=? AND password=?",
                           (new_username, current_username, hash_password(current_password)))
            username = new_username
        if new_password:
            hashed_new_password = hash_password(new_password)
            if username != current_username:
                cursor.execute("UPDATE user_authentication SET password=? WHERE username=? AND password=?",
                               (hashed_new_password, username, hash_password(current_password)))
            else:
                cursor.execute("UPDATE user_authentication SET password=? WHERE username=? AND password=?",
                               (hashed_new_password, current_username, hash_password(current_password)))
        conn.commit()
        return username
    except sqlite3.Error as e:
        print(e)


def add_email(conn, username, email):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE user_authentication SET email=? WHERE username=?", (email, username))
        conn.commit()
    except sqlite3.Error as e:
        print(e)


def get_email(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT email FROM user_authentication WHERE username=?", (username,))
        result = cursor.fetchone()
        if result:
            emails_text = result[0]
            return emails_text
    except sqlite3.Error as e:
        print(e)


def delete_email(conn, username):
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE user_authentication SET email=NULL WHERE username=?", (username,))
        conn.commit()
        print("Emails deleted successfully for username:", username)
    except sqlite3.Error as e:
        print(e)
