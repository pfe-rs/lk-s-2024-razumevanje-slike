import glob
import seaborn as sns
from prompts import *

class Validator:
    def __init__(self, bad=None, confusion_matrix=None):
        if bad is None:
            bad = 0
        self.bad = bad
        if confusion_matrix is None:
            confusion_matrix = [[0,0,0,0,0],
                                [0,0,0,0,0],
                                [0,0,0,0,0],
                                [0,0,0,0,0],
                                [0,0,0,0,0]] 
        self.confusion_matrix = confusion_matrix
    
    def response_number(self, response):
        if "pie chart" in response.lower():
            return 0
        elif "bar chart" in response.lower():
            return 1
        elif "line graph" in response.lower():
            return 2
        elif "list" in response.lower():
            return 3
        elif "trash" in response.lower():
            return 4
        else:
            self.bad += 1
            return 4
        
    def validation_helper(self, model, message, image, correct_response):
        i = self.response_number(correct_response)
        j = self.response_number(model.get_response(message, image))
        self.confusion_matrix[i][j] += 1

    def validation(self, model):
        ctr = 1;

        print("pie")
        for filename in glob.glob('/notebooks/dataset/pie/*.jpg'):
            if ctr > 2:
                break
            im = Image.open(filename)
            self.validation_helper(model, orchestrator_prompt, im, "pie chart")
            
            print(ctr)
            ctr += 1

        print("bar")
        for filename in glob.glob('/notebooks/dataset/bar/*.jpg'):
            if ctr > 4:
                break
            im = Image.open(filename)

            self.validation_helper(model, orchestrator_prompt, im, "bar chart")

            print(ctr)
            ctr += 1

        print("line")
        for filename in glob.glob('/notebooks/dataset/line/*.jpg'):
            if ctr > 6:
                break
            im = Image.open(filename)

            self.validation_helper(model, orchestrator_prompt, im, "line graph")

            print(ctr)
            ctr += 1

        print("table")
        for filename in glob.glob('/notebooks/dataset/table/*.jpg'):
            if ctr > 8:
                break
            im = Image.open(filename)

            self.validation_helper(model, orchestrator_prompt, im, "list")

            ctr += 1
            print(ctr)

        print("trash")
        for filename in glob.glob('/notebooks/dataset/trash/*.jpg'):
            if ctr > 10:
                break
            im = Image.open(filename)

            self.validation_helper(model, orchestrator_prompt, im, "trash")

            print(ctr)
            ctr += 1

        return ctr