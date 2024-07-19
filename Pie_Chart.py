import numpy as np
from PIL import Image
import json
import io
import matplotlib.pyplot as plt
from prompts import *

class Pie_Chart:
    def __init__(self, model):
        self.model = model
    
    def fig_to_img(self, fig):
        buf = io.BytesIO()
        fig.savefig(buf, format='png')
        buf.seek(0)
        img33 = Image.open(buf)
        return img33

    def create_pie_chart(self, data):
        sorted_data = sorted(data.values(), key=lambda x: x['Value'], reverse=False)

        labels = [info['Label'] for info in sorted_data]
        sizes = [info['Value'] for info in sorted_data]
        colors = [info['Color'] for info in sorted_data]

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=90)
        ax.axis('equal') 
        return fig
    
    def give_chart(self, imggg):
        answer = self.model.get_response(pie_chart_prompt, imggg)
        
        
        first_exclamation_index = answer.find('!')
        if first_exclamation_index == -1:
            pass

        last_exclamation_index = answer.rfind('!')
        if first_exclamation_index == last_exclamation_index:
            answer = answer[first_exclamation_index+1:]

        answer = answer[first_exclamation_index+1:last_exclamation_index]
        #print(answer)
        
        data = json.loads(answer)
        fig = self.create_pie_chart(data)
        img44 = self.fig_to_img(fig)
        imgg=img44
        
        return imgg