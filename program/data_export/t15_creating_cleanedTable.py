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


    def show_Views(self):
        # TODO : show all created views
        query = ("""SELECT name, sql
        FROM sqlite_master
        WHERE type = 'view';""")

        all_tables = pd.read_sql_query(query, self.conn)
        print(all_tables)
        


    def create_New_Cleaned_Table(self):
        # TODO : Craete new Cleaned Table
        
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS NETFLIX_COMBINED_CLEANED AS
            SELECT 
                *, 
                CASE WHEN release_year >= 2000 THEN 'yes' ELSE 'no' END AS release_2000_or_newer
            FROM VIEW_NETFLIX_META_WITH_RATING;
        """)

        self.cursor.execute("""
            UPDATE NETFLIX_COMBINED_CLEANED
            SET country = COALESCE(country, 'unknown');
        """)

        self.cursor.execute("""
            UPDATE NETFLIX_COMBINED_CLEANED
            SET country = 'many'
            WHERE country LIKE '%,%';
        """)

        self.cursor.execute("""
            UPDATE NETFLIX_COMBINED_CLEANED
            SET title = REPLACE(title, '"', '')""")
        
        self.cursor.execute("""
            DELETE FROM NETFLIX_COMBINED_CLEANED
            WHERE "cast" IS NULL; """)
                
        self.conn.commit()


def main_t15():

    db = Database()
    db.connect('program/database/netflix_database.db')
    db.create_New_Cleaned_Table()
    db.show_Views()
    db.close()

if __name__ == '__main__':
    main_t15()