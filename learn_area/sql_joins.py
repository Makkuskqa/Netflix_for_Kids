# SQL JOINS

# 1) Connect to the database you created in "sql_relations"

# 2) Combine with a JOIN the tables "GAME_OF_THRONES_HOUSES" and "GAME_OF_THRONES_CHARACTERS". The result should look like this:
"""
id | name     | house_name
---------------------------
1  | Arya     | Stark
2  | Tywin    | Lannister
3  | Theon    | NULL
4  | Daenerys | Targaryen
5  | Robert   | Baratheon
6  | Jaime    | Lannister
7  | Ned      | Stark
"""

# 3) Now JOIN again, but the result should look like this:
"""
id | name       | character
---------------------------
1  | Lannister  | Tywin
1  | Lannister  | Lannister
2  | Stark      | Arya
2  | Stark      | Ned
3  | Baratheon  | Robert
4  | Tully      | NULL
5  | Targaryen  | Daenerys
"""

# 4) Now use another JOIN again, the result should look like this. Here we have no NULL values anymore. (Dont filter out NULL values. Use a specific JOIN)
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

# FINISHED: Now get back to the lesson.
