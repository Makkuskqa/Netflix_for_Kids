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

bucket_name = "python-rocket-source-data-4s23"
source_blob_name = "etl-placement-report/test.csv"  #"etl-placement-report/test.csv"
destination_file_name = "export.csv"


def download_blob(bucket_name, source_blob_name, destination_file_name):
  """Downloads a blob from the bucket."""
  # The ID of your GCS bucket
  # bucket_name = "your-bucket-name"

  # The ID of your GCS object
  # source_blob_name = "storage-object-name"

  # The path to which the file should be downloaded
  # destination_file_name = "local/path/to/file"

  storage_client = storage.Client()

  bucket = storage_client.bucket(bucket_name)

  # Construct a client side representation of a blob.
  # Note `Bucket.blob` differs from `Bucket.get_blob` as it doesn't retrieve
  # any content from Google Cloud Storage. As we don't need additional data,
  # using `Bucket.blob` is preferred here.
  blob = bucket.blob(source_blob_name)
  blob.download_to_filename(destination_file_name)

  print("Downloaded storage object {} from bucket {} to local file {}.".format(
    source_blob_name, bucket_name, destination_file_name))

download_blob(bucket_name, source_blob_name, destination_file_name)