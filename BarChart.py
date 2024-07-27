import io
import json
import kaleido
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs._figure as go

from AIModel import *
from matplotlib import pyplot as plt
from PIL import Image
from prompts import *

class BarChart:
    def __init__(self, model: AIModel):
        # Constructor
        
        self.model = model

    def fig_to_img(self, fig: go.Figure) -> Image.Image:
        # Converts a Plotly figure to a PIL Image
        
        img_bytes = fig.to_image(format="png")
        img = Image.open(io.BytesIO(img_bytes))
        return img

    def crop_data(self, data: str, symbol1: str, symbol2: str = "symbol") -> str:
        # Crops model's response from the first occurrence of symbol1 to the last occurrence of symbol2
        
        if symbol2 == "symbol":
            symbol2 = symbol1
        
        first_symbol = data.find(symbol1)
        last_symbol = data.rfind(symbol2)
        
        if first_symbol == -1 and last_symbol == -1:
            return data
        
        if first_symbol == (len(data) - 2):
            return data[:last_symbol]
        
        if last_symbol == 0:
            return data[first_symbol + 1:]
        
        return data[first_symbol + 1:last_symbol]

    def create_bar_chart(self, img: np.ndarray, data: dict, orientation: str, flag: str, odg_perc: str) -> go.Figure:
        # Creates a bar chart based on the provided data and settings
        
        values = data['values']
        df = pd.DataFrame(values)

        if odg_perc == "Y":
            df['value_str'] = df['value'].round(2).astype(str) + '%'
        
        if orientation == "Horizontal":
            fig = px.bar(df, x='value', y='parameter', orientation='h')
            fig.update_layout(yaxis=dict(autorange='reversed'))
            title = self.model.get_response(prompt_xtitle, img)
            fig.update_layout(xaxis_title=title, yaxis_title='')
        else:
            fig = px.bar(df, x='parameter', y='value')
            title = self.model.get_response(prompt_ytitle, img)
            fig.update_layout(xaxis_title='', yaxis_title=title)
        
        if flag == "YES":
            if odg_perc == "Y":
                fig.update_traces(text=df['value_str'])
            else:
                fig.update_traces(text=df['value'])
        
        fig.update_traces(marker_color='blue')
        return fig

    def give_chart(self, img: np.ndarray) -> Image.Image:
        # Processes an image to extract chart data and generate a bar chart
        
        answer = self.model.get_response(bar_chart_prompt, img)
        answer = answer.replace('\\', ' or ')
        print(answer)
        
        odg_orient = self.model.get_response(prompt_orient, img)
        odg_lab = self.model.get_response(prompt_label, img)
        odg_perc = self.model.get_response(prompt_perc, img)

        podaci = self.crop_data(answer, '!')
        odg_perc = self.crop_data(odg_perc, '&')

        orientation = self.crop_data(odg_orient, '-')
        
        flag = self.crop_data(odg_lab, '&')
        data_dict = json.loads(podaci)
        
        fig = self.create_bar_chart(img, data_dict, orientation, flag, odg_perc)
        return self.fig_to_img(fig)