# Parameter class
import tkinter as tk
from tkinter import ttk, messagebox

# The parameter
dSPIN_Registers_general = {
    "dSPIN_ACC" :0x05,
    "dSPIN_DEC" :0x06,
    "dSPIN_MAX_SPEED" :0x07,
    "dSPIN_MIN_SPEED" :0x08,
    "dSPIN_OCD_TH" :0x13,
    "dSPIN_FS_SPD" :0x15,
    "dSPIN_STEP_MODE" :0x16,
    "dSPIN_ALARM_EN" :0x17,
    "dSPIN_GATECFG1" :0x18,
    "dSPIN_GATECFG2" :0x19,
    "dSPIN_CONFIG" :0x1A,
    #"dSPIN_STATUS" :0x1B
}

	
dSPIN_Registers_ro = {
    "dSPIN_SPEED" :0x04,
    "dSPIN_STATUS" :0x1B,
    "dSPIN_ADC_OUT" :0x12,
}
dSPIN_Registers_pos = {
    "dSPIN_ABS_POS" :0x01,
    "dSPIN_EL_POS" :0x02,
    "dSPIN_MARK" :0x03,
}

dSPIN_Registers_Voltage = {
"dSPIN_KVAL_HOLD" :0x09,
"dSPIN_KVAL_RUN" :0x0A,
"dSPIN_KVAL_ACC" :0x0B,
"dSPIN_KVAL_DEC" :0x0C,
"dSPIN_INT_SPEED" :0x0D,
"dSPIN_ST_SLP" :0x0E,
"dSPIN_FN_SLP_ACC" :0x0F,
"dSPIN_FN_SLP_DEC" :0x10,
"dSPIN_K_THERM" :0x11,
"dSPIN_STALL_TH" :0x14,
}

dSPIN_Registers_Current = {
"dSPIN_TVAL_HOLD" :0x09,
"dSPIN_TVAL_RUN" :0x0A,
"dSPIN_TVAL_ACC" :0x0B,
"dSPIN_TVAL_DEC" :0x0C,
"dSPIN_T_FAST" :0x0E,
"dSPIN_TON_MIN" :0x0F,
"dSPIN_TON_MIN" :0x10,
}

#define dSPIN_TVAL_HOLD		dSPIN_KVAL_HOLD
#define dSPIN_TVAL_RUN		dSPIN_KVAL_RUN
#define dSPIN_TVAL_ACC		dSPIN_KVAL_ACC
#define dSPIN_TVAL_DEC		dSPIN_KVAL_DEC
#define dSPIN_T_FAST		dSPIN_ST_SLP
#define dSPIN_TON_MIN		dSPIN_FN_SLP_ACC
#define dSPIN_TON_MIN		dSPIN_FN_SLP_DEC
MOTOR_ID_1 = 0
MOTOR_ID_2 = 1
MOTOR_ID_3 = 2

class Parameter:
    def __init__(self,name,code,root_frame,ro,protocol_handler=None):
        self.name = name
        self.code = code
        self.ro = ro
        self.protocol_handler = protocol_handler
        self.values = [0,0,0]

        self.ui_label= tk.Label(
            root_frame,
            text=self.name[6:], # Remove the dSPIN_
            font=("Helvetica", 10, "bold"),
            width=12, anchor="w", justify="left"
        )
        self.motor_entries= [tk.Entry(root_frame, width=6,justify='center'),
                             tk.Entry(root_frame, width=6,justify='center'),
                             tk.Entry(root_frame, width=6,justify='center')]
        if not self.ro:
            self.update_btns = [tk.Button(root_frame, text="W", width=5,command=lambda: self.update_fn(MOTOR_ID_1)),
                                tk.Button(root_frame, text="W", width=5,command=lambda: self.update_fn(MOTOR_ID_2)),
                                tk.Button(root_frame, text="W", width=5,command=lambda: self.update_fn(MOTOR_ID_3))]
        else:
            self.update_btns = []
    
    def update_fn(self,MotorID):
        """ Write the parameters """
        print(f'Upating {self.name} for Motor {MotorID}')
        value = self.motor_entries[MotorID].get()
        mask = 1 << MotorID
        if value:
            try:
              value = int(value,0)
              print(f'Running  {self.name} for Motor {MotorID} with Value {value}')
              self.protocol_handler.put_param(mask,self.code,value)
            except ValueError:
                messagebox.showerror("Invalid Input", f"Please enter a valid integer value for Motor {MotorID}.")
        
    def read_all(self):
        """ Read the parameter from  ALL the motor """
        data_received = self.protocol_handler.get_param(0x07,self.code)
        if data_received is None:
            raise Exception("No data received from the Pump Unit")
        #p1 = [20,20,100]
        for m in range (0,3):
            self.motor_entries[m].delete(0,tk.END)
            self.motor_entries[m].insert(0,hex(data_received[m]))

class Parameters:

    def __init__(self,root_frame,protocol_handler,parameter_dict,ro=False):
        self.root_frame = root_frame
        self.protocol_handler = protocol_handler
        self.parameter_dict = parameter_dict
        self.ro = ro
        self.all_parameters=[]
        self.make_parameters()

    def make_parameters(self):
        for name, value in self.parameter_dict.items():
            self.all_parameters.append(Parameter(name,value,self.root_frame,self.ro,self.protocol_handler))
            #print(f"{name=}  {value=}")
        print("LEN ====", len(self.all_parameters))
    
    def render_parameters(self,start_row):
        row=start_row
        tk.Label(self.root_frame, text="M1",font=("Helvetica", 10, "bold")).grid(row=row,column=1)
        tk.Label(self.root_frame, text="M2",font=("Helvetica", 10, "bold")).grid(row=row,column=2)
        tk.Label(self.root_frame, text="M3",font=("Helvetica", 10, "bold")).grid(row=row,column=3)
        row = row + 1

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
            separator.grid(row=row,column=0,sticky="ew",padx=2,pady=3,columnspan=4)
            row = row +1
    
    def read_all(self):
        for p in self.all_parameters:
            p.read_all()

