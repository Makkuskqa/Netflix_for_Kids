# SQL JOINS
import sqlite3

# 1) Connect to the database you created in ""

conn = sqlite3.connect('db_name')
cursor = conn.cursor()

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

cursor.execute("""
SELECT c.id, c.name, h.house_name
FROM GAME_OF_THRONES_CHARACTERS c
LEFT JOIN GAME_OF_THRONES_HOUSES h ON c.house_id = h.id
WHERE h.house_name IS NOT NULL
""")

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

cursor.execute("""
SELECT c.id, c.name, COALESCE(h.house_name, 'None') AS house_name
FROM GAME_OF_THRONES_CHARACTERS c
LEFT JOIN GAME_OF_THRONES_HOUSES h ON c.house_id = h.id
""")


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

cursor.execute("""
CREATE TABLE GAME_OF_THRONES_CHARACTER_WITH_HOUSES_NONULL AS
SELECT c.id, c.name, h.house_name
FROM GAME_OF_THRONES_CHARACTERS c
INNER JOIN GAME_OF_THRONES_HOUSES h ON c.house_id = h.id
""")


# FINISHED: Now get back to the instructions.
