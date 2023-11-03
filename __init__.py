

# Import asset manager
from Storage.asset_manager import AssetManager

# Import GUI
from GUI.app import AssetCompareApp

# Import AssetCompare class
from AssetCompare.asset_compare import AssetCompare



if __name__ == "__main__":
    
    #app = AssetCompareApp()
    #app.mainloop()
    compare = AssetCompare()
    
    ticker = "AAPL"
    tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "NVDA"]
    
    group = compare.create_group(group_tickers=tickers)
    #compare.graph.plot_data(data=group, label="P/S")
    compare.graph.plot_bar(data=group, metric="p/s")
    