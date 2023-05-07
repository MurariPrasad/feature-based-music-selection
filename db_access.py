import sqlite3 as sql3
import pandas as pd
import requests

BQ_URL = "https://asia-south1-feature-music-selection.cloudfunctions.net/query_table"
TABLE_PATH = "feature-music-selection.music_dataset.audio-data"


def read_db(query: str):
    assert "select" in query.lower(), "Not a SELECT Query"

    headers = {
        "query": query
    }
    resp = requests.get(BQ_URL, params=headers)

    return pd.DataFrame(resp.json())

# def read_db(query: str):
#     conn = sql3.connect('database.db')
#
#     assert "select" in query.lower(), "Not a SELECT Query"
#     cursor = conn.execute(query)
#
#     # get the rows & the headers
#     columns = [col[0] for col in cursor.description]
#     data = cursor.fetchall()
#
#     # format into row-wise json
#     response = []
#     for row in data:
#         dct = {}
#         for n, col in enumerate(columns):
#             dct[col] = row[n]
#
#         response.append(dct)
#
#     return response
#
#
# def write_db(query: str,  values):
#     conn = sql3.connect('database.db')
#
#     assert "insert" in query.lower(), "Not an INSERT Query"
#     conn.execute(query, values)
#     conn.commit()


if __name__ == "__main__":
    read_db(""" select * from `feature-music-selection.music_dataset.audio-data` LIMIT 10 """)
