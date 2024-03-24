import sqlite3
import hashlib


def create_connection(db_file):
    """Create a database connection to the SQLite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except sqlite3.Error as e:
        print(e)
    return conn


def hash_password(password):
    """Hash the password using SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()


def add_user(conn, username, password):
    """Add a new user with hashed password to the database"""
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
    """Check if a user with the given username and password exists"""
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
