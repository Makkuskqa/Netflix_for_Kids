from google.oauth2 import service_account
import csv
import requests
import pandas_gbq
import json
import pandas as pd
import sqlite3
from program.helper_functions import show_all_tables, show_table_schema, get_relations, show_data_from_table


def main():
  print("--------------------")
  print("netflix for kids")
  print("--------------------")


if __name__ == "__main__":
  main()

from google.cloud import storage


def get_service_account_authorization(path):
  credentials = service_account.Credentials.from_service_account_file(path)
  return credentials


def download_blob(bucket_name, source_blob_name, destination_file_name):
  """Downloads a blob from the bucket."""
  # The ID of your GCS bucket
  # bucket_name = "your-bucket-name"

  # The ID of your GCS object
  # source_blob_name = "storage-object-name"

  # The path to which the file should be downloaded
  # destination_file_name = "local/path/to/file"
  credentials = get_service_account_authorization(
    "program/authorization/service_user_read_file.json")
  storage_client = storage.Client("python-rocket-1", credentials=credentials)

  bucket = storage_client.bucket(bucket_name, )

  # Construct a client side representation of a blob.
  # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
  # any content from Google Cloud Storage. As we don't need additional data,
  # using `Bucket.blob` is preferred here.
  blob = bucket.blob(source_blob_name)
  blob.download_to_filename(destination_file_name)

  print("Downloaded storage object {} from bucket {} to local file {}.".format(
    source_blob_name, bucket_name, destination_file_name))


def get_from_bigquery():
  # TODO: Set project_id to your Google Cloud Platform project ID.
  credentials = get_service_account_authorization(
    "program/authorization/service_user_read_bigquery.json")
  project_id = "python-rocket-1"
  sql = """
  SELECT * FROM etl_netflix.ratings
  """
  df = pandas_gbq.read_gbq(sql, project_id=project_id, credentials=credentials)
  df.rename(columns={'rating': 'name'}, inplace=True)
  df.to_csv("program/data_sources/ratings.csv", index=False, sep=";")


def get_country_list():
  df = pd.read_csv("program/data_sources/netflix_shows.csv", sep=";")
  country_list = list(df["country"])
  unique_countries = set()
  for item in country_list:
    if isinstance(item, str):
      countries = item.split(", ")
      unique_countries.update(countries)
  return unique_countries


def fetch_gdp_per_capita(country_list, test=False):
  # Replace with your list of countries
  gdp_data = []
  for i, country in enumerate(country_list):
    api_url = f'https://api.api-ninjas.com/v1/country?name={country}'
    print(api_url)
    response = requests.get(
      api_url,
      headers={'X-Api-Key': '3x1NqgtMcZhyhiSCAEbzNg==YyEpTnDsxaPTGYN8'})
    if not response.status_code == requests.codes.ok:
      print("Error:", response.status_code, response.text)
    try:
      gdp_per_capita = json.loads(response.text)[0]["gdp_per_capita"]
      gdp_dic = {"country": country, "gdp_per_capita": gdp_per_capita}
      gdp_data.append(gdp_dic)
    except:
      print(f"counldnt find data for country {country}")
    if test and i >= 3:
      break
  df = pd.DataFrame(gdp_data)
  df.to_csv("program/data_sources/gdp_per_capita.csv", index=False, sep = ";")


def create_sql_schemas(conn):
  # creating database
  script_1 = """
  CREATE TABLE IF NOT EXISTS NETFLIX_SHOWS (
        show_id TEXT PRIMARY KEY,
        type TEXT,
        title TEXT,
        director TEXT,
        cast TEXT,
        country TEXT,
        date_added TEXT,
        release_year TEXT,
        rating TEXT,
        duration TEXT,
        listed_in TEXT,
        description TEXT,
        FOREIGN KEY (rating) REFERENCES RATINGS (id),
        FOREIGN KEY (country) REFERENCES GDP_PER_CAPITA (country));
  """
  script_2 = """
  CREATE TABLE IF NOT EXISTS RATINGS (
        id INTEGER PRIMARY KEY,
        name TEXT)
        ;
  """
  script_3 = """
  CREATE TABLE IF NOT EXISTS GDP_PER_CAPITA (
        country TEXT PRIMARY KEY,
        gdp_per_capita REAL)
        ;
  """
  query = "".join([script_1, script_2, script_3])
  cursor = conn.cursor()
  cursor.executescript(query)
  conn.commit()


