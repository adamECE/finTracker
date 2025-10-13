import os
import re 
import sys
import pathlib 

# Import repo dependencies 
match = re.search(r".*fintracker\\src", os.path.abspath(__file__))
src_path = str(pathlib.Path(match.group()))
if src_path not in sys.path:
    sys.path.append(src_path)

from DB_Interface_Base import DB_Interface_Base

DB_TABLES = ['''
CREATE TABLE category_map (
    category  TEXT NOT NULL,
    value     TEXT NOT NULL
);
''']

class DataCategorizationDb(DB_Interface_Base):
    """
    @brief      Interface class for managing data categorizations
    @param      base_db_path : Directory intending to contain database file
    """
    def __init__(self, base_db_path):
        super().__init__("dataCategorizations.db", base_db_path, DB_TABLES)
    

    def _fetch_dict(self):
        """
        @brief  Abstract method implementation for handling entire database extraction 
        """ 
        return self._readDb("SELECT category, value FROM category_map")


class DataCategorizer:
    def __init__(self, base_db_path : pathlib.Path):
        self.db_handle = DataCategorizationDb(base_db_path)