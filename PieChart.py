import io
import json
import kaleido
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs._figure as go

from AIModel import *
from PIL import Image
from prompts import *

class PieChart:
    def __init__(self, model: AIModel):
        # Initializes the PieChart class with an AI model
        
        self.model = model

    def fig_to_img(self, fig: go.Figure) -> Image.Image:
        # Converts a Plotly figure to a PIL Image
        
        fig_bytes = fig.to_image(format="png")  
        buf = io.BytesIO(fig_bytes)  
        img = Image.open(buf) 
        return img

    def crop_data(self, data: str) -> str:
        # Extracts a substring from the data between two markers ('&')
        
        first_excl = data.find('&')
        last_excl = data.rfind('&')

        if first_excl == -1 and last_excl == -1:
            return data

        if first_excl == (len(data) - 2):
            return data[:last_excl]

        if last_excl == 0:
            return data[first_excl + 1:]

        return data[first_excl + 1:last_excl]

    def create_pie_chart(self, data: dict) -> go.Figure:
        # Creates a pie chart from the given data

        sorted_data = sorted(data.values(), key=lambda x: x['Value'], reverse=True)
        labels = [info['Label'] for info in sorted_data]
        sizes = [info['Value'] for info in sorted_data]
        colors = {info['Label']: info['Color'] for info in sorted_data}

        df = pd.DataFrame({
            "Label": labels,
            "Value": sizes,
            "Color": [colors[label] for label in labels]
        })

        fig = px.pie(df, values='Value', names='Label', color='Label',
                     color_discrete_map=colors)

        fig.update_traces(
            textposition='inside', 
            textinfo='percent+label',  
            textfont_size=12,
            pull=[0.1 if val < 10 else 0 for val in sizes], 
        )

        fig.update_traces(
            textposition='outside',
            showlegend=False,
            pull=0.03,
            textinfo='percent+label',
        )

        fig.update_layout(
            uniformtext_minsize=12, 
            uniformtext_mode="hide", 
            margin=dict(t=0, b=0, l=0, r=0), 
            autosize=True,  
            annotations=[dict(
                x=0.5,
                y=0.5,
                text="",
                showarrow=False,
                font_size=20,
            )]
        )

        return fig

    def give_chart(self, img: np.array) -> Image.Image:
        # Processes an image, extracts pie chart data, and generates a pie chart
        
        answer = self.model.get_response(pie_chart_prompt, img)  # Get the response from the model
        answer = self.crop_data(answer)  # Extract relevant data from the response

        data = json.loads(answer)  # Parse the JSON data
        fig = self.create_pie_chart(data)  # Create a pie chart
        img_format = self.fig_to_img(fig)  # Convert the figure to an image
        
        return img_format
