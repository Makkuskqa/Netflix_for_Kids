# SQL JOINS

# 1) Connect to the database you created in ""
import sqlite3
conn = sqlite3.connect('learn_area/test_database.db')

# 2) JOIN the 2 tables "GAME_OF_THRONES_HOUSES" and "GAME_OF_THRONES_CHARACTERS". Dont save the result in a table. Store the result directly in a pandas dataframe. The result should look like this. Especially make sure the "None" value is like in the example.

"""
id | name     | house_name
---------------------------
1  | Arya     | Stark
2  | Tywin    | Lannister
3  | Theon    | None
4  | Daenerys | Targaryen
5  | Robert   | Baratheon
6  | Jaime    | Lannister
7  | Ned      | Stark
"""

import pandas as pd
query = """
SELECT v.id, v.name, h.name as house_name
FROM GAME_OF_THRONES_CHARACTERS v
LEFT JOIN GAME_OF_THRONES_HOUSES h ON v.house_id=h.id
"""
df = pd.read_sql_query(query, conn)
print(df)



# 3) The same like above, bit this time the result should look like this. Especially make sure the "None" value is like in the example.
"""
id | name       | character
---------------------------
1  | Lannister  | Tywin
1  | Lannister  | Lannister
2  | Stark      | Arya
2  | Stark      | Ned
3  | Baratheon  | Robert
4  | Tully      | None
5  | Targaryen  | Daenerys
"""

query = """
SELECT h.id, h.name, v.name as character
FROM GAME_OF_THRONES_HOUSES h 
LEFT JOIN GAME_OF_THRONES_CHARACTERS v ON h.id=v.house_id
"""
df = pd.read_sql_query(query, conn)
print(df)

# 4) This time we will create a new table (name "GAME_OF_THRONES_CHARACTER_WITH_HOUSES_NONULL") with a JOIN: The result should look like this. Here we have NO NULL values anymore. (Dont filter out NULL values. Use a specific JOIN to achieve that).
"""
id | name     | house_name
---------------------------
1  | Arya     | Stark
2  | Tywin    | Lannister
4  | Daenerys | Targaryen
5  | Robert   | Baratheon
6  | Jaime    | Lannister
7  | Ned      | Stark
"""


table = "GAME_OF_THRONES_CHARACTER_WITH_HOUSES_NONULL"
query = f"""
CREATE TABLE IF NOT EXISTS {table}
AS
SELECT v.id, v.name, h.name as house_name
FROM GAME_OF_THRONES_CHARACTERS v
INNER JOIN GAME_OF_THRONES_HOUSES h ON v.house_id=h.id
"""
cursor = conn.cursor()
cursor.executescript(query)
conn.commit()
query = f"SELECT * FROM {table}"
df = pd.read_sql_query(query, conn)
print(df)

# FINISHED: Now get back to the instructions.