import sqlite3 as sql3


def read_db(query: str):
    conn = sql3.connect('database.db')

    assert "select" in query.lower(), "Not a SELECT Query"
    cursor = conn.execute(query)

    # get the rows & the headers
    columns = [col[0] for col in cursor.description]
    data = cursor.fetchall()

    # format into row-wise json
    response = []
    for row in data:
        dct = {}
        for n, col in enumerate(columns):
            dct[col] = row[n]

        response.append(dct)

    return response


def write_db(query: str):
    conn = sql3.connect('database.db')

    assert "insert" in query.lower(), "Not an INSERT Query"
    cursor = conn.execute(query)


if __name__ == "__main__":
    read_db(""" select * from `audio-data` """)
