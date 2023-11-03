
# Pandas imports 
import pandas as pd

# Graph imports
import matplotlib.pyplot as plt 

# Date & Time imports
import datetime as dt



class AssetGraphs:
    def __init__(self):
        pass
    
    '''-----------------------------------'''
    def plot_data(self, data: list, metric: str) -> None:
        
        print(f"Data: {data}")
        
        
        # Create a figure and axis for the plot
        fig, ax = plt.subplots()

        # Iterate over the list of dictionaries and plot each DataFrame
        for entry in data:
            for key, df in entry.items():
                ax.plot(df.index, df[metric.lower()], marker="o", label=f'{key} ({df["calendarYear"].min()}-{df["calendarYear"].max()})')

        # Customize the plot
        ax.set_xlabel('Time')
        ax.set_ylabel(f'{metric} Ratio')
        ax.set_title(f'{metric} Ratio Over Time')
        ax.legend()

        # Show the plot
        plt.show()
    '''-----------------------------------'''
    def plot_bar(self, data: list, metric: str):
        
        parsed_dict = {}
        for i in data:
            for key, val in i.items():
                v = val[metric.lower()].to_list()
                parsed_dict[key] = v
        
        df = pd.DataFrame(parsed_dict)
        df = df.T
        
        # Get the current year minus 1 (since most of the time companies report at the end of the year, so if we are in 2023, we are looking at 2022 data.)
        year = dt.datetime.now().year - 1
        

        ax = df.plot(kind='bar', figsize=(10,6))
        
        # Customize the chart, labels, and title
        ax.set_xlabel('Year')
        ax.set_ylabel(f'{metric}')
        ax.set_title(f'{metric} for Different Stocks Over Time')

        # Show the plot
        plt.show()
        
        
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''
    '''-----------------------------------'''