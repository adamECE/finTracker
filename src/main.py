import pathlib 
import argparse
from src.config.env_vars import * 
from FinDataExtraction.CreditCardExtraction import CreditCardExtraction
from DB_Interface import DB_Interface_Base

def SetupOpts(): 
    parser = argparse.ArgumentParser(description = "Financial Tracker Application")

    parser.add_argument("-e", "--excel-path", dest = "excel_path", type  = pathlib.Path, 
                        help = "Path to BofA excel export" )

    return parser.parse_args() 

if __name__ == "__main__":
    args = SetupOpts() 
    
    cc_handle = CreditCardExtraction(args.excel_path)  