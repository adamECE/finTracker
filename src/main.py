import pathlib 
import argparse
from config.env_vars import * 
from DB_Interface import DB_Interface_Base
from CreditCardManager.BofaCreditCard import BofaCreditCard
from ReportGenerator.PlotGenerator import PlotGenerator

def SetupOpts(): 
    parser = argparse.ArgumentParser(description = "Financial Tracker Application")

    parser.add_argument("-e", "--excel-path", dest = "excel_path", type  = pathlib.Path, 
                        help = "Path to BofA excel export" )

    return parser.parse_args() 


if __name__ == "__main__":
    args = SetupOpts() 
    
    cc_handle = BofaCreditCard(args.excel_path)  
    cc_handle.extractCreditCardFromExcelOrCsv(args.excel_path)
    cc_df     = cc_handle.getRollupPayments()

    plot_gen_handle = PlotGenerator(DB_PATH)
    print(len(cc_df))
    plot_gen_handle.createPieChart(
        title="test",
        width=6,
        height=6,
        labels=cc_df['Payee'],
        sizes=cc_df['Amount']
    )  