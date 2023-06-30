# Data Transformation

Now that we have cleaned and prepared data. We can start to add some transformations for our business case.
You can make those transformations with pandas or with SQL. It is your choice. Both ways work.


### TASK 13 (PROJECT):
We want to remove movies which are not good for kids:
- Filter out movies where the rating says its not for kids.
- Remove all movies which are about war or violence.


### TASK 14 (PROJECT):
Now we want to mark movies which are likely to be popular for kids:
- Add a column "popularity" (it will have values from 1 to 3)
- We have a list of directors which are very popular for kids. Those directors are in the file "popular_directors.csv" Every movie with one of those directors should get a popularity of 3.
- Check the GDP of every country (using our csv "country_gdp.csv"). Every country with a gdp lower then 30000 should get a popularity of 0.
- All remaining movies should get a popularity of 2.


### TASK 15 (PROJECT):
Now its time for your ideas.
- Implement at least 2 more ideas how to figure out which movies are good for kids. Use your creativity. Here you can do some research or add some other information or data you find.
- Create a final table which contains only 3 columns. show_id, title and popularity. Save it as a SQL table and also as a CSV file.