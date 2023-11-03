
# Pandas
import pandas as pd



# Import the asset manager
import Storage.asset_manager

# Import graphs 
import Graphs.graphs



class AssetCompare:
    def __init__(self):
        self.ticker_list = []
        
        self.graph = Graphs.graphs.AssetGraphs()
        
        self.info_types = {
            "financialMetrics": ["FinancialMetrics","financialMetrics", "financialmetrics", "financial-metrics", "FM", "Fm", "fm"],
            "growth": ["Growth", "growth", "G", "g"],
            "perShare": ["PerShare", "perShare", "pershare", "ps"],
            "margins": ["Margins", "margins", "M", "m"],
            "expenses": ["Expenses", "expenses", "E", "e"]
        }
    '''-----------------------------------'''
    def create_asset_objects(self, tickers: list, period: str = "Annual") -> list:
        """
        :param tickers: List of tickers in string format. 
        
        :returns: List of "AssetManager" objects. 
        
        Description: This function will create "AssetManager" objects for each ticker in the list. 
        """
        
        obj_list = [Storage.asset_manager.AssetManager(i) for i in tickers]
        [i.set_all_statements(period=period)    for i in obj_list]
        
        return obj_list
        
    '''-----------------------------------'''
    def create_group(self, group_tickers: list, info_type: str = "financialMetrics", period: str = "Annual", group_metric: str = "p/s"):
        
        group_objects = self.create_asset_objects(tickers=group_tickers, period=period)
        group_df = pd.DataFrame()
        group_data = []
        drop = True 
        
        # Get the correct key. 
        key = self.get_key_from_values(value=info_type)
        
        # Logic below follows for all of the following keys. 
        if key == "financialMetrics":
            # Iterate through asset objects. 
            for i in group_objects:
                data = pd.DataFrame()
                # Get the columns of the specific metric we are searching for from the "financial_metrics" dataframe. Drop the index so that they are numerical rather than dates. 
                data = i.financial_metrics[[group_metric, "calendarYear"]]
                data = data.reset_index(drop=drop)
                # Concat new columns to the dataframe. 
                #group_df = pd.concat([group_df, data], axis=1)
                group_data.append({
                    f"{i.ticker}": data
                })
            #group_df.columns = group_tickers
        elif key == "growth":
            # Iterate through asset objects. 
            for i in group_objects:
                data = pd.DataFrame()
                # Get the columns of the specific metric we are searching for from the "financial_metrics" dataframe. Drop the index so that they are numerical rather than dates. 
                data = i.growth[group_metric].reset_index(drop=drop)
                # Concat new columns to the dataframe. 
                group_df = pd.concat([group_df, data], axis=1)
            group_df.columns = group_tickers
        elif key == "perShare":
            # Iterate through asset objects. 
            for i in group_objects:
                data = pd.DataFrame()
                # Get the columns of the specific metric we are searching for from the "financial_metrics" dataframe. Drop the index so that they are numerical rather than dates. 
                data = i.per_share_metrics[group_metric].reset_index(drop=drop)
                # Concat new columns to the dataframe. 
                group_df = pd.concat([group_df, data], axis=1)
            group_df.columns = group_tickers
        elif key == "margins":
            # Iterate through asset objects. 
            for i in group_objects:
                data = pd.DataFrame()
                # Get the columns of the specific metric we are searching for from the "financial_metrics" dataframe. Drop the index so that they are numerical rather than dates. 
                data = i.margins[group_metric].reset_index(drop=drop)
                # Concat new columns to the dataframe. 
                group_df = pd.concat([group_df, data], axis=1)
            group_df.columns = group_tickers
        elif key == "expenses":
            # Iterate through asset objects. 
            for i in group_objects:
                data = pd.DataFrame()
                # Get the columns of the specific metric we are searching for from the "financial_metrics" dataframe. Drop the index so that they are numerical rather than dates. 
                data = i.expenses_metrics[group_metric].reset_index(drop=drop)
                # Concat new columns to the dataframe. 
                group_df = pd.concat([group_df, data], axis=1)
            group_df.columns = group_tickers
            
        return group_data
        
        
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    def get_key_from_values(self, value: str):
        """
        :param values: The value to be searched in the dictionary. 
        
        :returns: The key of that contains the value in the parameter. 
        
        Description: Search the dictionary "self.info_type"'s values. If there is a key that contains a list
        """
        
        for key, vals in self.info_types.items():
            if value in vals:
                return key
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''