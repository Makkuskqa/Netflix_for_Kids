## SQL RELATIONS
import sqlite3
# 1) Create a SQllite Database with the name test_database.db in the directory "learn_area"

conn = sqlite3.connect('learn_area/test_database.db')

# 2) Create those 2 SQL tables with this data and add Primary Key and Foriegn Key (where it makes sense)
"""
The first table "GAME_OF_THRONES_HOUSES" 
id | name
--------------
1  | Lannister
2  | Stark
3  | Baratheon
4  | Tully
5  | Targaryen


The second table "GAME_OF_THRONES_CHARACTERS"
id | name     | house_id
------------------------
1  | Arya     | 2
2  | Tywin    | 1
3  | Theon    | 6
4  | Daenerys | 5
5  | Robert   | 3
6  | Jaime    | 1
7  | Ned      | 2

"""

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# SQLite script to create tables
script = """
    CREATE TABLE GAME_OF_THRONES_HOUSES (
        id INTEGER PRIMARY KEY,
        name TEXT
    );

    INSERT INTO GAME_OF_THRONES_HOUSES (id, name) VALUES (1, 'Lannister');
    INSERT INTO GAME_OF_THRONES_HOUSES (id, name) VALUES (2, 'Stark');
    INSERT INTO GAME_OF_THRONES_HOUSES (id, name) VALUES (3, 'Baratheon');
    INSERT INTO GAME_OF_THRONES_HOUSES (id, name) VALUES (4, 'Tully');
    INSERT INTO GAME_OF_THRONES_HOUSES (id, name) VALUES (5, 'Targaryen');

    CREATE TABLE GAME_OF_THRONES_CHARACTERS (
        id INTEGER PRIMARY KEY,
        name TEXT,
        house_id INTEGER,
        FOREIGN KEY (house_id) REFERENCES GAME_OF_THRONES_HOUSES (id)
    );

    INSERT INTO GAME_OF_THRONES_CHARACTERS (id, name, house_id) VALUES (1, 'Arya', 2);
    INSERT INTO GAME_OF_THRONES_CHARACTERS (id, name, house_id) VALUES (2, 'Tywin', 1);
    INSERT INTO GAME_OF_THRONES_CHARACTERS (id, name, house_id) VALUES (3, 'Theon', 6);
    INSERT INTO GAME_OF_THRONES_CHARACTERS (id, name, house_id) VALUES (4, 'Daenerys', 5);
    INSERT INTO GAME_OF_THRONES_CHARACTERS (id, name, house_id) VALUES (5, 'Robert', 3);
    INSERT INTO GAME_OF_THRONES_CHARACTERS (id, name, house_id) VALUES (6, 'Jaime', 1);
    INSERT INTO GAME_OF_THRONES_CHARACTERS (id, name, house_id) VALUES (7, 'Ned', 2);
"""

# Execute the script
cursor.executescript(script)

# Commit the changes
conn.commit()



# Check the content of the "GAME_OF_THRONES_HOUSES" table

# 3) Now lets check if everything was created like we intended.

# a) Check the data of each table

# Create a cursor object to execute SQL queries
cursor = conn.cursor()
tables = ["GAME_OF_THRONES_HOUSES", "GAME_OF_THRONES_CHARACTERS"]
for table in tables:
  cursor.execute(f"SELECT * FROM {table}")
  houses_data = cursor.fetchall()
  print(f"{table}:")
  for row in houses_data:
    print(row)

# b) Check the relations. For that execute the function "get_relations" from the file "helper_functions.py" and execute the function in the console. This will show you primary key and foreign key of the tables. If you did everything right, the result now should look like this:
"""
Table: GAME_OF_THRONES_HOUSES
Related Tables:  
Primary Key:  id
Foreign Key:  

Table: GAME_OF_THRONES_CHARACTERS
Related Tables:  GAME_OF_THRONES_HOUSES
Primary Key:  id
Foreign Key:  house_id
"""

# FINISHED: Now get back to the instructions.
