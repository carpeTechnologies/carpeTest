import tkinter as tk
from tkinter import ttk

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
        # field_values = [field.get() for field in self.fields] ## this is critical to getting the field inputs!

        field_values = ['2a8e9a34a61c45e1850963054b704f82','b1d4a804aa0241babd77e3ab08fece2a', 'test-drive-000aeaece5fe49d7891a8', '9af39a319af44df58b2b332c7b759c5f']
        self.submit_callback(field_values)
        # Close the launch screen window
        self.root.destroy()

class TabApp:
    def __init__(self, root, orders):
        self.root = root
        self.root.title("Carpe")

        # Set a fixed window size and prevent resizing
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.root.geometry(f"{screen_width}x{screen_height}")

        # Create a canvas and horizontal scrollbar
        self.canvas = tk.Canvas(root)
        self.canvas.grid(row=1, column=0, sticky=tk.NSEW)  # Placed in row 1
        self.scrollbar = ttk.Scrollbar(root, orient='horizontal', command=self.canvas.xview)
        self.scrollbar.grid(row=0, column=0, sticky=tk.EW)  # Placed in row 0, above the canvas
        self.canvas.configure(xscrollcommand=self.scrollbar.set)

        # Create a frame for the header (tab buttons) inside the canvas
        self.header_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.header_frame, anchor='nw')

        # Create a frame for the main content area
        self.content_frame = tk.Frame(root)
        self.content_frame.grid(row=2, column=0, sticky=tk.NSEW)

        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)  # Adjusted weight for row 0
        self.root.grid_rowconfigure(1, weight=1)  # Adjusted weight for row 1
        self.root.grid_rowconfigure(2, weight=1)

        # Initialize tabs list and current tab index
        self.tabs = []
        self.current_tab_index = 0
        self.no_orders_label = None

        # Create tabs for each order
        for order in orders:
            self.add_tab(order)

        # Show the first tab or no orders message
        if self.tabs:
            self.show_tab(0)
        else:
            self.show_no_orders_message()

    def add_tab(self, order):
        tab_index = len(self.tabs)
        name = f"Order {order['id']}"

        # Create a button for the tab
        tab_button = tk.Button(self.header_frame, text=name, command=lambda idx=tab_index: self.show_tab(idx))
        tab_button.pack(side=tk.LEFT, padx=5, pady=5)  # Adjust padding between buttons

        # Create a frame for the tab content
        tab_content = tk.Frame(self.content_frame)
        tab_content.pack(expand=True, fill=tk.BOTH)  # Expand to fill the available space

        # Create label for order ID and price
        order_info_label = tk.Label(tab_content, text=f"Order ID: {order['id']}\nOrder Total Price: {order['totals'][0]['value']}")
        order_info_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)  # Center the label
        
        # Create close button for the tab
        close_button = tk.Button(tab_content, text="Close Tab", command=self.close_current_tab)
        close_button.place(relx=0.5, rely=0.6, anchor=tk.CENTER)  # Center the button

        # Add tab to the list
        self.tabs.append((tab_button, tab_content))

        # Update canvas scroll region
        self.header_frame.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def show_tab(self, index):
        # Check if the index is within the valid range
        if index < 0 or index >= len(self.tabs):
            return

        # Hide content of other tabs
        for _, content in self.tabs:
            content.pack_forget()

        # Show the selected tab
        self.tabs[index][1].pack(expand=True, fill=tk.BOTH)

        # Update the current tab index
        self.current_tab_index = index
        order_number = self.tabs[index][0]['text'].split()[1]  # Extract order number from tab button text
        self.root.title(f"Order {order_number}")

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

            # Rebind tab button commands to correct indices
            for idx, (button, _) in enumerate(self.tabs):
                button.config(command=lambda idx=idx: self.show_tab(idx))

            # Show the next tab
            self.show_tab(self.current_tab_index)
        else:
            # Remove the last tab
            tab_button, tab_content = self.tabs.pop(self.current_tab_index)
            tab_button.pack_forget()
            tab_button.destroy()
            tab_content.destroy()

            # Display 'No orders to show' message
            self.show_no_orders_message()

    def show_no_orders_message(self):
        if self.no_orders_label is None:
            self.no_orders_label = tk.Label(self.content_frame, text="No orders to show!", font=('Helvetica', 24))
        for widget in self.content_frame.winfo_children():
            widget.grid_forget()
        self.no_orders_label.grid(row=0, column=0, sticky=tk.NSEW)  # Use grid to place the label
        self.root.title("Carpe")
