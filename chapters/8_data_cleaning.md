# Data Cleaning/Preparing

Before we use the data, it is important to clean and prepare it. Here are some things we should consider
1) Do we want to remove or change specific values?
2) How do we threat NULL or empty values?
3) Do we want to drop specific columns?
4) Do we want group some values into categories?
5) Do we want to add any columns?

Lets get started!

### TASK 12 (PROJECT):
- Use the VIEW we created as an input
- Create a new table "NETFLIX_COMBINED_CLEANED" where:
- Remove rows where the the column "cast" is empty
- When in the column "country" is no value that put in "unknown".
- When we have in column "country" many countries then replace them with "many"
- We have a bug in the column "title". Sometimes we have the following text: "{TITLE}". Remove this from every row.
- Add a new column with the name "from_2000". When a movie was released 2000 or later then there should be the value "yes". If its before 2000 there should be the value "no"
