from multiprocessing import Process, Queue, Event, Pool
from google.oauth2 import service_account
from google.cloud import storage
import pandas as pd
import pandas_gbq
import datetime
import sqlite3
import requests
import time
import json
import sys
import re




def download_blob(bucket_name, source_blob_name, destination_file_name):
    # TODO : """Downloads a blob from the bucket."""
    storage_client = storage.Client.from_service_account_json('program/authorization/service_user_read_file.json')
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(
        "Downloaded storage object {} from bucket {} to local file {}.".format(
            source_blob_name, bucket_name, destination_file_name
        )
    )


def download_bigquerycsv(project_id):
    # TODO: call and then save to csv bigquery request
    credentials_file = 'program/authorization/service_user_read_bigquery.json'
    credentials = service_account.Credentials.from_service_account_file(credentials_file)
    sql = """
        SELECT id, rating AS name
        FROM etl_netflix.ratings
        """
    df = pandas_gbq.read_gbq(sql, project_id=project_id, credentials=credentials)
    df.to_csv("program/data_sources/ratings.csv", index = False)
    

def print_time(func_name, start_time):
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"{func_name} completed in {elapsed_time:.2f} seconds")


def main():
    print("--------------------")
    print("netflix for kids")
    print("--------------------")

    # download_blob(bucket_name = "python-rocket-source-data-4s23",\
    #             source_blob_name = "etl-netflix/netflix_shows.csv",\
    #                 destination_file_name = "program/data_sources/netflix_shows.csv")

    # download_bigquerycsv(project_id = 'python-rocket-1' )

    start_time = time.time()
    sys.path.append('program/data_export/')

    # TODO : 1 PART Script.  Find all unique data in a parent <netflix_shows.csv> file + Calling API to find gdb per country

    print(f"1.Adding to list unique countries. \n 2.Searching with API gdp per capita")
    from t_6_7_Csv_files_work import find_all_geos, gdp_per_capita_multiprocessing
    unique_countries_list = find_all_geos()
    #gdp_per_capita_multiprocessing(unique_countries_list)
    print_time("Function 1", start_time)


    # TODO : Creating, Insert data into DB. + Creating View and clear result TABLE

    print(f"3.Creating all needed for program databases")
    from t10_creating_SQLiteDB import main_t10
    main_t10()
    print_time("Function 2", start_time)

    print(f"4. Inser data (gdp, netflix_shows, ratings) to different DB Tables ")
    from t_10_Insert_data_to_SQL import main_t10_1
    main_t10_1()
    print_time("Function 3", start_time)

    print(f"5. Craete and JOIN NETFLIX_SHOWS column <rating> with Ratings column <name> ")
    from t12_sql_Join_Rating import main_t12
    main_t12()
    print_time("Function 3", start_time)

    print(f"6. Craete VIEW and JOIN NETFLIX_SHOWS column <rating> with Ratings column <name>")
    from t14_creating_view import main_t14
    main_t14()
    print_time("Function 4", start_time)

    print(f"7. 1.show all created views \n 2. Creating NETFLIX_COMBINED_CLEANED ")
    from t15_creating_cleanedTable import main_t15
    main_t15()
    print_time("Function 5", start_time)


    # TODO : Algorithms to find KIDS content and return completed DF result

    # Find by API from https://www.omdbapi.com/  additional info to every movie
    #from t16_17_Additional_info_by_Movie_Target_kids import   # TODO : better start manually, because of >10 minutes waiting (For this project data is saved in data_sources)

    print(f"9. 1.write query to NETFLIX_COMBINED_CLEANED and save data to df \n 2.# Targeting all KIDS related content  \n 3. merging parent DF with additional info  \n 4. showing Kids Recomedation content \n 5.Saving it into Table + csv")
    from t16_19_clear_target_forKIDS import main_t16_19
    main_t16_19()
    print_time("Function 6", start_time)


if __name__ == "__main__":
  main()
