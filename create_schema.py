import sqlite3
import constant as const


def init_db():
    conn = sqlite3.connect(const.database_file)
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            current_location TEXT NOT NULL,
            session_id TEXT,
            session_expiration DATE 
        )
    """
    )

    conn.commit()
    conn.close()


if __name__ == "__main__":
    init_db()
