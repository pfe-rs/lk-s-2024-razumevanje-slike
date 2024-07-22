import glob
import seaborn as sns
from AIModel import *
from prompts import *

class Validator:
    def __init__(self, bad=0, confusion_matrix=[[0, 0, 0, 0] for _ in range(4)]) -> None:
        # Constructor
        self.bad = bad
        self.confusion_matrix = confusion_matrix
        
    def response_number(self, response: str) -> int:
        # Gets the corresponding row or column of a response in order to build confusion matrix
        response = response.lower()
        chart_map = {
            "pie chart": 0,
            "bar chart": 1,
            "line chart": 2,
            "trash": 3
        }

        for key, value in chart_map.items():
            if key in response:
                return value

        self.bad += 1
        return 3
        
    def validation_helper(self, model: AIModel, message: str, image: Image.Image, correct_response: str) -> None:
        # Builds confusion matrix based on correct response and the response the model gives
        i = self.response_number(correct_response)
        j = self.response_number(model.get_response(message, image))
        self.confusion_matrix[i][j] += 1

    def validation(self, model: AIModel) -> None:
        # Goes through the database and calls validation_helper for every image
        categories = ["pie", "bar", "line", "trash"]
        labels = ["pie chart", "bar chart", "line chart", "trash"]

        for i, category in enumerate(categories):
            print(category)
            
            counter = 1 # Limits how many images we go through
            for filename in glob.glob(f"/notebooks/dataset/{category}/*.jpg"):
                if category != "trash":
                    if counter > 100:
                        break
                    im = Image.open(filename)
                    self.validation_helper(model, orchestrator_prompt, im, labels[i])
                    print(counter)
                    counter += 1
                else:
                    if counter > 300:
                        break
                    im = Image.open(filename)
                    self.validation_helper(model, orchestrator_prompt, im, labels[i])
                    print(counter)
                    counter += 1