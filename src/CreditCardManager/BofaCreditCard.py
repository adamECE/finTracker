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
        # For now, just remove cc payment (any positive value)
        self.credit_card_df = self.credit_card_df[self.credit_card_df['Amount'] <= 0]

        # Turn amount paid into a positive value          
        self.credit_card_df['Amount'] = self.credit_card_df['Amount'] * -1 

        # Determine base payee names 
        self.__determine_base_payee_name__()
    
    @contextmanager
    def ___safe_apply___(self):
        temp_df = self.credit_card_df.copy()
        yield temp_df 
        self.credit_card_df['Payee'] = self.credit_card_df['Payee'].fillna(temp_df['Payee'])
        
    
    def __determine_base_payee_name__(self):
        for i in self.credit_card_df.index:
            full_payee_str = self.credit_card_df.at[i, 'Payee']

            # *** Parse unnecessary characters to extract store name 
            # Remove the last two words, which will always be the city+state 
            full_payee_str = " ".join(full_payee_str.split()[:-2])

            # Remove POS label 
            full_payee_str = full_payee_str.replace('TST*', '')
            full_payee_str = full_payee_str.replace('SPO*', '')

            # Remove any '#' marked store id's
            full_payee_str = full_payee_str.split('#')[0]

            # Remove the all text after first instance of a character that appears after an alphabetical character
            alphabetical_character_found = False 
            for char_idx in range(len(full_payee_str)):
                # Find index of first numerical character
                if alphabetical_character_found and full_payee_str[char_idx].isdigit():
                    full_payee_str = full_payee_str[:char_idx]
                    break

                # Mark first instance of an alphabetical character 
                if full_payee_str[char_idx].isalpha():
                    alphabetical_character_found = True 

            # Finally update string 
            self.credit_card_df.at[i, 'Payee'] = full_payee_str.strip()


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