def insert_into_sql(conn, csv_path, table):
  df = pd.read_csv(csv_path, sep=";")
  df.to_sql(table, conn, if_exists='replace', index=False)
  """
  data_columns = data.columns.tolist()
  insert_query = f'INSERT INTO {table} VALUES ({",".join(["?"] * len(data_columns))})'
  #insert_query = f'INSERT INTO {table} (id, name) VALUES (?, ?)'
  data_tuples = [tuple(x) for x in data.values]
  cursor = conn.cursor()
  cursor.executemany(insert_query, data_tuples)
  """
  
def create_joined_table(conn, table):
  print(f"Creating joined table with the name: {table}")
  query = f"""
  CREATE TABLE IF NOT EXISTS {table}
  AS
  SELECT
  s.show_id,
  s.type,
  s.title,
  s.director,
  s.cast,
  s.country,
  s.date_added,
  s.release_year,
  r.name as rating,
  s.duration,
  s.listed_in,
  s.description
  FROM NETFLIX_SHOWS s 
  LEFT JOIN RATINGS r ON s.rating=r.id
  """
  cursor = conn.cursor()
  cursor.executescript(query)
  conn.commit()
  show_data_from_table(conn, table)

def create_joined_view(conn, view):
  print(f"Creating joined view with the name: {view}")
  query = f"""
  CREATE VIEW IF NOT EXISTS {view}
  AS
  SELECT
  s.show_id,
  s.type,
  s.title,
  s.director,
  s.cast,
  s.country,
  s.date_added,
  s.release_year,
  r.name as rating,
  s.duration,
  s.listed_in,
  s.description
  FROM NETFLIX_SHOWS s 
  LEFT JOIN RATINGS r ON s.rating=r.id
  """
  cursor = conn.cursor()
  cursor.executescript(query)
  conn.commit()
  show_data_from_table(conn, view)


def create_cleaned_table(conn):
  table = "NETFLIX_COMBINED_CLEANED"
  print(f"Creating cleaned table with the name: {table}")
  query = f"""
  CREATE TABLE IF NOT EXISTS {table}
  AS
  SELECT
  show_id,
  type,
  REPLACE(title, '<TITLE>', '') AS title,
  director,
  `cast`,
  CASE
    WHEN country IS NULL OR country = ""
    THEN "unknown"
    WHEN country LIKE '%,%'
    THEN "many"
    ELSE country
  END AS country,
  date_added,
  release_year,
  rating,
  duration,
  listed_in,
  description,
  CASE
    WHEN release_year >= 2000 
    THEN "yes"
    ELSE "no"
  END AS release_2000_or_newer
  FROM VIEW_NETFLIX_SHOWS_WITH_RATING
  WHERE `cast` IS NOT NULL and `cast` != ""
  """
  cursor = conn.cursor()
  cursor.executescript(query)
  conn.commit()
  show_data_from_table(conn, table)


def filter_by_rating(df):
  # TV- ratings: https://en.wikipedia.org/wiki/TV_Parental_Guidelines
  # 
  # not for children: TV-MA, TV-14, NC-17, R (maybe more...)
  ratings_not_for_kids = ["TV-MA", "TV-14", "NC-17", "R"]
  filtered_df = df.drop(df[df['rating'].isin(ratings_not_for_kids)].index)
  return filtered_df

def remove_violent_content(df):
  list_of_violent_words = ["violence", "fight", "blood", "war", "weapon", "death", "blood", "army", "gun"]
  filtered_df = df[~df['description'].apply(lambda x: any(word in x.lower() for word in list_of_violent_words))]
  return filtered_df


