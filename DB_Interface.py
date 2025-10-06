import os
import sys 
import pathlib 
import sqlite3 

DB_NAME = "finTracker.db"

db_tables = [
    '''
''' 
]

class DB_Interface_Base:
    def __init__(self, base_db_path : pathlib.Path):
        if not os.path.exists(base_db_path):
            raise FileNotFoundError(f"Directory path DNE: {base_db_path}")
        
        # Init variables
        self.base_db_path   = base_db_path
        self.db_path        = os.path.join(base_db_path, DB_NAME)
        self.connection     = None 
        self.cursor         = None

        # Init db 
        self.connect() 
        self.initTable()

    
    def connect(self): 
        """
        @brief  Connect to SQLite3 db 
        """
        try: 
            self.connection = sqlite3.connect(self.db_path)
            self.cursor     = self.connection.cursor()
        except sqlite3.Error as err: 
            print(f"Connection error: {err}") 


    def initTable(self): 
        """
        @brief  Create table 
        """
        self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS creditCards (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL
                ) 
        ''')

    def close(self):
        if not self.connection:
            print("[Warning] No valid connection to close")
        else: 
            try: 
                self.connection.close()
            except sqlite3.Error as err:
                print(f"Error closing connection: {err}") 
