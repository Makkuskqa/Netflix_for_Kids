
# SQL Joins: How to combine the tables
Now back to our learning example. We have the 2 tables "DIRECTORS" and "MOVIES". We already know the relations. But now we want to combine their data.

In SQL you combine tables by using JOINS. There are endless tutorials about JOINs. Feel free to check them if you want or need a deeper understanding. At this point i will tell you only as much as you need to continue.

In SQL there are different JOINS. The most important once that you need to know at this moment:
1) LEFT JOIN
2) INNER JOIN


Remember our tables:

Table 1: DIRECTORS

![image](image_9.png)

Table 2: MOVIES

![image](image_12.png)


### SQL LEFT JOIN

Now lets say, we want to know for every movie the name of the director. In table 1 we have the name of the director. But in table 2 only the ID.

In the end we want a result which looks like this. Here you we see every movie and the name of the director of the movie. We also see 2 more things:
1) Every row from the table "MOVIES" is still there.
2) For the movie "Lord of the Rings" we didnt find a director_name. So, there we have a NULL value. 

![image](image_10.png)


The right graphic illustrates a LEFT JOIN. table1 is our "MOVIES". and table2 is "DIRECTORS"
![image](image_5.png)

So, how can we combine both tables together like this in SQL?

Yes, with a JOIN. More concrete a LEFT JOIN Here is the command we need to execute to get the resulting table:

```sql
SELECT m.id, m.name, m.director_id, d.name as director_name
FROM MOVIES as m
LEFT JOIN DIRECTOR as d ON m.director_id = d.id
```

What does this query do? This is how you should read it:
1. We select our first table "Movies" with "FROM Movies".
2. Then we decide which other table we want to JOIN. In this case we JOIN "DIRECTOR" with "LEFT JOIN DIRECTOR".
3. We say please join the tables where the column "director_id" from the table "MOVIES" equals the column "id" from the table "DIRECTOR" (m.director_id = d.id). Remember here we have our relation.
4. WITH the "SELECT" we define which columns of each tables we want to display.



Lets take a look back at our table. In our case of the LEFT JOIN the table "MOVIES" is on the left. This is always the table that we call after the "FROM".
- All the rows from the left table will still be in the result.
- When a row from the left table has cant find any value (in this case Lord of the Rings cant find a director name) we get a NULL value.

### LEFT JOIN (the other way around)
You might have realised that we lost some data when we did that join. We cant see the director "Martin scorsese" with the id "2" anywhere in our result table. This is because no movie of the "MOVIES" table has the director_id "2" for "Martin scorsese".

Lets say we now want it the other way around. We want to make sure to see all directors. And for ever director we want to join the movies they directed.

We want a table that looks like this. Here you can see:
1) We hav every director, even Martin scorsese.
2) For Martin scorsese there is no movie, so there is a NULL value for the column "movie_name"
3) We now have 2 rows with the direcor "Christopher Nolan". This is because we have 2 movies that he directed.

![image](image_14.png)

This would be the query:
```sql
SELECT d.id, d.name, m.name as movie_name
FROM DIRECTOR d
LEFT JOIN MOVIES m ON d.id = m.director_id
```

1) We now change the order of the tables. Now "DIRECTOR" is on the left.
2) We join still with the same condition.
3) We choose other columns that we want to display



### SQL INNER JOIN

As you can see in the first LEFT JOIN we would still have the movie "Lord of the Rings" even though it has no director. 

In the second LEFT JOIN we would still have the director "Martin scorsese" even though he has no movie. 


But know lets say, we want only rows where we find a match in the other table. We dont want those 2 cases with NULL values.

We want this result:
![image](image_13.png)


For that we need to use a INNER JOIN. The query will look like this:
```sql
SELECT m.id, m.name, m.director_id, d.name
FROM MOVIES m
INNER JOIN DIRECTOR d ON m.director_id = d.id
```
1) Everything is like in the first LEFT JOIN example. The only difference is that we now use "INNER JOIN" instead of "LEFT JOIN".
2) When using an INNER JOIN it doesnt matter which table is on the left or on the right. You can change the tables and still get the same result.

## SQL JOIN Tasks

### TASK 8 (CODING):
Now you will do your own JOINS. 
- Go through the file file learnarea/sql_joins.py


### TASK 9 (PROJECT):
Now lets use JOINS in our ETL project.
- Create a new table "NETFLIX_META_WITH_RATING". For that JOIN 2 of the tables so we get the follwing: We want all rows and columns from the table "NETFLIX_SHOWS". But for the column "ratings" instead of the number we want the actual name of the rating.
- JOIN 2 of the tables