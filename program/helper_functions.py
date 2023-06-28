def start_sql_interactive_shell(conn):
  print("### Welcome to the SQL interactive shell ###")
  print("")
  print('You can now just use SQL statements like "SELECT * FROM Countries".')
  print('If you want to exit the shell just type in "quit" and then hit enter')
  print("")
  cursor = conn.cursor()
  # Enter the interactive shell
  while True:
    command = input('sqlite> ')
    if command == 'quit':
      break
    cursor.execute(command)
    for row in cursor.fetchall():
      print(row)
  # Close the cursor and connection
  cursor.close()
  conn.close()


def get_relations(conn):
  # Create a cursor object to execute SQL queries
  cursor = conn.cursor()
  # Get all tables in the database
  cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
  tables = cursor.fetchall()
  # Retrieve table relations and key information
  relations = {}
  for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()
    cursor.execute(f"PRAGMA foreign_key_list({table_name})")
    foreign_keys = cursor.fetchall()
    relations[table_name] = {
      'related_tables': [fk[2] for fk in foreign_keys],
      'primary_key': [col[1] for col in columns if col[5] == 1],
      'foreign_key':
      [col[1] for col in columns if col[1] in [fk[3] for fk in foreign_keys]]
    }
  # Print the table relations with key information
  for table, data in relations.items():
    print(f"Table: {table}")
    print("Related Tables: ", ", ".join(data['related_tables']))
    print("Primary Key: ", ", ".join(data['primary_key']))
    print("Foreign Key: ", ", ".join(data['foreign_key']))
    print()
  # Close the cursor and connection
  cursor.close()
  conn.close()
