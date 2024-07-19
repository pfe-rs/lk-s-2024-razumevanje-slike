import json
import io
import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from prompts import *

class PieChart:
    def __init__(self, model):
        # Constructor
        self.model = model

    def fig_to_img(self, fig: plt.Figure) -> Image.Image:
        # Converts a Matplotlib figure to a PIL Image.
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        fig_image = Image.open(buf)
        return fig_image
    
    def crop_data(self, data: str) -> str:
        # Crops model's response from first exclamation mark to last

        first_exclamation_index = data.find('!')
        last_exclamation_index = data.rfind('!')
            
        if first_exclamation_index != -1 and first_exclamation_index != last_exclamation_index:
            return data[first_exclamation_index + 1:last_exclamation_index]
        elif first_exclamation_index != -1:
            return data[first_exclamation_index + 1:]
        return data
    

    def create_pie_chart(self, data: dict) -> plt.Figure:
        # Creates a pie chart from the provided data.
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

    def give_chart(self, imggg: np.array) -> Image.Image:
        # Processes an image, extracts pie chart data, and generates a pie chart.
        answer = self.model.get_response(pie_chart_prompt, imggg)
        answer = self.crop_data(answer)
        
        data = json.loads(answer)
        fig = self.create_pie_chart(data)
        img_format = self.fig_to_img(fig)
        
        return img_format

    def get_response(self, message: str, image: np.array) -> str:
        # Sends an image and a message to the model and returns the response. class.
        return self.model.get_response(message, image)