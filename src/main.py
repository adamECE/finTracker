import pathlib 
import argparse
from config.env_vars import * 
from FinDbManager.CreditCardDB import CreditCardDB
from CreditCardManager.BofaCreditCard import BofaCreditCard
from ReportGenerator.PlotGenerator import PlotGenerator
from ReportGenerator.HtmlReportGenerator import BuildHtmlReport
from CreditCardManager.DataCategorization.DataCategorizer import DataCategorizer, DataCategorizationDb


def SetupOpts(): 
    parser = argparse.ArgumentParser(description = "Financial Tracker Application")

    parser.add_argument("-e", "--excel-path", dest = "excel_path", type  = pathlib.Path, 
                        help = "Path to BofA excel export" )

    return parser.parse_args() 


if __name__ == "__main__":
    args = SetupOpts() 
    
    # Extract credit card data
    cc_handle = BofaCreditCard(args.excel_path)  
    cc_handle.extractCreditCardFromExcelOrCsv(args.excel_path)
    cc_df = cc_handle.getRollupPayments()

    # Categorize Data     
    data_categorizer_handle = DataCategorizer(CATEGORIZATION_DB_PATH)
    data_categorizer_handle.categorizeFromArray(list(cc_df['Payee']))

    # Build Report
    plot_gen_handle = PlotGenerator(FIN_DB_PATH)
    fig = plot_gen_handle.createBarChartFromDf(cc_df, 'Payee', 'Amount', 'test')
    html_handle = BuildHtmlReport(None, "TEST NAME")
    html_handle.appendFig(fig)
    html_handle.finalizeHtml()

    # handle = DataCategorizer(CATEGORIZATION_DB_PATH)