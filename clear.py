from command import Command

class Clear(Command): #inheritance
    def __init__(self, txt, isType):
        Command.__init__(self, txt, isType) #calling parent constructor

    def getTextBoxText(self):   #method overriding
        return self.text 
    
    def getStatusLabelText(self):   #method overriding
            return "What do you want to do? I'm listening..."
    
    def isContinue(self): #method overriding
         return False