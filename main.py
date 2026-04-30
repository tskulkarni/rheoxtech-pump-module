import tkinter as tk
from parameter import Parameters
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # 1. Configure the main application window
        self.title("Two-Pane Layout Framework")
        self.geometry("1424x720")
        self.minsize(1024, 720)

        # 2. Configure the grid for the main window
        # weight=1 allows the columns/rows to expand when the window is resized
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1) # Left column
        self.grid_columnconfigure(1, weight=1) # Right column

        # 3. Initialize the Left Frame
        # Background colors are added temporarily to make the layout visible
        self.left_frame = tk.Frame(self, bg="#e0f7fa")
        self.left_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # 4. Initialize the Right Frame
        self.right_frame = tk.Frame(self, bg="#f1f8e9")
        self.right_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)

        # 5. Populate the frames with widgets
        self.build_left_frame()
        self.build_right_frame()

    def build_left_frame(self):
        """Add widgets to the left frame."""
        label = tk.Label(
            self.left_frame, 
            text="Left Panel Content", 
            bg="#e0f7fa", 
            font=("Helvetica", 14, "bold")
        )
        label.pack(pady=20)
        
        # Example button
        btn = tk.Button(self.left_frame, text="Action 1")
        btn.pack(pady=10)

    def build_right_frame(self):
        """Add widgets to the right frame."""
        label = tk.Label(
            self.right_frame, 
            text="Paramters", 
            bg="#f1f8e9", 
            font=("Helvetica", 14, "bold")
        )
        label.pack(pady=4)
        self.update_all_button = tk.Button(self.right_frame, text="UPDATE ALL", width=20,command=self.update_all_params)
        self.update_all_button.pack(pady=4)
        self.canvas = tk.Canvas(self.right_frame,  bg="white")
        self.canvas.pack(side=tk.LEFT,fill='both',expand=True)
        self.scrollbar = tk.Scrollbar(self.right_frame, orient=tk.VERTICAL, width=16, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        scrollable_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=scrollable_frame,anchor="nw")
        
        self.canvas.bind_all("<Button-4>", self._linux_scroll_up)
        self.canvas.bind_all("<Button-5>", self._linux_scroll_down)


        scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.parameters = Parameters(scrollable_frame)
        self.parameters.render_parameters(2)
        
    def _on_mousewheel(self, event):
        print(event)
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _linux_scroll_up(self,event):
        self.canvas.yview_scroll(-2,"units")

    def _linux_scroll_down(self,event):
        self.canvas.yview_scroll(2,"units")

    def update_all_params(self):
        pass        

if __name__ == "__main__":
    # Instantiate and run the application
    app = App()
    app.mainloop()