import io
import json
import pandas as pd
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from AIModel import *
from io import BytesIO
from PIL import Image, ImageOps
from prompts import *

class BarChart:
    def __init__(self, model: AIModel):
        # Constructor
        self.model = model
    
    def crop_data(self, data: str, symbol: str) -> str:
        # Crops model's response from first exclamation mark to last
        first_symbol = data.find(symbol)
        last_symbol = data.rfind(symbol)
        
        if first_symbol == -1 and last_symbol == -1:
            return data
        
        if first_symbol == (len(data) - 2):
            return data[:last_symbol]
        
        if last_symbol == 0:
            return data[first_symbol + 1:]
        
        return data[first_symbol + 1:last_symbol]
    
    def add_labels(self, ax, x, y):
        for i in range(len(x)):
            ax.text(i, y[i], str(y[i]), ha='center', va='bottom', fontsize=7)
    
    def ax_to_pil(self, ax):
        buf = BytesIO()
        ax.figure.savefig(buf, format='png', bbox_inches='tight')
        buf.seek(0)
        # Open the image with PIL
        img = Image.open(buf)

        return img

    def create_bar_chart(self, data: dict, col, orientation: str, flag) -> plt.Figure:
        # Creates a pie chart from the provided data.
        print(col)
        df = pd.DataFrame.from_dict(data['values'])
        if orientation == "Horizontal":
            
            ax = df.plot.barh(x='parameter', y='value', rot=0, color=col)
            ax.invert_yaxis()
            ax.grid(axis='x')
            if(flag=="YES"):
                for index, value in enumerate(df['value']):
                    ax.text(value, index, str(value))
            #self.add_labels(ax, df['value'], df['parameter'])
        else:
            ax = df.plot.bar(x='parameter', y='value', rot=0, color=col)
            ax.grid(axis='y')
            if flag=="YES":
                self.add_labels(ax, df['parameter'], df['value'])
        return ax
        

    def give_chart(self, imggg: np.array) -> Image.Image:
        # Processes an image, extracts pie chart data, and generates a pie chart.
        answer = self.model.get_response(bar_chart_prompt, imggg)
        print(answer)
        
        odg_lab = self.model.get_response(prompt_label, imggg)
        odg_lab = self.crop_data(odg_lab, '&')
        print(odg_lab)
        
        podaci = self.crop_data(answer, '!')
        orientation = self.crop_data(answer, '-')
        print(orientation)
        
        data = json.loads(podaci)
        ax = self.create_bar_chart(data, "blue", orientation, odg_lab)
        img_format = self.ax_to_pil(ax)
        img_format = ImageOps.expand(img_format, border=(50,50,50,50), fill="white")
        
        return img_format