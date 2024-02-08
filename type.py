from command import Command

class Type(Command) : #inheritance
    def __init__(self, txt, isType):
        Command.__init__(self, txt, isType) #calling parent constructor

    def setTextBoxText(self, txt): 
         self.text = txt

    def getTextBoxText(self): #method overriding
        if self.isType and self.text == "please type":
            return ""
        
        if self.text == "please exit":
            self.isType = False            
            return "-exit";

        return self.text
        

    def getStatusLabelText(self):    #method overriding
            if self.isType:     
                return "Tell me what you want to type OR Say please exit to go back"
            else:
                 return "What do you want to do? I'm listening..."
            
    def isContinue(self): #method overriding
         return True
    
    