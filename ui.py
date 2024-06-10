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

        # Create a frame for the main content area
        self.content_frame = tk.Frame(root)
        self.content_frame.grid(row=2, column=0, sticky=tk.NSEW)

        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=0)  # Adjusted weight for row 0
        self.root.grid_rowconfigure(1, weight=0)  # Adjusted weight for row 1
        self.root.grid_rowconfigure(2, weight=1)

        # Initialize orders and current order index
        self.orders = orders
        self.current_order_index = 0

        # Create the first order tab
        if self.orders:
            self.show_order(self.current_order_index)
        else:
            self.show_no_orders_message()

    def show_order(self, index):
        order = self.orders[index]

        # Clear the content frame
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        left_container = tk.Frame(self.content_frame)
        left_container.grid(row=0, column=0, sticky='nsew')
        left_container.grid_rowconfigure(0, weight=1)
        left_container.grid_rowconfigure(1, weight=3)
        left_container.grid_rowconfigure(2, weight=1)
        left_container.grid_columnconfigure(0, weight=1)
        left_container.grid_columnconfigure(1, weight=1)
        left_container.grid_columnconfigure(2, weight=1)

        # Create a frame for the order details
        order_details_frame = tk.Frame(left_container)
        order_details_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')
        order_details_frame.grid_columnconfigure(0, weight=1)

        padFromTop = 35
        lineItemPadding = 5

        
        # Create and place label for the order number at the top
        order_number_label = tk.Label(order_details_frame, text=f"Order Number: {order['id']}", font=('Helvetica', 22, 'bold'), pady = padFromTop)
        order_number_label.grid(row=0, column=0, columnspan=2, sticky='n')

        # Display order lines
        for i, line in enumerate(order.get('orderLines', []), start=1):
            description = line.get('description', '')
            unit_price = line.get('unitPrice', 0)
            quantity = line.get('quantity', {}).get('value', 0)

            # Create and place labels for quantity, description, and price
            qty_desc_label = tk.Label(order_details_frame, text = f"{quantity} x {description}", anchor = 'w', font = ('Helvetica', 18), pady = lineItemPadding)
            qty_desc_label.grid(row=i, column=0, sticky='w', padx = (10,10))

            price_label = tk.Label(order_details_frame, text = f"${unit_price:.2f}", anchor = 'e', font = ('Helvetica', 18), pady = lineItemPadding)
            price_label.grid(row = i, column = 1, sticky = 'ew')

        # Create a frame for total price
        total_frame = tk.Frame(left_container)
        total_frame.grid(row=2, column=1, sticky='e', pady=(10, 0))

        # Create label for order total price and set it to bold
        total_price = sum(line.get('unitPrice', 0) * line.get('quantity', {}).get('value', 0) for line in order.get('orderLines', []))
        total_label = tk.Label(total_frame, text="Total Price:", font=('Helvetica', 18, 'bold'), anchor='w')
        total_label.grid(row=0, column=0, sticky='w')

        price_label = tk.Label(total_frame, text=f"${total_price:.2f}", font=('Helvetica', 18, 'bold'), anchor='e')
        price_label.grid(row=0, column=1, sticky='e')

        # Create a container frame for the right side
        right_container = tk.Frame(self.content_frame)
        right_container.grid(row=0, column=1, sticky=tk.NSEW)

        # Adjust column weights to occupy right half of the screen
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # Create a frame for the fixed-size buttons
        button_frame = tk.Frame(right_container)
        button_frame.grid(row=1, column=0, padx=10, sticky=tk.N)
        orderConf = tk.Label(right_container, text = "Is this order correct?", font = ('Helvetica', 18, 'bold'), anchor = 'n')
        orderConf.grid(row=0, column=0, columnspan = 2, sticky='w', pady = padFromTop)

        # Create Yes and No buttons with fixed size
        close_button = tk.Button(button_frame, text="Yes", command=self.close_current_order, width=10, height=2)
        close_button.grid(row=1, column=0, padx=5)

        no_button = tk.Button(button_frame, text="No", width=10, height=2)
        no_button.grid(row=1, column=1, padx=5)

        # Update the window title
        self.root.title(f"Order {order['id']}")

    def next_order(self):
        self.current_order_index = (self.current_order_index + 1) % len(self.orders)
        self.show_order(self.current_order_index)

    def close_current_order(self):
        if self.orders:
            # Remove the current order
            self.orders.pop(self.current_order_index)

            # Adjust the current_order_index if necessary
            if self.current_order_index >= len(self.orders):
                self.current_order_index = 0

            # Show the next order or the no orders message
            if self.orders:
                self.show_order(self.current_order_index)
            else:
                self.show_no_orders_message()

    def show_no_orders_message(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        no_orders_label = tk.Label(self.content_frame, text="No orders to show!", font=('Helvetica', 24))
        no_orders_label.pack(expand=True)
        self.root.title("Carpe")