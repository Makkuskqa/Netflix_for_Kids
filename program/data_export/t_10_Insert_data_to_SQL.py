import sqlite3
import pandas as pd

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

    
    def csv_source(self):
        df1 = pd.read_csv('/program/data_sources/gdp_per_capita.csv')
        df2 = pd.read_csv('/program/data_sources/netflix_shows.csv',sep=';',  low_memory=False)
        df3 = pd.read_csv('/program/data_sources/ratings.csv').drop_duplicates()

        df1.to_sql('GDP_PER_CAPITA', con = self.conn, if_exists='append', index=False)
        df2.to_sql('NETFLIX_SHOWS', con = self.conn, if_exists='append', index=False)
        df3.to_sql('RATINGS', con = self.conn, if_exists='append', index=False)



def main_t10_1():

    db = Database()
    db.connect('/program/database/netflix_database.db')
    db.csv_source()
    db.close()

if __name__ == '__main__':
    main_t10_1()