import sqlite3

conn = sqlite3.connect("/data/data.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
            CREATE TABLE IF NOT EXISTS subscriptions
            (
                chat_id
                INTEGER,
                spreadsheet_id
                TEXT,
                gid
                TEXT,
                range
                TEXT
            )
            """)

cur.execute("""
            CREATE TABLE IF NOT EXISTS last_values
            (
                spreadsheet_id
                TEXT,
                gid
                TEXT,
                range
                TEXT,
                value_hash
                TEXT,
                raw_value
                TEXT,
                PRIMARY
                KEY
            (
                spreadsheet_id,
                gid,
                range
            )
                )
            """)

conn.commit()


def add_subscription(chat_id, spreadsheet_id, gid, range_):
    cur.execute(
        "INSERT INTO subscriptions VALUES (?, ?, ?, ?)",
        (chat_id, spreadsheet_id, gid, range_)
    )
    conn.commit()


def remove_subscription(chat_id, spreadsheet_id, gid, range_):
    cur.execute(
        "DELETE FROM subscriptions WHERE chat_id=? AND spreadsheet_id=? AND gid=? AND range=?",
        (chat_id, spreadsheet_id, gid, range_)
    )
    conn.commit()


def get_subscriptions():
    cur.execute("SELECT * FROM subscriptions")
    return cur.fetchall()


def get_last_value(spreadsheet_id, gid, range_):
    cur.execute(
        "SELECT value_hash, raw_value FROM last_values WHERE spreadsheet_id=? AND gid=? AND range=?",
        (spreadsheet_id, gid, range_)
    )
    return cur.fetchone()


def set_last_value(spreadsheet_id, gid, range_, value_hash, raw_value):
    cur.execute("""
    INSERT OR REPLACE INTO last_values
    VALUES (?, ?, ?, ?, ?)
    """, (spreadsheet_id, gid, range_, value_hash, raw_value))
    conn.commit()


def get_subscriptions_by_chat(chat_id: int):
    cur.execute(
        "SELECT spreadsheet_id, gid, range FROM subscriptions WHERE chat_id=?",
        (chat_id,),
    )
    return cur.fetchall()
