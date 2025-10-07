import os
import pathlib 
import sqlite3 
import argparse
import pandas as pd 
from datetime import datetime 

DB_NAME   = "finTracker.db"
DB_TABLES = ['''
CREATE TABLE credit_cards_table (
    credit_card_name    TEXT PRIMARY KEY,
    issuer              TEXT,
    card_type           TEXT
);
''',
'''
CREATE TABLE credit_card_payments (
    payment_id          INTEGER PRIMARY KEY AUTOINCREMENT,
    credit_card_name    TEXT NOT NULL,
    payment_date        DATE NOT NULL,
    amount_paid         REAL NOT NULL,
    payee               TEXT NOT NULL,
    FOREIGN KEY (credit_card_name) REFERENCES credit_cards(credit_card_name)
        ON DELETE CASCADE
        ON UPDATE CASCADE
);
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
        self.___connect___() 
        self.___initTable___()
        self.___close___() 

    
    def __del__(self):
        self.___close___()


    def ___connect___(self): 
        """
        @brief  Connect to SQLite3 db 
        """
        try: 
            self.connection = sqlite3.connect(self.db_path)
            self.cursor     = self.connection.cursor()
        except sqlite3.Error as err: 
            print(f"Connection error: {err}") 


    def ___initTable___(self): 
        """
        @brief  Create table 
        """
        try: 
            for table in DB_TABLES: 
                self.cursor.execute(table)
            self.connection.commit()
        except sqlite3.Error as err: 
            self.connection.rollback()


    def ___close___(self):
        """
        @brief  Closes db connection 
        """
        if not self.connection:
            print("[Warning] No valid connection to close")
        else: 
            try: 
                self.connection.close()
            except sqlite3.Error as err:
                print(f"Error closing connection: {err}") 


    def exportToCsv(self):
        """
        @brief  Export a table from the SQLite DB to a CSV file. Primarily for debugging. 
        @param  table_name  : Name of the table to export
        @param  output_path : Path to save the CSV file
        """
        self.___connect___() 
        
        # Grab data for export  
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        cur_table = "NO_TABLE_SELECTED_YET" 


        try:
            # Get all table names
            self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [row[0] for row in self.cursor.fetchall()]

            for table in tables:
                query       = f"SELECT * FROM {table}"
                cur_table   = table 
                df          = pd.read_sql_query(query, self.connection)
                output_path = os.path.join(self.base_db_path, f"{table}_{timestamp}.csv")

                # Export csv
                df.to_csv(output_path, index=False)
                print(f"[Success] Exported '{table}' to '{output_path}'")

        except Exception as err:
            print(f"[Error] Failed to export {cur_table}: {err}")
        
        self.___close___()


def SetupOpts(): 
    parser = argparse.ArgumentParser(description = "Financial Tracker Application Database -- use for debugging")

    parser.add_argument("-e", "--export", dest = "export", action = "store_true", 
                        help = "Export database as csv" )
    
    parser.add_argument("-d", "--db-path", dest = "db_path", type = pathlib.Path, 
                        help = "Path to database directory" )


    return parser.parse_args() 


if __name__ == "__main__":
    args = SetupOpts() 

    db_handle = DB_Interface_Base(args.db_path)
    
    if args.export:
        db_handle.exportToCsv() 