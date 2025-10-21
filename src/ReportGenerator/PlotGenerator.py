import os
import pathlib 
import matplotlib.pyplot as plt 
from typing import List, Optional

class PlotGenerator: 
    def __init__(self, save_fig_dir : pathlib.Path, show_plots : bool = False):
        self.save_fig_dir = save_fig_dir

        # TODO : Maybe make this an input for functions instead
        self.show_plots   = show_plots

        self.___validateInputs___()


    def ___validateInputs___(self): 
        if not os.path.exists(self.save_fig_dir):
            raise FileNotFoundError(f"Directory path DNE: {self.save_fig_dir}")
    
        if not os.path.isdir(self.save_fig_dir):
            raise NotADirectoryError(f"Input path is not a directory: {self.save_fig_dir}")
        
    
    def createPieChart(
            self, 
            title   : str, 
            width   : float, # inches 
            height  : float, # inches 
            labels  : List[str], 
            sizes   : List[float], 
            colors  : Optional[List[str]]   = None, 
            explode : Optional[List[float]] = None
        ) -> plt.figure:

        fig = plt.figure(figsize=(width, height)) 

        plt.pie(
            sizes,  
            labels      = labels,
            colors      = colors,
            explode     = explode if explode else [0] * len(sizes) ,
            autopct     = '%1.1f%%',  # for now
            shadow      = True,
            startangle  = 140 
        )

        plt.title = title
        plt.axis('equal')
        
        if self.show_plots:
            plt.show()

        return fig 


    def createBarChartFromDf(self, df, label_col, value_col, title) -> plt.figure:
        fig = plt.figure(figsize=(10, 6))
        plt.bar(df[label_col], df[value_col], color='skyblue')
        plt.xlabel(label_col)
        plt.ylabel(value_col)
        plt.title(title)
        plt.xticks(rotation=90)
        plt.tight_layout()

        if self.show_plots:
            plt.show()

        return fig