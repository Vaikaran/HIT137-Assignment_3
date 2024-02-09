import tkinter as tk
from tkinter import ttk

class CourseTaskScheduler(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Study Course: Task Scheduler/Calendar")
        self.geometry("800x400")

        self.tasks_schedule_label = tk.Label(self,text="Tasks Scheduler (optimal in fullscreen)",font=("Arial Bold", 20))
        self.tasks_schedule_label.pack(pady=10)  # Encapsulates labelling in the class

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill=tk.BOTH,expand=True)

        self.day_tab =tk.Frame(self.notebook)
        self.week_tab = tk.Frame(self.notebook)
        self.month_tab= tk.Frame(self.notebook)
        self.year_tab =tk.Frame(self.notebook)

        self.notebook.add(self.day_tab, text='The Day')
        self.notebook.add(self.week_tab, text='The Week')
        self.notebook.add(self.month_tab, text='The Month')
        self.notebook.add(self.year_tab, text='The Year')

        self.create_day_tab()  # Encapsulates Method call to the function.
        self.create_week_tab()  #
        self.create_month_tab() #
        self.create_year_tab()  # 

    def create_day_tab(self):
        self.day_LHS_frame=tk.Frame(self.day_tab )
        self.day_LHS_frame.pack(side=tk.LEFT,padx=9, pady=9,fill=tk.BOTH, expand=True)

        self.day_RHS_frame=tk.Frame(self.day_tab)
        self.day_RHS_frame.pack( side=tk.LEFT,padx=9, pady=9,fill=tk.BOTH,expand=True)

        self.day_task_labelling=tk.Label(self.day_LHS_frame,text="Task Events (List)",font=("Arial Bold", 17))
        self.day_task_labelling.pack(pady=8)  

        self.day_task_listboxes= tk.Listbox(self.day_LHS_frame, height=30, width=140, selectmode=tk.SINGLE)
        self.day_task_listboxes.pack(pady=10)# Encapsulated functionality is within this class.

        self.day_time_nametag = tk.Label(self.day_RHS_frame, text="Time of Event (List)",font=("Arial Bold", 16))
        self.day_time_nametag.pack(pady=8)  # Encapsulation label terms within the class.

        self.day_time_listbox = tk.Listbox(self.day_RHS_frame,height=30,  width=40, selectmode=tk.SINGLE)
        self.day_time_listbox.pack(pady=10)  

        self.day_add_entry = tk.Entry(self.day_LHS_frame, width=30, bg='yellow')
        self.day_add_entry.pack(side=tk.LEFT, padx=5)  

        self.day_add_button= GreenButton(self.day_LHS_frame, text="<--[ Add Task", command=self.add_day_task)
        self.day_add_button.pack (side=tk.LEFT,padx=4)# Encapsulates function banner into class.

        self.day_removal_button= tk.Button(self.day_LHS_frame,text="Delete Task" ,command=self.delete_day_task,bg='red')
        self.day_removal_button.pack(side=tk.LEFT,padx=5)  

        self.day_add_entry_right = tk.Entry(self.day_RHS_frame, width=30, bg='yellow')
        self.day_add_entry_right.pack(side=tk.LEFT, padx=5)  # Encapsulation demonstrated fitting methods into these classing

        self.day_add_button_right = GreenButton(self.day_RHS_frame, text="<--[ Add Time Label", command=self.add_time_label)
        self.day_add_button_right.pack(side=tk.LEFT, padx=5)  

        self.day_delete_button_right = tk.Button(self.day_RHS_frame, text="Delete Time Label", command=self.delete_time_label, bg='red')
        self.day_delete_button_right.pack(side=tk.LEFT, padx=5)  # Encapsulate through method of packing in class systems

    def create_week_tab(self):
        self.days_of_the_week=[ 'Sunday','Monday','Tuesday','Wednesday','Thursday', 'Friday','Saturday']
        self.week_entries = []

        self.week_represent= tk.Canvas(self.week_tab)
        self.week_represent.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.week_xbar=ttk.Scrollbar(self.week_tab,orient=tk.HORIZONTAL,command=self.week_represent.xview)
        self.week_xbar.pack(side=tk.TOP, fill=tk.X)

        self.week_represent.configure(xscrollcommand=self.week_xbar.set)

        self.week_internal_frames = tk.Frame(self.week_represent)
        self.week_represent.create_window((0,0),window=self.week_internal_frames,anchor=tk.NW)
        self.week_internal_frames.bind("<Configure>",self.on_frame_configure)
        for i,day in enumerate(self.days_of_the_week):
            day_label= tk.Label(self.week_internal_frames,text=day,font=( "Arial Bold", 14))
            day_label.grid(row=0,column=i, padx=4,pady=4)

            display_frame = tk.Listbox(self.week_internal_frames, bd=2, relief=tk.SUNKEN, height=32, width=12)
            display_frame.grid(row=1, column=i, padx=5, pady=5, sticky="nsew")

            inputted_frame=tk.Frame(self.week_internal_frames)
            inputted_frame.grid(row=2,column=i,padx=5, pady=5,sticky="nsew")

            text_entry_port=tk.Entry(inputted_frame,width=15,bg='yellow')
            text_entry_port.pack(side=tk.LEFT, padx=6)
            self.week_entries.append(text_entry_port)  # Encapsulation: Accessing and storing entry references within the class.

            add_button = GreenButton(inputted_frame,text="Add Task",command=lambda entry=text_entry_port,listbox=display_frame:self.add_week_task(entry, listbox))
            add_button.pack(side=tk.LEFT, padx=4) 

            delete_button=tk.Button(inputted_frame,text="Delete Task",command=lambda listbox=display_frame:self.delete_week_task(listbox),bg='red')
            delete_button.pack(side=tk.LEFT,padx=6)

        self.week_internal_frames.grid_columnconfigure(1, weight=1)
        self.week_internal_frames.grid_rowconfigure(1, weight=1)
        scroll_bar_label=tk.Label(self.week_internal_frames, text="<--- Scroll Bar Below --->", font=("Arial Bold", 16))
        scroll_bar_label.grid(row=3, columnspan=len(self.days_of_the_week), pady=5 )

    def create_month_tab(self):
        weeks=['Week-1 (days 1-7): ','Week-2 (days 8-14): ','Week-3 (days 15-21):','Week-4 (days 22-28):  ' , 'Week-5 (days 29-31): ' ]
        for i, week_text in enumerate (weeks):
            label=tk.Label( self.month_tab, text=week_text,font=("Arial Bold",14) )
            label.grid(row=i,column=0,sticky=tk.W)

            listbox=tk.Listbox(self.month_tab,bd=2, height=6, width=170 )
            listbox.grid( row=i,column=1, sticky=tk.W )
        self.month_entry=tk.Entry(self.month_tab,width=50,bg='yellow')
        self.month_entry.grid(row=i+1,column=0,padx=7, pady=7,sticky="w")
        self.add_weekly_note_button=tk.Button(self.month_tab, text="<--[ Select Week Tab (above) to Add Weekly Note",command=self.add_weekly_note,bg='green')
        self.add_weekly_note_button.grid(row=i+1,column=1, padx=4,pady=4, sticky="w")
        self.delete_weekly_note_button = tk.Button(self.month_tab, text="Delete Selected Weekly Note",command=self.delete_selected_weekly_note,bg='red')
        self.delete_weekly_note_button.grid(row=i+2, column=1, sticky="w")

    def create_year_tab(self):
        months=['January', 'February', 'March','April','May', 'June','July', 'August', 'September','October', 'November','December']
        for i, month in enumerate (months):
            row = i // 4
            col = i % 4
            visible_frame=tk.Listbox(self.year_tab,bd=2,relief=tk.SUNKEN,height=12,width=54)
            visible_frame.grid( row=row,column=col, padx=6,pady=3,sticky="nsew")
            month_titles=tk.Label(self.year_tab,text=month, font= ("Arial Bold", 10))
            month_titles.grid(row=row,column=col,padx=4,pady=3,sticky="s")

        self.year_entry_point=tk.Entry(self.year_tab,width=50,bg='yellow')
        self.year_entry_point.grid(row=row+1,column=0, padx=6,pady=6,sticky="w")
        self.add_monthly_comment_button=tk.Button(self.year_tab,text="<--[ Select a Month(above) to Add Monthly Note",command=self.add_monthly_note,bg='green')
        self.add_monthly_comment_button.grid(row=row+1,column=1, padx=5,pady=5,sticky="w")
        self.erase_monthly_comment_button = tk.Button(self.year_tab, text="Delete Selected Monthly Note(above)", command=self.delete_selected_monthly_note,bg='red')
        self.erase_monthly_comment_button.grid(row=row+1,column=2,padx=4,pady=4,sticky="w")
    def add_day_task(self):  # Demonstrates polymorphism: add_day_task() takes tasks to 'day_tab'
        task = self.day_add_entry.get()
        if task:
            self.day_task_listboxes.insert(tk.END, task)
            self.day_add_entry.delete(0, tk.END)
            print(f"Task '{task}' added successfully!")  # Multiple Inheritance: double function when succesfully activating green button 
                                                         # Encapsulation: Alters method within green button class
    def add_time_label(self):  # Polymorphism: add_time_label() adds time labels to 'day_tab'
        time_label = self.day_add_entry_right.get()
        if time_label:
            self.day_time_listbox.insert(tk.END, time_label)
            self.day_add_entry_right.delete(0, tk.END)
            print(f"Time label '{time_label}' added successfully!")  # Multiple Inheritance: provides simulataneous secondary output print function to green button
                                                                     # Encapsulation:Changes functionals within class.
    def delete_day_task(self):  #polymorphism: same 'delete_day_task()' removes the tasks from 'day_tab'
        self.delete_last_item(self.day_task_listboxes)

    def delete_time_label(self):  # Demonstrates polymorphism: 'delete_time_label()' deletes time labels from 'day_tab'
        self.delete_last_item(self.day_time_listbox)

    def add_week_task(self, text_entry, listbox):  #polymorphism:'add_week_task()' adds tasks to 'week_tab'
        task = text_entry.get()
        if task:
            listbox.insert(tk.END, task)
            text_entry.delete(0, tk.END)
            print(f"Task '{task}' added successfully!")  # Multiple Inheritance:Same print output function to green button after primary text transfer function
                                                         # Encapsulation: Same again.

    def delete_week_task(self, listbox):  # polymorphism: 'delete_week_task()' deletes tasks from 'week_tab'
        self.delete_last_item(listbox)

    def delete_last_item(self, listbox):
        listbox.delete(tk.END)

    def add_monthly_note(self):  #Polymorphism:'add_monthly_note()' can add notes to 'year_tab'
        selected_listbox = self.year_tab.focus_get()  # Get the currently focused widget
        if isinstance(selected_listbox, tk.Listbox):  # Check if the focused widget is a Listbox
            note = self.year_entry_point.get()
            if note:
                selected_listbox.insert(tk.END, note)
                self.year_entry_point.delete(0, tk.END)

    def delete_selected_monthly_note(self):  #polymorphism:'delete_selected_monthly_note()'deletes notes from 'year_tab'
        selected_listbox = self.year_tab.focus_get()  # Get the currently focused widget
        if isinstance(selected_listbox, tk.Listbox):  # Check if the focused widget is a Listbox
            selected_index = selected_listbox.curselection()
            if selected_index:  # Check if any item is selected
                selected_listbox.delete(selected_index)

    def delete_selected_weekly_note(self):  #polymorphism: "delete_selected_weekly_note()"take out note off- month_tab
        selected_listbox = self.month_tab.focus_get()  # Get the currently focused widget
        if isinstance(selected_listbox, tk.Listbox):  # Check if the focused widget is a Listbox
            selected_index = selected_listbox.curselection()
            if selected_index:  # Check if any item is selected
                selected_listbox.delete(selected_index)

    def on_frame_configure(self, event):
        self.week_represent.configure(scrollregion=self.week_represent.bbox("all"))

    def add_weekly_note(self):  #polymorphism: 'add_weekly_note()' notes put to the 'month_tab'
        selected_listbox = self.month_tab.focus_get()  # Get the currently focused widget
        if isinstance(selected_listbox, tk.Listbox):  # Check if the focused widget is a Listbox
            note = self.month_entry.get()
            if note:
                selected_listbox.insert(tk.END, note)
                self.month_entry.delete(0, tk.END)

class GreenButton(tk.Button):  # Multiple Inheritance: The green button inherits from the 'tk.Button'
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.configure(bg='green')

        # Add the command handler
        if 'command' in kwargs:
            self.command = kwargs['command']

            def new_command():   # Method Override concept present here to override the primary command to include printing functionality
                self.command()
                print(f"Green button activated successfully!")  # Multiple Inheritance:To place the secondary inherited function of output print (pressing of green button)
                                                                # Encapsulation of the secondary function into the "GreenButton" class.
            self.configure(command=new_command)

if __name__ == "__main__":
    app = CourseTaskScheduler()
    app.mainloop()
