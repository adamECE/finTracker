import os
import re 
import sys 
import pathlib 
import sqlite3 
import argparse
import pandas as pd 
from datetime import datetime 

# Import repo dependencies 
match = re.search(r".*fintracker\\src", os.path.abspath(__file__))
if match:
    src_path = str(pathlib.Path(match.group()))
    if src_path not in sys.path:
        sys.path.append(src_path)

from DB_Interface_Base import DB_Interface_Base

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

class CreditCardDB(DB_Interface_Base):
    def __init__(self, base_db_path : pathlib.Path):
        super().__init__(DB_NAME, base_db_path, DB_TABLES)


    def _fetch_dict(self):
        """
        @brief  Abstract method impleentation for handling entire database extraction 
        """ 
        return self._readDb("SELECT * FROM credit_card_payments")


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