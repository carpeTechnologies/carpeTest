import tkinter as tk

class LaunchScreen:
    def __init__(self, root, onSubmit=None):
        self.root = root
        self.root.title("Launch Screen")

        # Create input fields
        self.fields = []
        fields_data = ["Secret Key:", "Shared Key:", "Nep-Organization:", "Nep-Enterprise-Unit / Site ID:"]
        for data in fields_data:
            label = tk.Label(root, text=data)
            label.pack()
            entry = tk.Entry(root)
            entry.pack()
            self.fields.append(entry)

        # Create submit button
        submit_button = tk.Button(root, text="Submit", command=self.submit)
        submit_button.pack()

    def submit(self):
        # Get input values and store them in variables
        field_values = [field.get() for field in self.fields]
        self.root.destroy()  # Close the launch screen window
        # self.root.quit()  # Quit the main loop
        print(field_values)
        return field_values

    def launch():
        root = tk.Tk()
        app = LaunchScreen(root)
        root.mainloop()
        return app.submit()

class TabApp:
    def __init__(self, root, orders):
        self.root = root
        self.root.title("Dynamic Orders Tabs Example")
        
        # Create the header frame to hold the tab buttons
        self.header_frame = tk.Frame(root)
        self.header_frame.pack(side=tk.TOP, fill=tk.X)
        
        # Create a frame for the main content area
        self.content_frame = tk.Frame(root)
        self.content_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        
        # Initialize tabs list and current tab index
        self.tabs = []
        self.current_tab_index = 0
        
        # Create tabs for each order
        for order in orders:
            self.add_tab(order)
        
        # Show the first tab
        if self.tabs:
            self.show_tab(0)
        
    def add_tab(self, order):
        tab_index = len(self.tabs)
        name = f"Order {order['id']}"
        
        # Create a button for the tab
        tab_button = tk.Button(self.header_frame, text=name, command=lambda idx=tab_index: self.show_tab(idx))
        tab_button.pack(side=tk.LEFT)
        
        # Create a frame for the tab content
        tab_content = tk.Frame(self.content_frame)
        label = tk.Label(tab_content, text=f"Order ID: {order['id']}\nOrder Total Price: {order['totals'][0]['value']}")
        label.pack(pady=20)
        close_button = tk.Button(tab_content, text="Close Tab", command=self.close_current_tab)
        close_button.pack(pady=20)
        
        # Add tab to the list
        self.tabs.append((tab_button, tab_content))
        
    def show_tab(self, index):
        # Hide all tabs
        for _, content in self.tabs:
            content.pack_forget()
        
        # Show the selected tab
        self.tabs[index][1].pack(fill=tk.BOTH, expand=True)
        self.current_tab_index = index
        
    def close_current_tab(self):
        if len(self.tabs) > 1:  # Ensure there's at least one tab left
            # Remove the current tab
            tab_button, tab_content = self.tabs.pop(self.current_tab_index)
            tab_button.pack_forget()  # Remove the tab button from display
            tab_button.destroy()
            tab_content.destroy()
            
            # Calculate the new width for the remaining tab buttons
            new_width = self.header_frame.winfo_width() // len(self.tabs)
            
            # Update the width of the remaining tab buttons
            for button, _ in self.tabs:
                button.config(width=new_width)
            
            # Show the next tab, if available
            next_index = self.current_tab_index % len(self.tabs)
            self.show_tab(next_index)

            # Resize the window to its original size
            self.root.update_idletasks()
            self.root.geometry(f"{self.root.winfo_width()}x{self.root.winfo_height()}")