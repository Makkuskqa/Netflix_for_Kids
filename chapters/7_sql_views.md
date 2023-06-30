
# SQL VIEWS
Think of a view as a saved query that you can treat as a table.
Lets say you use the inner join from above. But this time we also add a "WHERE" condition. We want to filter for movies from "Christopher Nolan":

```sql
SELECT m.id, m.name, m.director_id, d.name
FROM MOVIES m
INNER JOIN DIRECTOR d ON m.director_id = d.id
WHERE d.name = "Christopher Nolan
```

The result would look semething like this. We would have only those 2 rows.
![image](image_22.png)

Now we could take the result and load it into a pandas datafram and then work with the data. But lets say, we want to execute the JOIN many times, for example once a day. 

We can save the SQL query in a view. Lets first check the code. It is the same sql query. we just added "CREATE VIEW MOVIES_NOLAN AS". 

```sql
CREATE VIEW MOVIES_NOLAN AS
SELECT m.id, m.name, m.director_id, d.name
FROM MOVIES m
INNER JOIN DIRECTOR d ON m.director_id = d.id
WHERE d.name = "Christopher Nolan
```

What will happen?
Now in your database you with the command "show tables;" you will see something that looks like a table with the name "MOVIES_NOLAN".

![image](image_23.png)

You can now use it as if it is a table. You can for example use this query:

```sql
SELECT name
FROM MOVIES_NOLAN m
```

And you will get:
![image](image_24.png)

So, what makes a view different then a table?
1) We dont store the data of the view. We only store the sql query. Only then when we query the view, the sql query of the view will be executed.
2) Views are dynamic. The data we get from a view changes when the underlying data of the tables the views refers to is changed. So in our example above. When the data from the table "MOVIES" changes, the data we get from the view "MOVIES_NOLAN" also automatically changes.
3) Performance is worse. Understand that querying a view involves executing the underlying query logic each time the view is accessed. This can take more time then if the data of the view would already been stored in a table.

### TASK 10 (CODING):

Lets now create our own views.
- Follow the instructions in "learn_area/sql_views"


### TASK 11 (PROJECT):

Now lets use views in our project:
- Create a View with the name "NETFLIX_COMBINED". This VIEW should be a JOIN between the table "NETFLIX_META_WITH_RATING" and the table "NETFLIX_SHOWS".
- Make sure you dont have any column duplicates.
- Query the VIEW to see if the result is like intended.