# Operating system imports 
import os 
import dotenv
dotenv.load_dotenv()

# Pandas imports 
import pandas as pd

# Date & Time imports 
import datetime as dt

# Web requests
import requests

# Yahoo imports 
import yfinance as yf

# Paths to folder
cwd = os.getcwd()
annual_data_folder = f"{cwd}\\Storage\\AnnualData"
quarter_data_folder = f"{cwd}\\Storage\\QuarterData"

fmp_key = os.getenv("fmp_key")

class StorageManager:
    def __init__(self, ticker: str, verbose_error: bool = False, verbose_update: bool = False):
        self.ticker = ticker
        self.verbose_error = verbose_error
        self.verbose_update = verbose_update
        
        # Period parameters. 
        self.annual_params = ["Annual", "annual", "A", "a"]
        self.quarter_params = ["Quarter", "quarter", "Quarterly", "quarterly", "Q", "q"]
        
        self.fmp_root_url = "https://financialmodelingprep.com/api/v3/{}/{}?limit={}&apikey={}"
    '''-----------------------------------'''
    def get_financial_statement(self, financial_statement: str = "income_statement", period: str = "Annual"):
        """
        :param:
        
        :returns: 
        
        Description: 
        """
        
        # --- Annual Logic ---
        if period in self.annual_params:
            
            
            
            file_path = f"{annual_data_folder}\\{self.ticker}\\{self.ticker}_{financial_statement}.csv"
            # Check if the folder to the ticker exists. 
            if not os.path.exists(path=f"{annual_data_folder}\\{self.ticker}"):
                # If the folder does not exist, create it. 
                os.mkdir(path=f"{annual_data_folder}\\{self.ticker}")
        
        
            try:
                df = pd.read_csv(file_path)
                df = df.set_index("Unnamed: 0")
                df.index.name = "index"
                
                outdated = self.is_outdated(df=df)
                
                if self.verbose_update:
                    print(f"[StorageManager] {financial_statement} retrieved from csv file: {file_path}  ")
            # If the file does not exist. 
            except FileNotFoundError:
                if financial_statement == "income_statement":
                    fmp_endpoint = "income-statement"
                elif financial_statement == "balance_sheet":
                    fmp_endpoint = "balance-sheet-statement"
                elif financial_statement == "cash_flow":
                    fmp_endpoint = "cash-flow-statement"
                # Query financialmodellingprep.com 
                data = requests.get(self.fmp_root_url.format(fmp_endpoint, self.ticker, 20, fmp_key))
                data = data.json()
                
                # Create a dataframe for the incomestatement. 
                df = pd.DataFrame(data)
                # Swap row labels with column labels. 
                df = df.T
                # Reverse the columns so the newest date is on the right side. 
                df = df[df.columns[::-1]]
                # Rows to remove 
                rows_to_remove = ["acceptedDate"]
                df.columns = df.loc["date"]
                df = df.drop("date") # Drop leftover date row. 
                df = self.add_stock_prices(df=df, period=period)
                
                # Write this data to the csv file. 
                df.to_csv(file_path)
                
                if self.verbose_update:
                    print(f"[StorageManager] {financial_statement} retrieved from 'financialmodellingprep.com' ")
        
        return df
        # --- Quarter Logic ---
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    def add_stock_prices(self, df: pd.DataFrame, period: str = "annual"):
        """
        :param df: Dataframe to add stock prices to. 
        
        :returns: The same dataframe passed in, but with new rows for the stock price. 
        
        Description: The dataframe will contain columns where each column represents an annual report.
                     This function will add the high, low, and average of the stock price for that period to the existing dataframe. 
                     Then it will return the existing dataframe with the new rows.  
        """
        
        # Get the first year from the dataframe. 
        date_data_points = df.columns
        
        start_date = date_data_points[0]
        end_date = date_data_points[-1]
        
        # Parse the dates 
        start_year, start_month, start_day = start_date.split("-")
        end_year, end_month, end_day = end_date.split("-")
        
        
        index = 0
        annual_prices_collected = [] 
        for i in range(int(start_year), int(end_year)+1):
            annual_prices = {}
            # Skip the first index. Since this is the first column in our dataframe, there is no previous column to reference. 
            if index < len(date_data_points):
                if index == 0:
                    # When index is 0, we are working with our first column. Meaning we have not dates before this. 
                    # So we use the columns date as the end date, subtract one year from it, and use that as the start date. 
                    index_end_date = date_data_points[index]
                    index_end_year, index_end_month, index_end_day = index_end_date.split("-")
                    index_start_year = int(index_end_year) - 1
                    index_start_date = f"{index_start_year}-{index_end_month}-{index_end_day}"
                    period = f"{index_start_date} - {index_end_date}"
                else:
                    
                    index_start_date = date_data_points[index-1]
                    index_end_date = date_data_points[index]
                    
                    period = f"{index_start_date} - {index_end_date}" 
                
                
                annual_data = yf.download(self.ticker, start=index_start_date, end=index_end_date)
                
                # Parse the annual data. 
                annual_prices["date"] = index_end_date
                annual_prices["startPeriod"] = index_start_date
                annual_prices["endPeriod"] = index_end_date
                annual_prices["high"] = round(annual_data["High"].max(), 2)
                annual_prices["low"] = round(annual_data["Low"].min(), 2)
                try:
                    annual_prices["average"] = round(annual_data["Close"].mean(), 2)
                except ValueError:
                    annual_prices["average"] = "N\A"
                
                
                annual_prices_collected.append(annual_prices)
            else:
                pass    
                
            index += 1
            
        prices_df = pd.DataFrame(annual_prices_collected)
        # Transpose the dataframe (swap the rows with the columns). 
        prices_df = prices_df.T
        # Set the columns as the values of the date row. 
        prices_df.columns = prices_df.loc["date"]
        # Drop the date row that is left over. 
        prices_df = prices_df.drop("date")
        # Concat the dataframes, to add the prices_df dataframe to the dataframe passed in the parameter of the function. 
        result = pd.concat([df, prices_df])
        
        return result
    '''-----------------------------------'''
    '''-----------------------------------'''
    def is_outdated(self, df: pd.DataFrame, considered_outdated: float = 12.5, warning_message: bool = True) -> bool:
        """
        :param df: Dataframe with columns of financial data. 
        :param considered_outdated: The amount of time that the user guages is outdated. NOTE: This variable controls the boolean return of this function. 
        :param warning_message: Determine if warning readouts should be displayed. 
        
        Description: Check the dates in the columns of the dataframe. 
        """
        
        filing_dates = list(df.loc["fillingDate"])
        # Get the current date. 
        current_date = dt.datetime.now()
        # Create datetime object for filing date. 
        recent_filing_obj = dt.datetime.strptime(filing_dates[-1], "%Y-%m-%d")
        
        # Calculate the difference between dates and get the total seconds.
        difference = (current_date - recent_filing_obj).total_seconds()
        
        # The amount of seconds in a month. 
        seconds_in_month = 30.44 * 24 * 60 * 60 # 30.44 days per month * 24 hours * 60 minutes * 60 seconds 
        
        months_difference = difference / seconds_in_month 
        
        if months_difference >= considered_outdated:
           return True
        else: 
           return False
    '''-----------------------------------'''
    '''-----------------------------------'''
    """
    :param:
    
    :returns: 
    
    Description: 
    """
    """
    :param:
    
    :returns: 
    
    Description: 
    """
    """
    :param:
    
    :returns: 
    
    Description: 
    """
    """
    :param:
    
    :returns: 
    
    Description: 
    """
    
    