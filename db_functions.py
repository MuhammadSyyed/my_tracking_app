import sqlite3
import uuid
from datetime import datetime, timedelta
import constant as const


def connect_db(db):
    return sqlite3.connect(db)


def add_new_user(username, password):
    try:
        conn = connect_db(const.database_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password,current_location, session_id, session_expiration) VALUES (?,?,?,?,?)",
            (
                username,
                password,
                'Main Gate',
                None,
                None,
            ),
        )

        return {"success": True, "message": "User added successfully"}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": "User already exists!"}
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def get_one_user(username, password):
    conn = sqlite3.connect(const.database_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM users WHERE username = ? and password = ? ", (username, password)
    )
    user = cursor.fetchone()
    if user:
        session_id = str(uuid.uuid4())
        session_expiration = datetime.now() + timedelta(minutes=const.expiry_in_minutes)
        cursor.execute(
            "UPDATE users SET session_id = ? WHERE username = ? and password = ? ",
            (session_id, username, password),
        )
        cursor.execute(
            "UPDATE users SET session_expiration = ? WHERE username = ? and password = ? ",
            (session_expiration, username, password),
        )
        conn.commit()
        cursor.close()
        conn.close()

        user_dtl = {
            "user_id": user["user_id"],
            "username": user["username"],
            "password": user["password"],
            "current_location": user["current_location"],
            "session_id": session_id,
            "session_expiration": session_expiration,
        }
        return user_dtl


def get_user_by_session_id(session_id: str):
    conn = sqlite3.connect(const.database_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE session_id = ?", (session_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        user_dtl = {
            "user_id": user["user_id"],
            "username": user["username"],
            "password": user["password"],
            "current_location": user["current_location"],
            "session_id": user["session_id"],
            "session_expiration": datetime.strptime(
                user["session_expiration"], "%Y-%m-%d %H:%M:%S.%f"
            ),
        }
        return user_dtl


def delete_session(session_id: int):
    try:
        conn = sqlite3.connect(const.database_file)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users set session_id = NULL WHERE session_id= ?", (session_id,)
        )
        conn.commit()
        conn.close()
        return {"success": True, "message": "Session removed successfully"}
    except Exception as e:
        print(f"Error deleting session: {str(e)}")
        return {"success": False, "message": "Error deleting session"}


if __name__ == "__main__":

    add_new_user("Imran", "1234")
    # user = get_one_user("Imran","1234")
    # print(user)
