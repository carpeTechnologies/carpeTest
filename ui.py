import tkinter as tk

class LaunchScreen:
    def __init__(self, root, submit_callback):
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

        # Store the callback function
        self.submit_callback = submit_callback

    def submit(self):
        # Get input values and store them in variables
        field_values = [field.get() for field in self.fields]
        # Call the submit callback function with the field values
        self.submit_callback(field_values)
        # Close the launch screen window
        self.root.destroy()


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
        # Check if the index is within the valid range
        if index < 0 or index >= len(self.tabs):
            return
        
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

            # Adjust the current_tab_index if necessary
            if self.current_tab_index >= len(self.tabs):
                # If the current tab index is out of bounds after removal, set it to the last tab
                self.current_tab_index = len(self.tabs) - 1
            
            # Show the next tab
            self.show_tab(self.current_tab_index)
        else:
            print("Cannot close the last tab.")
