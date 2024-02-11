import asyncio
from tkinter import *
from handle_command import HandleCommand 
import speech_command as sc
import tkinter.font as fnt

class Main:
    root = Tk()
    headerFrame = Frame(root)
    topFrame = Frame(root)
    bottomFrame = Frame(root)
    headerFrame.pack()
    topFrame.pack()
    bottomFrame.pack()
    window_width = 850
    window_height = 350
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    center_x = int((screen_width - window_width)/2)
    center_y = int((screen_height - window_height)/2)
    root.geometry(f"{window_width}x{window_height}+{center_x}+{center_y}")
    root.resizable(False, False)

    label1 = Label(headerFrame, text="Voice Commands", font=fnt.Font(size=15, weight="bold"))
    button1 = Button(topFrame, text="Please Type", background="green", fg="white", font = fnt.Font(size = 10, weight="bold"), width=12, height=2)
    button2 = Button(topFrame, text="Please Clear", background="orange", fg="white", font = fnt.Font(size = 10, weight="bold"), width=12, height=2)
    button3 = Button(topFrame, text="Please Close", background="red", fg="white", font = fnt.Font(size = 10, weight="bold"), width=12, height=2)
    textBox1 = Text(bottomFrame, width=100, height=10)
    labelStatus = Label(bottomFrame, text="Initiating...", font=fnt.Font(size=10))
    labelLog = Label(bottomFrame, text="", font=fnt.Font(size=10))
    label1.grid(row=0, pady=(5, 10))
    button1.grid(row=2, column=0)
    button2.grid(row=2, column=2, padx=(10, 10))
    button3.grid(row=2, column=4)
    textBox1.grid(row=3, pady=(10, 0))
    labelStatus.grid(row=4, column=0, padx=(10, 0))
    labelLog.grid(row=5, column=0, padx=(10, 0))
                
    def __init__(self):  
        self.root.after(2000, self.begin_listening)
        self.isCommanding = False
        self.com = None
        self.root.mainloop()
        
    def begin_listening(self):
        voiceCommandHandler = sc.SpeechCommand(); #create class object
        if not self.isCommanding:
            self.labelStatus.config(text="What do you want to do? I'm listening...")
        self.labelLog.config(text="Speak")
        self.root.update()
        recorded_speach = voiceCommandHandler.record_speech(5) #call a method from object
        vCommand = voiceCommandHandler.recognize_speech(recorded_speach) #call a method from object
        if not self.isCommanding and vCommand is None:            
            self.labelLog.config(text="Sorry, Voice command could not be fount!")
            self.root.update()
        elif not self.isCommanding and vCommand == "please close":
                self.root.destroy()
        else:
            if not self.isCommanding:
                vCom = HandleCommand(vCommand);
                self.com = vCom.getCommandType();
            else:
                if vCommand is not None:
                    self.com.setTextBoxText(vCommand)
                                    
            if self.com is not None:
                self.textBox1.focus()
                self.labelStatus.config(text=self.com.getStatusLabelText())
                tbox = self.com.getTextBoxText()
                if tbox == "-exit":
                    self.isCommanding = False
                    self.labelStatus.config(text="What do you want to do? I'm listening...")
                else:
                    if self.isCommanding:
                        self.labelLog.config(text="Your Command: " + tbox)
                    self.textBox1.delete("1.0", "end")
                    self.textBox1.insert(END, tbox)
                    self.isCommanding = self.com.isContinue()
            else:
                self.labelLog.config(text="Sorry, Voice command is not matching!")
        self.root.after(2000, self.begin_listening)

mn = Main()