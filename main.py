import tkinter as tk
from tkinter import messagebox
import serial

from parameter import Parameters,dSPIN_Registers_general,dSPIN_Registers_ro,dSPIN_Registers_pos,dSPIN_Registers_Voltage,dSPIN_Registers_Current
from command import Commands
from protocol import Protocol
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # 1. Configure the main application window
        self.title("Pump Unit Test")
        self.geometry("1400x1000")
        self.port_open = False
        self.com_handle = None
        self.protocol_handler = Protocol(None)
    
        # Initialize all the parameters and commands

        # 4. Initialize the Right Frame
        self.right_frame = tk.Frame(self, bg="#f1f8e9")
        self.right_frame.pack(fill="both")

        
        self.build_right_frame()

    def build_left_frame(self):
        """Add widgets to the left frame."""
        label = tk.Label(
            self.left_frame, 
            text="Left Panel Content", 
            bg="#e0f7fa", 
            font=("Helvetica", 14, "bold")
        )
        label.pack(pady=0)
        
        # Example button
        btn = tk.Button(self.left_frame, text="Action 1")
        btn.pack(pady=10)

    def build_right_frame(self):
        
        # Create the top frame
        self.top_frame = tk.Frame(self.right_frame)
        self.top_frame.pack()
        label = tk.Label(
            self.top_frame, 
            text="Paramters", 
            bg="#f1f8e9", 
            font=("Helvetica", 14, "bold")
        )
        #label.pack(pady=4)
        self.com_port_txt = tk.Entry(self.top_frame,width = 25)
        self.com_port_txt.grid(row=0,column=0,padx=2) 
        self.open_com_port_button = tk.Button(self.top_frame,text="Open Port", width=10,command=self.open_com_port)
        self.open_com_port_button.grid(row=0,column=1,padx=2) 
        
        self.update_all_button = tk.Button(self.top_frame, text="Read all Parameters", width=20,
                                           command=self.update_all_params)
        self.update_all_button.grid(row=1,column=0, columnspan=2, pady=4)
        
        # This frame
        self.parameter_frame = tk.Frame(self.right_frame)
        self.parameter_frame.pack()
        
        
        self.ro_setup_frame  = tk.Frame(self.parameter_frame,highlightbackground='black', highlightthickness=2)
        self.ro_setup_frame.grid(row=0,column=0,padx=1)
        l1 = tk.Label(
            self.ro_setup_frame,
            text="Read Only Parameters", 
            bg="#f1f8e9", 
            font=("Helvetica", 12, "bold")
        )
        l1.grid(row=0,column=0,columnspan=3)
        
        self.parameters_ro = Parameters(self.ro_setup_frame,self.protocol_handler,dSPIN_Registers_ro,ro=True)
        self.parameters_ro.render_parameters(2)

        self.general_setup_frame  = tk.Frame(self.parameter_frame,highlightbackground='black', highlightthickness=2)
        self.general_setup_frame.grid(row=0,column=1,padx=1,rowspan=4)
        l2 = tk.Label(
            self.general_setup_frame,
            text="General Parameters", 
            bg="#f1f8e9", 
            font=("Helvetica", 12, "bold")
        )
        l2.grid(row=0,column=0,columnspan=3)
        self.parameters_g = Parameters(self.general_setup_frame,self.protocol_handler,dSPIN_Registers_general,ro=False)
        self.parameters_g.render_parameters(2)


        self.position_setup_frame  = tk.Frame(self.parameter_frame,highlightbackground='black', highlightthickness=2)
        self.position_setup_frame.grid(row=1,column=0   ,padx=1)
        l3 = tk.Label(
            self.position_setup_frame,
            text="Position Parameters", 
            bg="#f1f8e9", 
            font=("Helvetica", 12, "bold")
        )
        l3.grid(row=1,column=0,columnspan=3)

        self.parameters_pos = Parameters(self.position_setup_frame,self.protocol_handler,dSPIN_Registers_pos,ro=False)
        self.parameters_pos.render_parameters(2)

        # Voltage Config
        self.voltage_setup_frame  = tk.Frame(self.parameter_frame,highlightbackground='black', highlightthickness=2)
        self.voltage_setup_frame.grid(row=0,column=2   ,padx=1,rowspan=5)
        l3 = tk.Label(
            self.voltage_setup_frame,
            text="Voltage Config Parameters", 
            bg="#f1f8e9", 
            font=("Helvetica", 12, "bold")
        )
        l3.grid(row=0,column=0,columnspan=3)
        self.parameters_v = Parameters(self.voltage_setup_frame,self.protocol_handler,dSPIN_Registers_Voltage,ro=False)
        self.parameters_v.render_parameters(2)

        # Current Config   
        self.current_setup_frame  = tk.Frame(self.parameter_frame,highlightbackground='black', highlightthickness=2)
        self.current_setup_frame.grid(row=0,column=3   ,padx=1,rowspan=5)
        l4 = tk.Label(
            self.current_setup_frame,
            text="Current Config Parameters", 
            bg="#f1f8e9", 
            font=("Helvetica", 12, "bold")
        )
        l4.grid(row=0,column=0,columnspan=3)
        self.parameters_i = Parameters(self.current_setup_frame,self.protocol_handler,dSPIN_Registers_Current,ro=False)
        self.parameters_i.render_parameters(2)


        # Commands
        self.command_setup_frame  = tk.Frame(self.parameter_frame,highlightbackground='black', highlightthickness=2)
        self.command_setup_frame.grid(row=3,column=0   ,padx=1,rowspan=1)
        l5 = tk.Label(
            self.command_setup_frame,
            text="Commands", 
            bg="#f1f8e9", 
            font=("Helvetica", 12, "bold")
        )
        l5.grid(row=0,column=0,columnspan=3)
        self.commands = Commands(self.command_setup_frame,self.protocol_handler)
        self.commands.render_commands(2)


        
    def _on_mousewheel(self, event):
        print(event)
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _linux_scroll_up(self,event):
        self.canvas.yview_scroll(-2,"units")

    def _linux_scroll_down(self,event):
        self.canvas.yview_scroll(2,"units")

    def update_all_params(self):
        if not self.port_open:
            messagebox.showerror("Error", "Com Port not Open!")
            return
        try:
            self.parameters_ro.read_all()
            self.parameters_g.read_all()
            self.parameters_pos.read_all()
            self.parameters_i.read_all()
            self.parameters_v.read_all()
        except Exception as ex:
            messagebox.showerror("Error", f'{ex}')
        
    def open_com_port(self):
        if not self.port_open:
            comm_str =  self.com_port_txt.get()
            try:
                self.com_handle = serial.Serial(comm_str, 19200,timeout=1)
                if self.com_handle.is_open:
                    self.port_open = True
                    self.protocol_handler.ser_handle = self.com_handle
            except Exception as ex:
                messagebox.showerror("Error", f'{ex}')

if __name__ == "__main__":
    # Instantiate and run the application
    app = App()
    app.mainloop()