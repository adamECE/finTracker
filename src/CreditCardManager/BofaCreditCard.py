import os
import re 
import sys
import pathlib 

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

    
    def getRollupPayments(self) -> None:
        # should probably be in base class 
        breakpoint()
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

