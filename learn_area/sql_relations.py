## SQL RELATIONS

# 1) Create a SQllite Database with the name test_database.db in the directory "learn_area"

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

# 3) Now lets check if everything was created like we intended.

# a) Check the data of each table

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
