import sqlite3

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

    
    def get_relations(self):
        # Create a cursor object to execute SQL queries
        self.cursor = self.conn.cursor()
        # Get all tables in the database
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        # Retrieve table relations and key information
        relations = {}
        for table in tables:
            table_name = table[0]
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            self.cursor.execute(f"PRAGMA foreign_key_list({table_name})")
            foreign_keys = self.cursor.fetchall()
            relations[table_name] = {
            'related_tables': [fk[2] for fk in foreign_keys],
            'primary_key': [col[1] for col in columns if col[5] == 1],
            'foreign_key':
            [col[1] for col in columns if col[1] in [fk[3] for fk in foreign_keys]]
            }
        # Print the table relations with key information
        print()
        for table, data in relations.items():
            print(f"Table: {table}")
            print("Related Tables: ", ", ".join(data['related_tables']))
            print("Primary Key: ", ", ".join(data['primary_key']))
            print("Foreign Key: ", ", ".join(data['foreign_key']))
            print()



    def show_table_schema(self, table_name):
        import pandas as pd
        print("")
        print(f"schema for table {table_name}")
        print("")
        # Query the schema information
        query = f"PRAGMA table_info({table_name})"
        schema_df = pd.read_sql_query(query, self.conn)
        # Display the schema DataFrame
        print(schema_df)


    def show_all_tables(self):
        import pandas as pd
        # Query the schema information
        query = "SELECT name FROM sqlite_schema WHERE type ='table' AND name NOT LIKE 'sqlite_%'"
        all_tables = pd.read_sql_query(query, self.conn)
        # Display the schema DataFrame
        print(all_tables)


    def show_data_from_table(self, table):
        import pandas as pd
        query = f"SELECT * FROM {table}"
        data = pd.read_sql_query(query, self.conn)
        print(f"showing data columns sql table {table}")
        print(data.columns)
        print(f"showing data from sql table {table}")
        print(data)


def main():
    db = Database()
    db.connect('program/database/netflix_database.db')

    db.get_relations()
    #db.show_table_schema('NETFLIX_SHOWS')
    db.show_all_tables()
    db.show_data_from_table('SHOWS_FOR_KIDS_RECOMMENDATION')

    db.close()

if __name__ == '__main__':
    main()