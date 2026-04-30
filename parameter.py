# Parameter class
import tkinter as tk
from tkinter import ttk

# The parameter
dSPIN_Registers = {
    "dSPIN_ABS_POS": 0x01,
    "dSPIN_EL_POS": 0x02,
    "dSPIN_MARK": 0x03,
    "dSPIN_SPEED": 0x04,
    "dSPIN_ACC": 0x05,
    "dSPIN_DEC": 0x06,
    "dSPIN_MAX_SPEED": 0x07,
    "dSPIN_MIN_SPEED": 0x08,
    "dSPIN_TVAL_HOLD": 0x09,
    "dSPIN_TVAL_RUN": 0x0A,
    "dSPIN_TVAL_ACC": 0x0B,
    "dSPIN_TVAL_DEC": 0x0C,
    "dSPIN_RESERVED_REG1": 0x0D,
    "dSPIN_T_FAST": 0x0E,
    "dSPIN_TON_MIN": 0x0F,
    "dSPIN_TOFF_MIN": 0x10,
    "dSPIN_RESERVED_REG2": 0x11,
    "dSPIN_ADC_OUT": 0x12,
    "dSPIN_OCD_TH": 0x13,
    "dSPIN_STALL_TH": 0x14,
    "dSPIN_FS_SPD": 0x15,
    "dSPIN_STEP_MODE": 0x16,
    "dSPIN_ALARM_EN": 0x17,
    "dSPIN_GATECFG1": 0x18,
    "dSPIN_GATECFG2": 0x19,
    "dSPIN_CONFIG": 0x1A,
    "dSPIN_STATUS": 0x1B
}



MOTOR_ID_1 = 0
MOTOR_ID_2 = 1
MOTOR_ID_3 = 2

class Parameter:
    def __init__(self,name,code,root_frame):
        self.name = name
        self.code = code
        self.values = [0,0,0]

        self.ui_label= tk.Label(
            root_frame,
            text=self.name, 
            font=("Helvetica", 10, "bold"),
            width=30, anchor="w", justify="left"
        )
        self.motor_entries= [tk.Entry(root_frame, width=20),
                             tk.Entry(root_frame, width=20),
                             tk.Entry(root_frame, width=20)]
        self.update_btns = [tk.Button(root_frame, text="Update", width=20,command=lambda: self.update_fn(MOTOR_ID_1)),
                            tk.Button(root_frame, text="Update", width=20,command=lambda: self.update_fn(MOTOR_ID_2)),
                            tk.Button(root_frame, text="Update", width=20,command=lambda: self.update_fn(MOTOR_ID_3))]

    def update_fn(self,MotorID):
        print(f'Upating {self.name} for Motor {MotorID}')


class Parameters:

    def __init__(self,root_frame):
        self.root_frame = root_frame
        self.all_parameters=[]
        self.make_parameters()

    def make_parameters(self):
        for name, value in dSPIN_Registers.items():
            self.all_parameters.append(Parameter(name,value,self.root_frame))
            #print(f"{name=}  {value=}")
        print("LEN ====", len(self.all_parameters))
    
    def render_parameters(self,start_row):
        row=start_row
        for p in self.all_parameters:
            p.ui_label.grid(row=row,column=0,sticky="ew",padx=2,pady=2, rowspan=2)
            column =1
            for e in p.motor_entries:
                e.grid(row=row,column=column,sticky="ew",padx=2,pady=2)
                column = column + 1
            row = row + 1
            column = 1
            for b in p.update_btns:
                b.grid(row=row,column=column,sticky="ew",padx=2,pady=2)
                column = column + 1
            
            row = row + 1
            separator = ttk.Separator(self.root_frame ,orient='horizontal')
            separator.grid(row=row,column=0,sticky="ew",padx=2,pady=6,columnspan=4)
            row = row +1
