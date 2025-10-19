import os
import re 
import sys
import pathlib 
import pandas as pd
from contextlib import contextmanager

# Import repo dependencies 
match = re.search(r".*fintracker\\src", os.path.abspath(__file__))
if match:
    src_path = str(pathlib.Path(match.group()))
    if src_path not in sys.path:
        sys.path.append(src_path)

from CreditCardManager.CreditCardExtraction import CreditCardExtractorBase



class BofaCreditCard(CreditCardExtractorBase):
    def __init__(self, name):
        super().__init__(name, 'BANK_OF_AMERICA')

    
    def ___payemntDataProcessing___(self) -> None:
        '''
        @brief  Apply post extraction processing to self.credit_card_df
        @note   Implements abstract method from CreditCardExtractorBase
        '''        
        # Determine base store names 
        self.__determine_base_payee_name__()

        # For now, just remove cc payment (any positive value)
        self.credit_card_df = self.credit_card_df[self.credit_card_df['Amount'] <= 0]

        # Turn amount paid into a positive value          
        self.credit_card_df['Amount'] = self.credit_card_df['Amount'] * -1 

    
    @contextmanager
    def ___safe_apply___(self):
        temp_df = self.credit_card_df.copy()
        yield temp_df 
        self.credit_card_df['Payee'] = self.credit_card_df['Payee'].fillna(temp_df['Payee'])
        
    
    def __determine_base_payee_name__(self):
        # Create a copy of the original df for re-insertion
        # with self.___safe_apply___() as temp_df :
        #     self.credit_card_df['Payee'] = temp_df['Payee'].apply(lambda x: ' '.join(x.split()[:-2]))
        breakpoint()
        with self.___safe_apply___() as temp_df :
            self.credit_card_df['Payee'] = temp_df['Payee'].apply(lambda x: ' '.join(x.split()[:3]))
        
        # REmove TST* from string (TST* is just a POS payment processor tag)
        with self.___safe_apply___() as temp_df :
            self.credit_card_df['Payee'] = temp_df['Payee'].str.replace(r'^TST\*', '', regex=True)

        # Split based on store number i.e. #123 
        with self.___safe_apply___() as temp_df :
            self.credit_card_df['Payee'] = self.credit_card_df['Payee'].str.split('#').str[0] 

        # Split based on any integer that occurs after an alphabetical character 
        with self.___safe_apply___() as temp_df :
            self.credit_card_df['Payee'] = temp_df['Payee'].str.extract(r'^(.*?[A-Za-z])(?=\d)') 


    def getRollupPayments(self) -> None:
        # should probably be in base class 
        return self.credit_card_df.groupby('Payee', as_index=False)['Amount'].sum() 


    def getDfColumnMapping(self) -> dict:
        '''
        @brief  Get a dictionary mapping of which dataframe columns map to which value in the database
        @note   Implements abstract method from CreditCardExtractorBase
        '''
        df_col_mappings = {
            "payment_date"   : "Posted Date", 
            "payee"          : "Payee",
            "amount_paid"    : "Amount"
        }

