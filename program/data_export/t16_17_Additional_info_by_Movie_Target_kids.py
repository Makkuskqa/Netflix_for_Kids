import pandas as pd
import time
import requests
from multiprocessing import Process, Queue, Event, Pool
import json
import sqlite3


def call_api(api_key,  data):
    results = []
    for value in data:
        if value is None:
            print("all titles were processed")          
            break
        else:
            try:
                response = requests.get(f'http://www.omdbapi.com/?t={value}&apikey={api_key}')
                result = json.loads(response.text)
                try:
                    result['Ratings'] = ', '.join([f"{rating['Source']}:{rating['Value']}" for rating in result['Ratings']])
                except:
                    result['Ratings'] = 0

                df_request = pd.DataFrame(result, index=[0])
                df_request = df_request[['Title', 'Year', 'Rated', 'Genre', 'Director',
                                            'Plot', 'Language', 'Country', 'Awards', 
                                                'Ratings',  'imdbRating', 'imdbVotes']]                          
                results.append(df_request)
                print(results)
                #time.sleep(0.2)
                
            except Exception as e:
                print(f"!!!!!, {e, api_key, data}, !!!!")
                

    return results

def split_dataframe(df, n):
    """Split dataframe into n roughly equal parts"""
    chunk_size = (len(df) + n - 1) // n  # Fix for non-divisible lengths
    chunks = [df.iloc[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
    return chunks





if __name__ == "__main__":
    start_time = pd.Timestamp.now() 
    results = pd.DataFrame()

    from t16_19_clear_target_forKIDS import main_t16_19
    df = main_t16_19()

    API_KEYS = ['30715a8d', '7dc0a921', '17f3c841', 'b83ba0de', 'a0080555', '8901cd38']
    df_chunks = split_dataframe(df, len(API_KEYS))

    pool = Pool(processes=len(API_KEYS))
    try:
        results_list = pool.starmap(call_api, [(api_key, df_chunk['title']) for api_key, df_chunk in zip(API_KEYS, df_chunks)])
    except Exception as e:
        print(f"Error while processing data: {e}")
        results_list = []
    pool.close()
    pool.join()
    for result in results_list:
        results = results._append(result, ignore_index=True)
        

    results.to_csv('program/data_sources/Additional_info_by_Movie_Target_kids2.csv')
    conn = sqlite3.connect('program/database/netflix_database.db')
    try:
        results.to_sql('Additional_info_by_Movie_Target_kids', conn, if_exists='append', index=False, method='multi')
    except Exception as e:
        print(f"Error while writing to the database: {e}")
    conn.close()

    end_time = pd.Timestamp.now() 
    print(f'process time -- {end_time-start_time}')

