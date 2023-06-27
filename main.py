"""
from google.cloud import storage
from google.oauth2 import service_account

bucket_name = "python-rocket-source-data-4s23"
file_path = "etl-placement-report/test.csv"  #"etl-placement-report/test.csv"
destination_path = "export.csv"


def download_file_from_gcp():
  credentials = service_account.Credentials \
    .from_service_account_file("python-rocket-1-e40bc56dde8a.json")
  client = storage.Client(credentials=credentials)

  bucket = client.get_bucket(bucket_name)
  blob = bucket.blob(file_path)
  blob.download_to_filename(destination_path)

download_file_from_gcp()
"""

from google.cloud import storage

from google.oauth2 import service_account


def download_blob():
  bucket_name = "python-rocket-source-data-4s23"
  source_blob_name = "etl-netflix/netflix_content.csv"  #"etl-placement-report/test.csv"
  destination_file_name = "data_sources/netflix_content.csv"
  """Downloads a blob from the bucket."""
  # The ID of your GCS bucket
  # bucket_name = "your-bucket-name"

  # The ID of your GCS object
  # source_blob_name = "storage-object-name"

  # The path to which the file should be downloaded
  # destination_file_name = "local/path/to/file"
  credentials = service_account.Credentials.from_service_account_file(
    "chapters/1_GCP/service_user_read_file.json")
  storage_client = storage.Client(project="python-rocket-1",
                                  credentials=credentials)
  bucket = storage_client.bucket(bucket_name)
  # Construct a client side representation of a blob.
  # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
  # any content from Google Cloud Storage. As we don't need additional data,
  # using `Bucket.blob` is preferred here.
  blob = bucket.blob(source_blob_name)
  blob.download_to_filename(destination_file_name)
  print("Downloaded storage object {} from bucket {} to local file {}.".format(
    source_blob_name, bucket_name, destination_file_name))


def read_bq():
  # def read_bq():
  import pandas as pd
  from google.oauth2 import service_account

  # Define the service account credentials JSON file path
  service_account_file = "chapters/1_GCP/service_user_read_bigquery.json"

  # Define the BigQuery project ID and table name
  project_id = 'python-rocket-1'
  table_id = 'etl_netflix.ratings'

  # Set up the BigQuery client with the service account credentials
  credentials = service_account.Credentials.from_service_account_file(
    service_account_file)

  # Query and read the BigQuery table into a DataFrame
  query = f'SELECT * FROM `{project_id}.{table_id}`'
  df = pd.read_gbq(query, project_id=project_id, credentials=credentials)

  # Save the DataFrame as a CSV file
  destination_file = 'data_sources/ratings_data.csv'
  df.to_csv(destination_file, index=False)

  print(
    "Downloaded data from big quuery table {} and saved it in the following file {}."
    .format(table_id, destination_file))


read_bq()
#download_blob()
+
#def create_sql_tables():
import sqlite3

# Connect to the database (or create it if it doesn't exist)
conn = sqlite3.connect('mydatabase.db')

# Create a cursor object to interact with the database
cursor = conn.cursor()

# Create the "Parent" table
cursor.execute('''
    CREATE TABLE Parent (
        id INTEGER PRIMARY KEY,
        name TEXT
    )
''')

# Create the "Child" table with a foreign key referencing the "Parent" table
cursor.execute('''
    CREATE TABLE Child (
        id INTEGER PRIMARY KEY,
        name TEXT,
        parent_id INTEGER,
        FOREIGN KEY (parent_id) REFERENCES Parent (id)
    )
''')

# Commit the changes and close the connection
conn.commit()
conn.close()

conn.execute("SELECT * FROM Parent;").fetchall()
cursor = conn.cursor()
cursor.execute(f"PRAGMA table_info({table_name})")
conn.execute(f"PRAGMA foreign_key_list(Child)").fetchall()


rows = [
    (1, 'Child 1', 1),
    (2, 'Child 2', 1),
    (3, 'Child 3', 2),
    (4, 'Child 4', 3),
    (5, 'Child 5', 3)
]

# Execute the INSERT statement for each row
cursor.executemany('INSERT INTO Child (id, name, parent_id) VALUES (?, ?, ?)', rows)

# Commit the changes
conn.commit()




