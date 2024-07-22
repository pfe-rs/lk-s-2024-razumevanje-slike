import io
import json
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np

from AIModel import *
from PIL import Image
from prompts import *

class LineChart:
    def __init__(self, model: AIModel):
        self.model = model

    def fig_to_img(self, fig: plt.Figure) -> Image.Image:
        # Converts a Matplotlib figure to a PIL Image
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        fig_image = Image.open(buf)
        
        return fig_image
    
    def crop_data(self, data: str) -> str:
        # Crops model's response from first exclamation mark to last
        first_excl = data.find('!')
        last_excl = data.rfind('!')
        
        if first_excl == -1 and last_excl == -1:
            return data
        
        if first_excl == (len(data) - 2):
            return data[:last_excl]
        
        if last_excl == 0:
            return data[first_excl + 1:]
        
        return data[first_excl + 1:last_excl]

    def create_line_chart(self, data: dict) -> plt.Figure:
        # Creates a line chart from the provided data
        x, y = [], []
        y_label = data['Y_Axis']['Label']
        del data['Y_Axis']
        
        data = data.values()
        
        for info in data:
            x_value = info['X_Value']
            y_value = info['Y_Value']

            if y_value[-1] == "%":
                y_value = y_value[:-1]
                y_value = float(y_value) * 0.01
            else:
                y_value = float(y_value)

            x.append(x_value)
            y.append(round(y_value, 2))

        fig, ax = plt.subplots(figsize=(8, 6))

        ax.grid(axis='y')
        ax.plot(x, y, marker='o', linestyle='-')
        ax.tick_params(axis='x', rotation=45)
        ax.set_ylabel(y_label)
        
        for i, (xi, yi) in enumerate(zip(x, y)):
            plt.annotate(f'({xi}, {yi})', (xi, yi), textcoords="offset points", xytext=(0, 10), ha='center')
        
        return fig

    def give_chart(self, img: Image.Image) -> Image.Image:
        # Processes an image, extracts line chart data, and generates a line chart
        answer = self.model.get_response(line_chart_prompt, img)
        answer = self.crop_data(answer)
        
        data = json.loads(answer)
        fig = self.create_line_chart(data)
        img_format = self.fig_to_img(fig)
        
        return img_format