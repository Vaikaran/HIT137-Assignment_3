from tkinter import * 

class Command: #base class
    def __init__(self, txt, isType):
        self.text = txt
        self.isType = isType

    def getTextBoxText(self):
        return self.text

    def getStatusLabelText(self):        
        return ""
    
    def isContinue(self):
        return False