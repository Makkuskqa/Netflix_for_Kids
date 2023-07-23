# SQL VIEWS

# 1) Explain what is the difference between a view and a table? Especially what are the benefits of using a view? what are the downsides?

" A view is a virtual database table or multi tables , saved as a query or print as a request"
" A table is physical storage of data "

""" Benefits view :
    - optimization
    - Instead of every time using this sql query and execute it, we can instead save the SQL query in a view.
    - Security and access control to our table sources"""
""" Minuses :
    - Read only
    - Overhead """

# 2) Connect to the database you created in "sql_relations"

import sqlite3
con = sqlite3.connect('db.db')
cursor = con.cursor()

# 3) Create a VIEW (the view name  should start with "VIEW_") which contains a JOIN of the 2 tables "GAME_OF_THRONES_HOUSES" and "GAME_OF_THRONES_CHARACTERS" and any WHERE condition.

cursor.execute("""CREATE VIEW VIEW_GAME_OF_THRONES_JOIN AS
SELECT c.id, c.name AS character_name, h.name AS house_name
FROM GAME_OF_THRONES_CHARACTERS c
LEFT JOIN GAME_OF_THRONES_HOUSES h ON c.house_id = h.id
WHERE c.is_alive = 1;""")
               
# 4) Create another VIEW of your choice

cursor.execute("""CREATE VIEW VIEW_GAME_OF_THRONES_CHARACTERS_AND_HOUSES AS
SELECT c.*, h.name AS house_name
FROM GAME_OF_THRONES_CHARACTERS c
LEFT JOIN GAME_OF_THRONES_HOUSES h ON c.house_id = h.id;""")
               

# 5) Now Query both of the VIEWs

VIEW_1 = cursor.execute("""SELECT * FROM VIEW_GAME_OF_THRONES_JOIN;""")
VIEW_2 = cursor.execute("""SELECT * FROM VIEW_GAME_OF_THRONES_CHARACTERS_AND_HOUSES;""")