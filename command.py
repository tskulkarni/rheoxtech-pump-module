import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
MOTOR_ID_1 = 0
MOTOR_ID_2 = 1
MOTOR_ID_3 = 2


dSPIN_Commands = {

"dSPIN_RUN" :		    'R',
"dSPIN_RESET_DEVICE" :	'X',
"dSPIN_SOFT_STOP" :	    's',
"dSPIN_HARD_STOP" :     'S',
"dSPIN_SOFT_HIZ" :	    'z',
"dSPIN_HARD_HIZ":       'Z'
}
class Command:
    def __init__(self,name,code,root_frame,protocol_handler):
        self.name = name
        self.code = code
        self.protocol_handler = protocol_handler
        self.ui_label= tk.Label(
            root_frame,
            text=self.name[6:], # Remove the dSPIN_
            font=("Helvetica", 10, "bold"),
            width=12, anchor="w", justify="left"
        )
        if self.name == "dSPIN_RUN":
            self.speed_entries= [tk.Entry(root_frame, width=6,justify='center'),
                                 tk.Entry(root_frame, width=6,justify='center'),
                                 tk.Entry(root_frame, width=6,justify='center')]
        else:
            self.speed_entries = []
        self.update_btns = [tk.Button(root_frame, text="M1", width=5,command=lambda: self.cmd_fn(MOTOR_ID_1)),
                            tk.Button(root_frame, text="M2", width=5,command=lambda: self.cmd_fn(MOTOR_ID_2)),
                            tk.Button(root_frame, text="M3", width=5,command=lambda: self.cmd_fn(MOTOR_ID_3))]    
    def cmd_fn(self,MotorID):
        """ Write the parameters """
        speed = self.speed_entries[MotorID].get() if self.speed_entries else None
        mask = 1 << MotorID
        if speed:

            try:
              speed = int(speed,0)
              print(f'Running  {self.name} for Motor {MotorID} with speed {speed}')
              self.protocol_handler.execute_cmd(mask,self.
                                                code,1,speed)
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter a valid integer speed for Motor {MotorID}.")
        else:
            print(f'Running  {self.name} for Motor {MotorID} with no speed')
            self.protocol_handler.execute_cmd(mask,self.code)

class Commands:

    def __init__(self,root_frame,protocol_handler):
        self.root_frame = root_frame
        self.protocol_handler = protocol_handler
        self.all_commands=[]
        self.make_commands()

    def make_commands(self):
        for name, value in dSPIN_Commands.items():
            self.all_commands.append(Command(name,value,self.root_frame,self.protocol_handler))
            
    
    def render_commands(self,start_row):
        row=start_row
        for c in self.all_commands:
            c.ui_label.grid(row=row,column=0,sticky="ew",padx=2,pady=2, rowspan=2)
            column =1
            if len(c.speed_entries):
                tk.Label(self.root_frame, text="Speed (Steps/s)",font=("Helvetica", 10, "bold")).grid(row=row-1,column=column,sticky="ew",padx=2,pady=2,columnspan=3)
                row = row + 1
            for e in c.speed_entries:
                e.grid(row=row,column=column,sticky="ew",padx=2,pady=2)
                column = column + 1
            row = row  + 1
            column = 1
            for b in c.update_btns:
                b.grid(row=row,column=column,sticky="ew",padx=2,pady=2)
                column = column + 1
            
            row = row + 1
            separator = ttk.Separator(self.root_frame ,orient='horizontal')
            separator.grid(row=row,column=0,sticky="ew",padx=2,pady=3,columnspan=4)
            row = row +1
    