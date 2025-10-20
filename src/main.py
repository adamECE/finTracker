import pathlib 
import argparse
from config.env_vars import * 
from FinDbManager.CreditCardDB import CreditCardDB
from CreditCardManager.BofaCreditCard import BofaCreditCard
from ReportGenerator.PlotGenerator import PlotGenerator
from CreditCardManager.DataCategorization.DataCategorizer import DataCategorizer, DataCategorizationDb

def SetupOpts(): 
    parser = argparse.ArgumentParser(description = "Financial Tracker Application")

    parser.add_argument("-e", "--excel-path", dest = "excel_path", type  = pathlib.Path, 
                        help = "Path to BofA excel export" )

    return parser.parse_args() 


if __name__ == "__main__":
    args = SetupOpts() 
    
    cc_handle = BofaCreditCard(args.excel_path)  
    cc_handle.extractCreditCardFromExcelOrCsv(args.excel_path)
    cc_df = cc_handle.getRollupPayments()

    plot_gen_handle = PlotGenerator(FIN_DB_PATH)
    # plot_gen_handle.createPieChart(
    #     title="test",
    #     width=6,
    #     height=6,
    #     labels=cc_df['Payee'],
    #     sizes=cc_df['Amount']
    # )  

    # data_categorizer_handle = DataCategorizer(CATEGORIZATION_DB_PATH)
    # data_categorizer_handle.categorizeFromArray([x for x in cc_df['Payee']])

    plot_gen_handle.createBarChartFromDf(cc_df, 'Payee', 'Amount', 'test')

    cat_db_handle = DataCategorizationDb(CATEGORIZATION_DB_PATH)
    cat_db_handle.exportToCsv()
    # handle = DataCategorizer(CATEGORIZATION_DB_PATH)