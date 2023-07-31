import sqlite3
import pandas as pd
import re
import numpy as np

class Database:
    def __init__(self) -> None:
        self.conn = None
        self.cursor = None

    def connect(self, db_name):
        try:
            self.conn = sqlite3.connect(db_name)
            self.cursor = self.conn.cursor()
        except sqlite3.Error as e:
            print(f" Error connecting to database: {e}")

    def close(self):
        try:
            if self.cursor:
                self.cursor.close()
            if self.conn:
                self.conn.close()
        except sqlite3.Error as e:
            print(f"Error closing database connection: {e}")


    def save_data_toDF(self):
        # TODO : write query to NETFLIX_COMBINED_CLEANED and save data to df

        query = f"SELECT * FROM {'NETFLIX_COMBINED_CLEANED'}"
        data = pd.read_sql_query(query, self.conn)
        return data
    

    def t16_clear_noKids_films(self, df):
        # TODO: create first test part with only Kids content && filtering hard genres

        Kids = ['PG', 'TV-PG','TV-Y', 'TV-Y7','TV-G','G','TV-Y7-FV',]  #  < 10 years old
        teens = ['TV-14','PG-13','NC-17',]                             #  10 < years < 18
        Adults = ['TV-MA','R','NR','UR']                               #  > 18
        No_category = ['74 min', '84 min', '66 min',  None ]           # no accurate category

        want_to_add_to_kids = ['74 min', '84 min', '66 min',  None, 'TV-14','PG-13']  # I think i can find some movies that are for Kids 

        keywords_to_exclude = ['war', 'horror', 'sex', 'drama','thriller', 'religion', 'documentary', 'documentation'] 
# determine keywords for excluding 

# Filtering want_to_add_to_kids rating category
        filtering_double_faced_content = df[df['rating'].isin(want_to_add_to_kids)]  
# make df with potential new content

        filtering_double_faced_content[['description','listed_in']] = filtering_double_faced_content[['description','listed_in']].apply(lambda x: x.str.lower()) 
# making all words content lowercase

        filtering_double_faced_content[['description','listed_in']] = filtering_double_faced_content[['description','listed_in']].applymap(lambda x: re.sub(r'[^\w\s]', '', x))
# remove all non-word characters (e.g., commas, periods)

        filtered_double_faced_content = filtering_double_faced_content[ ~(~filtering_double_faced_content['description'].str.contains('|'.join(keywords_to_exclude), na=False))\
                                                                   & ~(~filtering_double_faced_content['listed_in'].str.contains('|'.join(keywords_to_exclude), na=False))]
