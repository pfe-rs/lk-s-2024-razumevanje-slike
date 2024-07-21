import io
import json
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from AIModel import *
from prompts import *

class PieChart:
    def __init__(self, model: AIModel):
        # Constructor
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
    

    def create_pie_chart(self, data: dict) -> plt.Figure:
        # Creates a pie chart from the provided data
        sorted_data = sorted(data.values(), key=lambda x: x['Value'], reverse=False)

        labels = [info['Label'] for info in sorted_data]
        sizes = [info['Value'] for info in sorted_data]
        colors = []
        for info in sorted_data:
            color = info['Color']
            try:
                mcolors.to_rgb(color)
                colors.append(color)
            except ValueError:
                colors.append('gray')

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal')
        return fig

    def give_chart(self, img: np.array) -> Image.Image:
        # Processes an image, extracts pie chart data, and generates a pie chart
        answer = self.model.get_response(pie_chart_prompt, img)
        answer = self.crop_data(answer)
        
        data = json.loads(answer)
        fig = self.create_pie_chart(data)
        img_format = self.fig_to_img(fig)
        
        return img_format