
# Pandas imports 
import pandas as pd
pd.options.display.float_format = "{:,.2f}".format

# Import storage manager
import Storage.storage_manager


class AssetManager:
    def __init__(self, ticker:str):
        self.ticker = ticker.upper()
        # Create StorageManager object. 
        self.storage = Storage.storage_manager.StorageManager(ticker=self.ticker)
    
        # Empty dataframes to hold financial statements. 
        self.income_statement = pd.DataFrame()
        self.balance_sheet = pd.DataFrame()
        self.cash_flow = pd.DataFrame()
        self.financial_metrics = pd.DataFrame()
        self.growth = pd.DataFrame()
        self.per_share_metrics = pd.DataFrame()
        self.margins = pd.DataFrame()
        self.expenses_metrics = pd.DataFrame()
    
    '''-----------------------------------'''
    def set_income_statement(self, period: str = "Annual"):
        """
        :param period: The timeframe to get the "income statement" for. Ex: Annual or Quarterly
        
        :returns: None
        
        Description: Set the income statement of the ticker set to the class var "self.ticker".
        """
        self.income_statement = self.storage.get_financial_statement(financial_statement="income_statement",period=period) 
    '''-----------------------------------'''
    def get_income_statement(self, period: str = "Annual"):
        """
        :param period: The timeframe to get the "balance sheet" for. Ex: Annual or Quarterly
        
        :returns: DataFrame
        
        Description: Get the income statement of the ticker set to the class var "self.ticker".
        """
        if self.income_statement.empty:
            self.set_income_statement(period=period)
        return self.income_statement
    '''-----------------------------------'''
    def set_balance_sheet(self, period: str = "Annual"):
        """
        :param period: The timeframe to get the "balance sheet" for. Ex: Annual or Quarterly
        
        :returns: None
        
        Description: Set the income statement of the ticker set to the class var "self.ticker".
        """
        self.balance_sheet = self.storage.get_financial_statement(financial_statement="balance_sheet",period=period)
    '''-----------------------------------'''
    def get_balance_sheet(self, period: str = "Annual"):
        """
        :param period: The timeframe to get the "income statement" for. Ex: Annual or Quarterly
        
        :returns: DataFrame
        
        Description: Get the income statement of the ticker set to the class var "self.ticker".
        """
        if self.balance_sheet.empty:
            self.set_balance_sheet(period=period)
        return self.balance_sheet
    '''-----------------------------------'''
    def set_cash_flow(self, period: str = "Annual"):
        """
        :param period: The timeframe to get the "cash flow" for. Ex: Annual or Quarterly
        
        :returns: None
        
        Description: Set the income statement of the ticker set to the class var "self.ticker".
        """
        self.cash_flow = self.storage.get_financial_statement(financial_statement="cash_flow",period=period)
    '''-----------------------------------'''
    def get_cash_flow(self, period: str = "Annual"):
        """
        :param period: The timeframe to get the "income statement" for. Ex: Annual or Quarterly
        
        :returns: DataFrame
        
        Description: Get the income statement of the ticker set to the class var "self.ticker".
        """
        if self.cash_flow.empty:
            self.set_cash_flow(period=period)
        return self.cash_flow
    '''-----------------------------------'''
    def set_metrics(self, period: str = "Annual"):
        """
        :param period: The timeframe of data to look at. 
        :returns: None
        
        Description: Add various financial ratios to the companies data. 
        """
        
        if self.income_statement.empty:
            self.set_income_statement(period=period)
        
        if self.balance_sheet.empty:
            self.set_balance_sheet(period=period)
        
        if self.cash_flow.empty:
            self.set_cash_flow(period=period)
            
        # Convert main rows to float. 
        revenue_row = self.income_statement.loc["revenue"].astype(float)
        netincome_row = self.income_statement.loc["netIncome"].astype(float)   
            
        self.financial_metrics["averagePrice"] = self.income_statement.loc["average"]
        self.financial_metrics["basicShares"] = self.income_statement.loc["weightedAverageShsOut"]
        self.financial_metrics["dilutedShares"] = self.income_statement.loc["weightedAverageShsOutDil"]

        # Convert columns to float. 
        self.financial_metrics["averagePrice"] = pd.to_numeric(self.financial_metrics["averagePrice"], errors="coerce", downcast="float")
        self.financial_metrics["basicShares"] = pd.to_numeric(self.financial_metrics["basicShares"], errors="coerce", downcast="float")
        self.financial_metrics["dilutedShares"] = pd.to_numeric(self.financial_metrics["dilutedShares"], errors="coerce", downcast="float")
        
        # --- Calculations --- 
        self.financial_metrics["marketcap"] = self.financial_metrics["averagePrice"] * self.financial_metrics["basicShares"]

        
        # Price to sales 
        self.financial_metrics["p/s"] = self.financial_metrics["marketcap"] / revenue_row
        # Earnings per share 
        self.financial_metrics["eps"] = self.income_statement.loc["eps"]
        self.financial_metrics["epsDiluted"] = self.income_statement.loc["epsdiluted"]
        # Price to earnings
        self.financial_metrics["p/e"] = self.financial_metrics["marketcap"] / netincome_row
        # Price to book
        self.financial_metrics["p/b"] = self.financial_metrics["marketcap"] / self.balance_sheet.loc["totalStockholdersEquity"].astype(float)
        # Price to free-cash-flow
        self.financial_metrics["p/fcf"] = self.financial_metrics["marketcap"] / self.cash_flow.loc["freeCashFlow"].astype(float)
        
        # --- Enterprise Value calculations --- 
        self.financial_metrics["enterpriseValue"] = self.financial_metrics["marketcap"] + self.balance_sheet.loc["netDebt"].astype(float)
        self.financial_metrics["ev/s"] = self.financial_metrics["enterpriseValue"] / revenue_row
        self.financial_metrics["ev/e"] = self.financial_metrics["enterpriseValue"] / netincome_row
        self.financial_metrics["ev/ebitda"] = self.financial_metrics["enterpriseValue"] / self.income_statement.loc["ebitda"].astype(float)
        self.financial_metrics["ev/fcf"] = self.financial_metrics["enterpriseValue"] / self.cash_flow.loc["freeCashFlow"].astype(float)
        self.financial_metrics["currentRatio"] = self.balance_sheet.loc["totalCurrentAssets"].astype(float) / self.balance_sheet.loc["totalCurrentLiabilities"].astype(float)
        self.financial_metrics["debt/equity"] = (self.balance_sheet.loc["totalDebt"].astype(float) / self.balance_sheet.loc["totalEquity"].astype(float)) * 100
        
        
        # --- Financial Metrics calculations. 
        self.financial_metrics["roa"] = (netincome_row / self.balance_sheet.loc["totalAssets"].astype(float)) * 100
        self.financial_metrics["roe"] = (netincome_row / self.balance_sheet.loc["totalStockholdersEquity"].astype(float)) * 100
        self.financial_metrics["roic"] = ( # ROIC = NOPAT / Total Invested Capital
            (self.income_statement.loc["operatingIncome"].astype(float) * (1 - (self.income_statement.loc["incomeTaxExpense"].astype(float) / self.income_statement.loc["incomeBeforeTax"].astype(float)))) / # NOPAT = Operating Income * (1 - Tax Rate)
            (self.balance_sheet.loc["totalDebt"].astype(float) + self.balance_sheet.loc["totalStockholdersEquity"].astype(float)) # Total Invested Capital = Total Debt + Shareholders equity
            ) * 100
        
        self.financial_metrics["payout"] = (abs(self.cash_flow.loc["dividendsPaid"].astype(float)) / netincome_row) * 100
        self.financial_metrics["calendarYear"] = self.income_statement.loc["calendarYear"]
        
    '''-----------------------------------'''
    def set_growth(self, period: str = "Annual"):
        """
        :param period: The timeframe of data to look at. 
        :returns: None
        
        Description: Add various financial ratios to the companies data. 
        """
        
        if self.income_statement.empty:
            self.set_income_statement(period=period)
        
        if self.balance_sheet.empty:
            self.set_balance_sheet(period=period)
        
        if self.cash_flow.empty:
            self.set_cash_flow(period=period) 
        
        # Income statement 
        self.growth["revenue"] = (self.income_statement.loc["revenue"].astype(float).pct_change()) * 100 # Revenue
        self.growth["netIncome"] = (self.income_statement.loc["netIncome"].astype(float).pct_change()) * 100 # Net Income (earnings)
        self.growth["eps"] = (self.income_statement.loc["eps"].astype(float).pct_change()) * 100 # Earnings per share
        self.growth["basicShares"] = (self.income_statement.loc["weightedAverageShsOut"].astype(float).pct_change()) * 100 # Basic Shares
        self.growth["dilutedShares"] = (self.income_statement.loc["weightedAverageShsOutDil"].astype(float).pct_change()) * 100 # Diluted Shares
        
        # Balance sheet
        self.growth["cash"] = (self.balance_sheet.loc["cashAndCashEquivalents"].astype(float).pct_change()) * 100 # Total Cash
        self.growth["debt"] = (self.balance_sheet.loc["totalDebt"].astype(float).pct_change()) * 100 # Total Debt
        self.growth["netDebt"] = (self.balance_sheet.loc["netDebt"].astype(float).pct_change()) * 100 # Net Debt (Debt - Cash)
        self.growth["shareholdersEquity"] = (self.balance_sheet.loc["totalStockholdersEquity"].astype(float).pct_change()) * 100 # Shareholders' Equity
        self.growth["equity"] = (self.balance_sheet.loc["totalEquity"].astype(float).pct_change()) * 100  # Total Equity 
        
        # Cash flow
        self.growth["sbc"] = (self.cash_flow.loc["stockBasedCompensation"].astype(float).pct_change()) * 100 # Stock based compensation
        self.growth["cffo"] = (self.cash_flow.loc["netCashProvidedByOperatingActivities"].astype(float).pct_change()) * 100 # Cash flow from operations
        self.growth["capex"] = (self.cash_flow.loc["capitalExpenditure"].astype(float).pct_change()) * 100 # Capital expenditures
        self.growth["fcf"] = (self.cash_flow.loc["freeCashFlow"].astype(float).pct_change()) * 100 # Free cash flow
        self.growth["sbi"] = (self.cash_flow.loc["commonStockIssued"].astype(float).pct_change()) * 100 # Stock based issuance
        self.growth["sbb"] = (self.cash_flow.loc["commonStockRepurchased"].astype(float).pct_change()) * 100 # Share buy backs
        self.growth["dividends"] = (self.cash_flow.loc["dividendsPaid"].astype(float).pct_change()) * 100
        self.growth["calendarYear"] = self.income_statement.loc["calendarYear"]
        
    '''-----------------------------------'''    
    def set_per_share(self, period: str = "Annual") -> None:
        """
        :param period: The timeframe to get all the statements for. 
        
        :returns: None
        """
        
        if self.income_statement.empty:
            self.set_income_statement(period=period)
            
        if self.balance_sheet.empty:
            self.set_balance_sheet(period=period)
            
        if self.cash_flow.empty:
            self.set_cash_flow(period=period)
        
        # Income statement 
        self.per_share_metrics["revenue"] = self.income_statement.loc["revenue"].astype(float) / self.income_statement.loc["weightedAverageShsOut"].astype(float)
        self.per_share_metrics["eps"] = self.income_statement.loc["eps"].astype(float)
        
        # Balance Sheet
        self.per_share_metrics["cash"] = self.balance_sheet.loc["cashAndCashEquivalents"].astype(float) / self.income_statement.loc["weightedAverageShsOut"].astype(float)
        self.per_share_metrics["debt"] = self.balance_sheet.loc["totalDebt"].astype(float) / self.income_statement.loc["weightedAverageShsOut"].astype(float)
        
        # Cash flow
        self.per_share_metrics["fcf"] = self.cash_flow.loc["freeCashFlow"].astype(float) / self.income_statement.loc["weightedAverageShsOut"].astype(float)
        self.per_share_metrics["calendarYear"] = self.income_statement.loc["calendarYear"]
        
    '''-----------------------------------'''
    def set_margins(self, period: str) -> None:
        """
        :param period: The timeframe to get all the statements for. 
        
        :returns: None
        
        Description: Set the margins of the business such as gross margin, operating margin, and profit margin. 
        """
        if self.income_statement.empty:
            self.set_income_statement(period=period)
        
        # Income Statement. 
        self.margins["grossMargin"] = self.income_statement.loc["grossProfitRatio"].astype(float) * 100
        self.margins["operatingMargin"] = self.income_statement.loc["operatingIncomeRatio"].astype(float) * 100
        self.margins["profitMargin"] = self.income_statement.loc["netIncomeRatio"].astype(float) * 100
        self.margins["calendarYear"] = self.income_statement.loc["calendarYear"]
    
    '''-----------------------------------'''
    def set_expenses(self, period: str = "Annual"):
        """
        :param period: The timeframe to get all the statements for. 
        
        :returns: None
        
        Description: Set the margins of the business such as gross margin, operating margin, and profit margin. 
        """
        if self.income_statement.empty:
            self.set_income_statement(period=period)
        
        grossprofit_row = self.income_statement.loc["grossProfit"].astype(float)
        operatingprofit_row = self.income_statement.loc["operatingIncome"].astype(float)
        
        
        # --- Gross Profit breakdown ---
        self.expenses_metrics["rd/grossProfit"] = (self.income_statement.loc["researchAndDevelopmentExpenses"].astype(float) / grossprofit_row) * 100
        self.expenses_metrics["ga/grossProfit"] = (self.income_statement.loc["generalAndAdministrativeExpenses"].astype(float) / grossprofit_row) * 100
        self.expenses_metrics["sm/grossProfit"] = (self.income_statement.loc["sellingAndMarketingExpenses"].astype(float) / grossprofit_row) * 100
        self.expenses_metrics["sga/grossProfit"] = (self.income_statement.loc["sellingGeneralAndAdministrativeExpenses"].astype(float) / grossprofit_row) * 100
        self.expenses_metrics["other/grossProfit"] = (self.income_statement.loc["otherExpenses"].astype(float) / grossprofit_row) * 100
        
        self.expenses_metrics["interestExpenses/operatingProfit"] = (self.income_statement.loc["interestExpense"].astype(float) / operatingprofit_row) * 100
        self.expenses_metrics["interestIncome/operatingProfit"] = (self.income_statement.loc["interestIncome"].astype(float) / operatingprofit_row) * 100
        self.expenses_metrics["calendarYear"] = self.income_statement.loc["calendarYear"]
        
        
    '''-----------------------------------'''
    def set_all_statements(self, period: str = "Annual") -> None:
        """
        :param period: The timeframe to get all the statements for. Ex: Annual or Quarterly
        
        :returns: None
        
        Description: Set all of the class variables.
        """
        self.income_statement = self.storage.get_financial_statement(financial_statement="income_statement",period=period) 
        self.balance_sheet = self.storage.get_financial_statement(financial_statement="balance_sheet",period=period)
        self.cash_flow = self.storage.get_financial_statement(financial_statement="cash_flow",period=period)
        self.set_metrics(period=period)
        self.set_growth(period=period)
        self.set_per_share(period=period)
        self.set_expenses(period=period)
    '''-----------------------------------'''
    def get_all_statements(self, period: str = "Annual"):
        """
        :param period: The timeframe to get the "income statement" for. Ex: Annual or Quarterly
        
        :returns: DataFrame
        
        Description: Set all of the class variables.
        """
        
        # First check if all the vars are empty. This is so we can you the "set_all_statements()" function. 
        if self.income_statement.empty and self.balance_sheet.empty and self.cash_flow.empty:
            self.set_all_statements(period=period)
        else:
            # Individually check if each dataframe is empty. Set the empty dataframes. 
            if self.income_statement.empty:
                self.set_income_statement(period=period)
            if self.balance_sheet.empty:
                self.set_balance_sheet(period=period)
            if self.cash_flow.empty:
                self.set_cash_flow(period=period)
                
            
            return {
                "income_statement": self.income_statement,
                "balance_sheet": self.balance_sheet,
                "cash_flow": self.cash_flow
            }
        
    '''-----------------------------------'''
    def set_all_analysis(self, period: str = "Annual"):
        """
        :param period: The timeframe to get the "income statement" for. Ex: Annual or Quarterly
        
        :returns: None
        
        Description: Set all of the class fundamental variables.
        """
        
        self.set_metrics(period=period)
        self.set_growth(period=period)
        self.set_per_share(period=period)
        self.set_expenses(period=period)
    '''-----------------------------------'''
    '''-----------------------------------'''