# clear dataframe from exclude keywords
        filter_double_faced_content = filtered_double_faced_content._append(df[df['rating'].isin(Kids)] )

        return filter_double_faced_content
    

    def t16_5_Additional_info_by_Movie_Target_kids_NEWDF_NEWTABLE(self, df):

        Not_Related_Genres = ['War', 'Crime', 'Drama',  'History',  'Romance', 'Documentary',    'Western',  'Noir', 'News', 'Thriller',\
                                       'Biography',  'Talk', 'Horror',  'Sci', 'Fi', 'Reality']
    # determine keywords for excluding 

        info = pd.read_csv('program/data_sources/Additional_info_by_Movie_Target_kids.csv').drop(columns=['Unnamed: 0'])
    # reading csv file with our new additional info

        df = df.merge(info, how='left', right_on='Title', left_on='title')
    # merging 2 DF one parent , second previous

        df['director'] = np.where(df['director'].isna(), df['Director'], df['director'])
    # checking and comparing info about directors from both info-sources

        df['imdbVotes'] = df['imdbVotes'].str.replace(',', '').astype('float64', errors='ignore')
    # change dtype column imdVotes to float

        df = df.drop(columns = df.iloc[:,[4,6,9,11,13,14,17,18,20]].columns)
    # drop not needed columns

        pattern = '|'.join(Not_Related_Genres)
    # preparation keywords for excluding  in pandas .loc function visible format

    # Use the pattern with str.contains() to filter the DataFrame
        df = df[~df['Genre'].str.contains(pattern, case=False, na=False)]
        
        Kids_content_with_additional_info_clear = df[df['release_2000_or_newer']=='yes']
    # drop movies under 2000 year
        
        return Kids_content_with_additional_info_clear
    


    def t17_add_popularity(self, df, path_directors_csv, path_gdp_csv):
    # TODO : Add all ratings to our target DF

    # TODO : Reading and merging dataframes with popular Directors and gdp in every country
        directors = pd.read_csv(path_directors_csv,sep=';',  low_memory=False)
        gdp_per_capacity = pd.read_csv(path_gdp_csv,  low_memory=False)
        df = df.merge(gdp_per_capacity, how='left', on='country')
        df['gdp_per_capita'] = df['gdp_per_capita'].astype('float64', errors='ignore')

        
        df['popularity'] = np.where(df['gdp_per_capita'] > 30000, 2, 1)
    # where in column gdp < 30k input 0 scores

        df['popularity'] = np.where(df['director'].isin(directors['director'].tolist()), 3, df['popularity'])
    # where movie has popular director input 2 scores


    # TODO : working with <qcut> and divide all movies on 3 accurate parts [0-30%; 30%-70%; 70-100%] in global rating popularity

        df['imdbRating_Scores_3Stars'] = pd.qcut(df['imdbRating'], q=[0,0.3, 0.7, 1], labels=[1, 2, 3]).astype('float64', errors='ignore').fillna(0)
        df['imdbVotes_Scores_3Stars'] = pd.qcut(df['imdbVotes'], q=[0,0.3, 0.7, 1], labels=[1, 2, 3]).astype('float64', errors='ignore').fillna(0)

    # TODO : creating rating grounded by awards
        score_dict = {
            ('nominations', 'nomination'): 1,
            ('wins', 'Won', 'win'): 2,
            ('wins'): 3,
            ( 'Award'): 2,
            ( 'BAFTA', 'Primetime'): 4,
            ( 'Emmy'): 5,
            ( 'Emmys'): 6,
            ( 'Oscar'): 7,
            ( 'Oscars'): 8,
        }
        def calculate_new_score(awards_str):
            if pd.isnull(awards_str) or not awards_str.strip():
                return 0
            score = 0
            for words, points in score_dict.items():
                for word in words:
                    if word in str(awards_str):
                        score += points
                        #break  # Break once any of the words is found
            return score

    # apply algo with sum scores that movie received
        df['Awards_qScores'] = df['Awards'].apply(calculate_new_score)#.astype('int', errors='ignore').fillna(0)
    # qcut this column from 1 till 5 stars by rating awards

        non_zero_df = df[df['Awards_qScores'] > 0]
    # Calculate quantiles for non-zero values and divide into 5 equal parts
        quantiles = pd.qcut(non_zero_df['Awards_qScores'], q=[0, 0.2, 0.4, 0.6, 0.8, 1], labels=[1,2,3,4,5])
    # Replace non-zero values with quantiles
        df.loc[df['Awards_qScores'] > 0, 'Awards_qScores_5Stars'] = quantiles
        df['Awards_qScores_5Stars'] = np.where(df['Awards_qScores_5Stars'].isna(), 0, df['Awards_qScores_5Stars'])



    # Count total rating by all scores
        df['Total_Rating'] = (df['Awards_qScores_5Stars'] + df['imdbVotes_Scores_3Stars'] + df['imdbRating_Scores_3Stars'] + df['popularity']).astype('int')
    # cut this column from 1 till 5 stars by rating awards
        df['Total_Rating_5Stars'] = pd.cut(df['Total_Rating'], bins=5, labels=[1, 2, 3, 4, 5])
  

        shows_for_kids_recommendation = df.iloc[:, [0,1,10, 17,18,19,21,23]]
        print(shows_for_kids_recommendation)
        return shows_for_kids_recommendation


    def insert_Result_intoTable(self, df):
        df.to_sql('SHOWS_FOR_KIDS_RECOMMENDATION', self.conn, if_exists='replace', index=False, method='multi')
        df.to_csv('program/data_result_load/shows_for_kids_recommendation.csv', index = False)





def main_t16_19():
    db = Database()
    db.connect('program/database/netflix_database.db')

    all_Df = db.save_data_toDF()  # SELECT DF FROM TABLE from NETFLIX_COMBINED_CLEANED and save to csv

    filter_double_faced_content = db.t16_clear_noKids_films(all_Df)  # Target all KIDS related content

    Kids_content_with_additional_info_clear = db.t16_5_Additional_info_by_Movie_Target_kids_NEWDF_NEWTABLE(filter_double_faced_content)  
    # merge parent DF with additional info

    shows_for_kids_recommendation = db.t17_add_popularity(Kids_content_with_additional_info_clear, 'program/data_sources/popular_directors.csv',\
                          'program/data_sources/gdp_per_capita.csv')

    db.insert_Result_intoTable(shows_for_kids_recommendation)
    db.close()
    

    return filter_double_faced_content

if __name__ == '__main__':
    main_t16_19()