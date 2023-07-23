import sqlite3

class Database:
    def __init__(self):
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


    def create_tables(self):
        try:
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS GDP_PER_CAPITA (
                    country TEXT PRIMARY KEY,          
                    gdp_per_capita REAL
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS RATINGS (
                    id INTEGER PRIMARY KEY,
                    name TEXT 
                )
            ''')
            
            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS NETFLIX_SHOWS (
                    show_id TEXT PRIMARY KEY,
                    type TEXT,
                    title TEXT,
                    director TEXT,
                    cast TEXT,
                    country TEXT,
                    date_added TEXT,
                    release_year INTEGER,
                    rating INTEGER,
                    duration TEXT,
                    listed_in TEXT,
                    description TEXT,
                                                  
                    FOREIGN KEY (rating) REFERENCES RATINGS(id)                              
                )
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS Additional_info_by_Movie_Target_kids (
                                Title           TEXT  PRIMARY KEY,
                                Year            TEXT,
                                Rated           TEXT,                               
                                Genre           TEXT,
                                Director        TEXT,                               
                                Plot            TEXT,
                                Language        TEXT,
                                Country         TEXT,
                                Awards          TEXT,                               
                                Ratings         TEXT,
                                imdbRating      TEXT,
                                imdbVotes       TEXT                                                    
                )                     
            ''')

            self.cursor.execute('''
                CREATE TABLE IF NOT EXISTS SHOWS_FOR_KIDS_RECOMMENDATION (
                                show_id         TEXT,  
                                type            TEXT,
                                Genre           TEXT,                               
                                popularity           INTEGER,
                                imdbRating_qScores   INTEGER,                               
                                imdbVotes_qScores    INTEGER,
                                Awards_qScores       INTEGER,
                                Total_Rating         INTEGER                                                 
                )                     
            ''')


        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")

def main_t10():

    db = Database()
    db.connect('/program/database/netflix_database.db')
    db.create_tables()
    db.close()

if __name__ == '__main__':
    main_t10()




