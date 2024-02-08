from clear import Clear
from command import Command
from type import Type


class HandleCommand:
    def __init__(self, txt):
        self.textCommand = txt
        self.typeCommand = None        

    def getCommandType(self) -> Command:
        if self.textCommand == "please type":
            if self.typeCommand is None:
                self.typeCommand = Type(self.textCommand, True)
                return self.typeCommand;
            else:
                self.typeCommand.setTextBoxText(self.textCommand)
                return self.typeCommand
        elif(self.textCommand == "please clear"):
            self.typeCommand = Clear("", False)
            return self.typeCommand
        return None
