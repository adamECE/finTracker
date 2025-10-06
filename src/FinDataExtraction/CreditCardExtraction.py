import os 
import pathlib 
import pandas as pd 

class CreditCardExtraction: 
    def __init__(self, excel_path : pathlib.Path):
        self.bofa_cc_df = None 

        # Conert excel or csv to df 
        if os.path.exists(excel_path):
            if excel_path.suffix.lower() == ".csv": 
                self.bofa_cc_df = pd.read_csv(excel_path)
            elif excel_path.suffix.lower() == ".xlsx": 
                self.bofa_cc_df = pd.read_excel(excel_path)
            else:
                raise ValueError(f"Unsupported file: {excel_path}. Must be csv of xlsx.")
        else:
            raise FileExistsError(f"Excel path {excel_path} DNE")
        
    
    def getCreditCardDF(self) -> pd.DataFrame: 
        return self.bofa_cc_df


    
