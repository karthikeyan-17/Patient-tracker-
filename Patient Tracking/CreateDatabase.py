import sqlite3


sql1 = """
    CREATE TABLE IF NOT EXISTS Patient(
        no TEXT NOT NULL PRIMARY KEY,
        name TEXT,
        gender TEXT,
        address TEXT NOT NULL,
        city TEXT,
        state TEXT,
        concern TEXT,
        att TEXT,
        date TEXT,
        dob TEXT,
        complete BOOLEAN
        
    );
"""

sql2 = """
    CREATE TABLE IF NOT EXISTS Report(
        no TEXT NOT NULL,
        att TEXT,
        date TEXT

    );
"""

sql3 = """
    CREATE TABLE IF NOT EXISTS Cases(
        active INTEGER,
        complete INTEGER,
        total INTEGER

    );
"""

sql = """
        INSERT INTO Cases(active, complete, total) VALUES(%s, %s, %s)""" % (0, 0, 0)


def execute_query(sql):
    with sqlite3.connect("case.db") as conn:
        cur = conn.cursor()
        result = cur.execute(sql)
        conn.commit()
    return result


if __name__ == '__main__':
    execute_query(sql)
