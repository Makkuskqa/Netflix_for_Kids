import pandas as pd
import requests
import json
import re
import time
import datetime
from multiprocessing import Process, Queue

def find_all_geos():
    # TODO : read csv file, which we download from Goodle cloud and return list with all unique countries
    df= pd.read_csv('program/data_sources/netflix_shows.csv',\
                         sep=';',  low_memory=False)
    df = df.dropna() 
    # delete empty values

    list_countries = df.country.unique()
    # create list with all unique values in df.country

    unique_countries = set()
    # create set for appending clear <word> value from unique countries

    for item in list_countries:
        words = re.split(r',\s*|,', item)
        # split rows with more than one country inside

        unique_countries.update(words) 
        # update our set

    unique_countries_list = list(unique_countries) 
    #convert to a list

    unique_countries_list.remove('') 
    # remove one empty value

    #print(unique_countries_list)
    return unique_countries_list



# TODO : finding API gdp for every country with <multiprocessing with queue > -- estimated time  == 0 days 00:00:34.841512
# finding API gdp for every country with <LOOP algo> -- estimated time  == 0:02:41.156275
# QUEUE - [ - 2 minutes ]
def fetch_gdp_per_capita(queue):
    # TODO : function for running requests for API
    while True:
        country = queue.get() # get one country from queue
        if country is None: # break if all country have used
            break
        req = requests.get(f'https://api.api-ninjas.com/v1/country?name={country}', headers={'X-Api-Key': 'PtTVI4uKi0xwUvZ+en3hWQ==4otHBoTdMwWzadZq'})
        request_dict = json.loads(req.text)
        try:
            gdp_per_capita = request_dict[0]['gdp_per_capita'] # get gdp value
        except:
            gdp_per_capita = ''   # get empty if country not exists
        queue.put((country, gdp_per_capita)) # put result into queue

def gdp_per_capita_multiprocessing(list_countries, is_test=None):
    # TODO : multiprocessing start
    if is_test == True:
        list_countries = list_countries[:5]
    gdp_per_capitaDF = pd.DataFrame({'country': [], 'gdp_per_capita': []})
    start_time = pd.Timestamp.now() 
    num_workers = 5 # num queue per one time
    queue = Queue()
    processes = []
    for _ in range(num_workers):
        process = Process(target=fetch_gdp_per_capita, args=(queue,)) # start queue
        process.start()
        processes.append(process)
    for country in list_countries: # add country to queue
        queue.put(country)
    for _ in range(num_workers):
        queue.put(None) 
    for process in processes:
        process.join()
    while not queue.empty():
        country, gdp_per_capita = queue.get() # get result from queue
        gdp_per_capitaDF = gdp_per_capitaDF._append(pd.DataFrame([[country, gdp_per_capita]], columns=gdp_per_capitaDF.columns), ignore_index=True)
    end_time = pd.Timestamp.now()
    print(f"Time for all countries: {end_time - start_time}")
    gdp_per_capitaDF.to_csv('program/data_sources/gdp_per_capita.csv', index=False)
    return gdp_per_capitaDF



def main():
    unique_countries_list = find_all_geos()
    gdp_per_capita_multiprocessing(unique_countries_list)#, is_test=True)        # queu algo -- estimated time  == 0 days 00:00:34.841512 (-2 min)


# if __name__ == "__main__":
#     main()



