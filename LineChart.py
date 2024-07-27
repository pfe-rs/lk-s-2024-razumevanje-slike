import io
import json
import kaleido
import numpy as np
import plotly.express as px
import plotly.graph_objs._figure as go

from AIModel import *
from PIL import Image
from prompts import *

class LineChart:
    def __init__(self, model: AIModel):
        # Constructor
        
        self.model = model

    def fig_to_img(self, fig: go.Figure) -> Image.Image:
        # Converts a Plotly figure to a PIL Image
        
        fig_bytes = fig.to_image(format="png")
        buf = io.BytesIO(fig_bytes)
        img = Image.open(buf)
        return img
    
    def crop_data(self, data: str, symbol1: str, symbol2: str) -> str:
        # Crops model's response from the first occurrence of symbol1 to the last occurrence of symbol2
        
        first_symbol = data.find(symbol1)
        last_symbol = data.rfind(symbol2)
        
        if first_symbol == last_symbol and first_symbol == -1:
            return data
        if symbol1 == '{':
            return data[first_symbol:last_symbol + len(symbol2)]
        else:
            return data[first_symbol + len(symbol1):last_symbol]

    def create_line_chart(self, data: dict, perc: str) -> go.Figure:
        # Creates a line chart from the provided data
        
        x, y = [], []
        y_label = data['Y_Axis']['Label']
        del data['Y_Axis']
        
        data = data.values()
        
        for info in data:
            x_value = info['X_Value']
            y_value = info['Y_Value']
            
            if isinstance(y_value, str):
                if y_value[-1] == '%':
                    perc = "YES"
                    y_value = y_value[:-1]
                    y_value = round(float(y_value) * 0.01, 4)
                elif perc == "YES":
                    y_value = round(float(y_value) * 0.01, 4)
                else:
                    y_value = round(float(y_value), 2)
            elif perc == "YES":
                y_value = round(float(y_value) * 0.01, 4)
            else:
                y_value = round(float(y_value), 2)

            x.append(x_value)
            y.append(y_value)

        fig = px.line(x = x, y = y)
        
        fig.update_xaxes(tickangle=45)
        fig.update_layout(yaxis_tickformat=".2f")
        fig.update_layout(yaxis_title=dict(text=y_label), xaxis_title=None)
        if perc == "YES":
            fig.update_layout(yaxis_tickformat=".2%")
        
        return fig

    def give_chart(self, img: Image.Image) -> Image.Image:
        # Processes an PIL Image, extracts line chart data, and generates a line chart
        
        perc_response = self.model.get_response(line_chart_percentages_prompt, img)
        perc_response = self.crop_data(perc_response, '&', '&')
        
        data = self.model.get_response(line_chart_prompt, img)
        data = self.crop_data(data, '{', '}\n}')

        try:
            points = json.loads(data)
            fig = self.create_line_chart(points, perc_response)
            img_format = self.fig_to_img(fig)
            return img_format
        except:
            img_format = Image.open("/notebooks/image_2024-07-18_195702655.png")
            return img_format