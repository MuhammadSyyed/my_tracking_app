import sqlite3
import uuid
from datetime import datetime, timedelta
import constant as const


def connect_db(db):
    return sqlite3.connect(db)


"""User related functions"""


def add_new_user(username, password):
    try:
        conn = connect_db(const.database_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO users (username, password,current_location, session_id, session_expiration) VALUES (?,?,?,?,?)",
            (
                username,
                password,
                "Parking",
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


"""Locations related functions """


def add_new_location(locations_dtls):
    try:
        conn = connect_db(const.database_file)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO locations (location_name, latitude,longitude, description, image_path) VALUES (?,?,?,?,?)",
            (
                locations_dtls["location_name"],
                locations_dtls["latitude"],
                locations_dtls["longitude"],
                locations_dtls["description"],
                locations_dtls["image_path"],
            ),
        )

        return {"success": True, "message": "Locations added successfully"}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": "Locations already exists!"}
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def get_location_by_id(location_id):

    conn = sqlite3.connect(const.database_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM locations WHERE location_id = ?", (location_id,))
    location = cursor.fetchone()
    conn.close()

    if location:
        return dict(location)


def update_location(locations_dtls):
    try:
        conn = connect_db(const.database_file)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE locations SET location_name = ?, latitude = ?, longitude = ?, description = ?, image_path = ? WHERE location_id = ?",
            (
                locations_dtls["location_name"],
                locations_dtls["latitude"],
                locations_dtls["longitude"],
                locations_dtls["description"],
                locations_dtls["image_path"],
                locations_dtls["location_id"],
            ),
        )

        if cursor.rowcount == 0:
            return {"success": False, "message": "Location not found!"}

        return {"success": True, "message": "Location updated successfully"}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": "Error updating location!"}
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def delete_location(location_id):
    try:
        conn = connect_db(const.database_file)
        cursor = conn.cursor()
        cursor.execute("DELETE FROM locations WHERE location_id = ?", (location_id,))

        if cursor.rowcount == 0:
            return {"success": False, "message": "Location not found!"}

        return {"success": True, "message": "Location deleted successfully"}
    except sqlite3.Error as e:
        return {"success": False, "message": "Error deleting location!"}
    finally:
        conn.commit()
        cursor.close()
        conn.close()


def get_all_locations():

    conn = sqlite3.connect(const.database_file)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM locations")
    locations = cursor.fetchall()
    conn.close()

    if locations:
        return [dict(loc) for loc in locations]
    else:
        return []


def update_user_location_by_session_id(session_id, location):
    try:
        conn = connect_db(const.database_file)
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE users SET current_location = ? WHERE session_id = ?",
            (location, session_id),
        )
        return {"success": True, "message": "Location updated successfully"}
    except sqlite3.IntegrityError as e:
        return {"success": False, "message": "Error updating location!"}
    finally:
        conn.commit()
        cursor.close()
        conn.close()


if __name__ == "__main__":

    # add_new_user("Imran", "1234")
    # user = get_one_user("Imran","1234")
    # print(user)
    add_new_location(
        {
            "location_name": "Parking",
            "latitude": 24,
            "longitude": 67,
            "description": "Main University gate",
            "image_path": "",
        }
    )
    # loc = get_location_by_id(1)
    # print(loc)
    # print(get_all_locations())

    # update_location({'location_id': 2, 'location_name': 'Parking', 'latitude': 24.0, 'longitude': 67.0, 'description': 'Parking', 'image_path': ''})
    # delete_location(2)
    # print(get_all_locations())
