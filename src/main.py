import pathlib 
import argparse
from FinDataExtraction.CreditCardExtraction import CreditCardExtraction

def SetupOpts(): 
    parser = argparse.ArgumentParser(description = "Financial Tracker Application")

    parser.add_argument("-e", "--excel-path", dest = "excel_path", type  = pathlib.Path, 
                        help = "Path to BofA excel export" )

    return parser.parse_args() 

if __name__ == "__main__":
    args = SetupOpts() 
    
    cc_handle = CreditCardExtraction(args.excel_path)  