def remove_if_not_for_kids(conn):
  query = f"SELECT * FROM NETFLIX_COMBINED_CLEANED"
  df = pd.read_sql_query(query, conn)
  df_rating = filter_by_rating(df)
  df_result = remove_violent_content(df)
  print("dataframe with filtered out violent content")
  print(df_result)
  return df_result


def define_popularity_for_kids(df, conn):
  popular_directors = pd.read_csv("program/data_sources/popular_directors.csv", sep=";")
  gdp_per_capita = pd.read_csv("program/data_sources/gdp_per_capita.csv", sep=";")
  #df['popularity'] = np.where(df['directors'].isin(popular_directors['directors']), 3, np.nan)
  #df['popularity'] = pd.Series(dtype='Int64')
  df['popularity'] = df['director'].isin(popular_directors['director']).map({True: int(3), False: None})
  df_merged = df.merge(gdp_per_capita, on='country', how='left')
  df_merged.loc[df_merged['gdp_per_capita'] < 30000, 'popularity'] = 1
  df_merged['popularity'] = df_merged['popularity'].astype('Int64').fillna(2)
  print("dataframe with popularity column")
  print(df_merged)
  print(df_merged.groupby("popularity").size())
  return df_merged

  
  
def save_final_recommendation(df, conn):
  table = "SHOWS_FOR_KIDS_RECOMMENDATION"
  csv_export_path = "program/data_export/movie_recommendations.csv"
  columns = ["show_id", "title",  "popularity"]

  df_save = df[columns]
  print(f"Saving final movie recommendations in table {table}")
  df_save.to_sql(table, conn, if_exists='replace', index=False)
  print(f"Saving final movie recommendations in csv {csv_export_path}")
  df_save.to_csv(csv_export_path, sep=";")
  


"""
- Remove rows where the the column "cast" is empty
- When in the column "country" is no value that put it to "unknown".
- When we have in column "country" many countries then replace them with "many"
- We have a bug in the column "title". Sometimes we have the following text: "{TITLE}". Remove this from every row.
- Add a new column with the name "2000_or_newer". When a movie was released 2000 or later then there should be the value "yes". If its before 2000 there should be the value "no"
"""

def main():
  
  test = True
  # 1. Download from storage
  print("1. Download from storage")
  bucket_name = "python-rocket-source-data-4s23"
  source_blob_name = "etl-netflix/netflix_shows.csv"
  destination_file_name = "program/data_sources/netflix_shows.csv"
  download_blob(bucket_name, source_blob_name, destination_file_name)
  # 2. Download from Bigquery
  print("2. Download from Bigquery")
  get_from_bigquery()
  
  # 3. Get Country list
  print("3. Get Country list")
  country_list = get_country_list()
  # 4. Download from API
  print("Download from API")
  fetch_gdp_per_capita(country_list, test)

  # 5. SQL
  conn = sqlite3.connect("program/database/netflix_database.db")
  # a) Create tables with relations
  create_sql_schemas(conn)
  show_all_tables(conn)
  for table in ["NETFLIX_SHOWS", "RATINGS", "GDP_PER_CAPITA"]:
    show_table_schema(conn, table)
  get_relations(conn)
  # b) Insert data into tables
  for csv_name, table in [["netflix_shows", "NETFLIX_SHOWS"], ["ratings", "RATINGS"],
                          ["gdp_per_capita", "GDP_PER_CAPITA"]]:
    csv_path = "program/data_sources/" + csv_name + ".csv"
    insert_into_sql(conn, csv_path, table)
    show_data_from_table(conn, table)
  
  # c) Create JOINED table
  
  joined_table = "NETFLIX_SHOWS_WITH_RATING"
  create_joined_table(conn, joined_table)
  #show_data_from_table(conn, joined_table)
  joined_view = "VIEW_NETFLIX_SHOWS_WITH_RATING"
  create_joined_view(conn, joined_view)
  #show_data_from_table(conn, joined_view)

  conn = sqlite3.connect("program/database/netflix_database.db")
  
  create_cleaned_table(conn)
  df = remove_if_not_for_kids(conn)
  df = define_popularity_for_kids(df, conn)
  save_final_recommendation(df, conn)
  



if __name__ == "__main__":
  main()
