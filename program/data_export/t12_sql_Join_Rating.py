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


    def newTable_withJoin(self):
        # TODO : Craete and JOIN NETFLIX_SHOWS column <rating> with Ratings column <name>

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS NETFLIX_META_WITH_RATING AS 
        WITH updated_ratings AS (
            SELECT NS.*, R.name AS rating_name
            FROM NETFLIX_SHOWS NS
            LEFT JOIN RATINGS R ON NS.rating = R.id
        )
        SELECT 
            ur.show_id, 
            ur.type, 
            ur.title, 
            ur.director, 
            ur.cast, 
            ur.country, 
            ur.date_added, 
            ur.release_year, 
            ur.rating_name AS rating, 
            ur.duration, 
            ur.listed_in, 
            ur.description	
        FROM updated_ratings AS ur;
        """)

def main_t12():

    db = Database()
    db.connect('program/database/netflix_database.db')
    db.newTable_withJoin()
    db.close()

if __name__ == '__main__':
    main_t12()