import tkinter as tk
from tkinter import ttk
import tkmacosx as tkmac

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

        # field_values = ['2a8e9a34a61c45e1850963054b704f82','b1d4a804aa0241babd77e3ab08fece2a', 'test-drive-000aeaece5fe49d7891a8', '9af39a319af44df58b2b332c7b759c5f']
        field_values = ['2a8e9a34a61c45e1850963054b704f82','b1d4a804aa0241babd77e3ab08fece2a', 'test-drive-000aeaece5fe49d7891a8', 'f8873705ecfb41919875c14bf59c1fb2']
        self.submit_callback(field_values)
        # Close the launch screen window
        self.root.destroy()

class TabApp:
    def __init__(self, root):
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
        self.orders = []
        self.incorrect_orders = [] 
        self.correct_orders = [] 
        self.processed_orders = set()
        self.current_order_index = 0

    def addProcessedOrder(self, order_id):
        self.processed_orders.add(order_id)

    def getProcessedOrders(self):
        return self.processed_orders

    def update_orders(self, new_orders):
        if new_orders:
            self.orders = new_orders
            self.current_order_index = 0
            self.show_order(self.current_order_index)
        else:
            self.show_no_orders_message()

    def show_order(self, index):
        if not self.orders:
            self.show_no_orders_message()
            return

        while self.orders and (self.orders[index]['id'] in self.incorrect_orders or self.orders[index]['id'] in self.correct_orders):
            self.orders.pop(index)
            if not self.orders:
                self.show_no_orders_message()
                return
            index %= len(self.orders)

        if not self.orders:
            self.show_no_orders_message()
            return

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
        standardText = ('Helvetica', 18)
        standardTextBold = ('Helvetica', 18, 'bold')
        # Create and place label for the order number at the top
        order_number_label = tk.Label(order_details_frame, text=f"Order Number: {order['id']}", font=('Helvetica', 22, 'bold'), pady=padFromTop)
        order_number_label.grid(row=0, column=0, columnspan=2, sticky='n')

        # Display order lines
        for i, line in enumerate(order.get('orderLines', []), start=1):
            description = line.get('description', '')
            unit_price = line.get('unitPrice', 0)
            quantity = line.get('quantity', {}).get('value', 0)

            # Create and place labels for quantity, description, and price
            qty_desc_label = tk.Label(order_details_frame, text=f"{quantity} x {description}", anchor='w', font=standardText, pady=lineItemPadding)
            qty_desc_label.grid(row=i, column=0, sticky='w', padx=(10, 10))

            price_label = tk.Label(order_details_frame, text=f"${unit_price:.2f}", anchor='e', font=standardText, pady=lineItemPadding)
            price_label.grid(row=i, column=1, sticky='ew')

        total_price = sum(line.get('unitPrice', 0) * line.get('quantity', {}).get('value', 0) for line in order.get('orderLines', []))

        # Create label for order total price and set it to bold
        total_label = tk.Label(order_details_frame, text="Total Price:", font=standardTextBold, anchor='w')
        total_label.grid(row=len(order.get('orderLines', [])) + 1, column=0, sticky='e', pady=(10, 0))

        price_label = tk.Label(order_details_frame, text=f"${total_price:.2f}", font=standardTextBold, anchor='e')
        price_label.grid(row=len(order.get('orderLines', [])) + 1, column=1, sticky='e', pady=(10, 0))

        # Create a container frame for the right side
        right_container = tk.Frame(self.content_frame)
        right_container.grid(row=0, column=1, sticky=tk.NSEW)

        # Adjust column weights to occupy right half of the screen
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(1, weight=1)

        # Create a frame for the fixed-size buttons
        button_frame = tk.Frame(right_container)
        button_frame.grid(row=1, column=0, columnspan=2, padx=10, sticky=tk.N)
        orderConf = tk.Label(right_container, text="Is this order correct?", font=('Helvetica', 25, 'bold'), anchor='n')
        orderConf.grid(row=0, column=1, columnspan=1, sticky='w', pady=padFromTop)

        # Center the two columns in right_container
        right_container.grid_columnconfigure(0, weight=1)
        right_container.grid_columnconfigure(1, weight=1)

        # Create Yes and No buttons with fixed size
        confButtonWidths = 5
        confButtonHeights = 2
        buttonFont = ('Helvetica', 58)
        close_button = tkmac.Button(button_frame, text="Yes", font=buttonFont, bg='green', fg='white', command=lambda: self.orderCorrect(order['id']))
        close_button.grid(row=1, column=0)

        no_button = tkmac.Button(button_frame, text="No", font=buttonFont, bg='#ff4122', fg='white', command=lambda: self.orderIncorrect(order['id']))
        no_button.grid(row=1, column=1, padx=5)

        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)
        # Update the window title 
        self.root.title(f"Order {order['id']}")

    def orderIncorrect(self, order_id):
        print(f'ALERT: Order Number: {order_id} is wrong!')
        self.close_current_order()
        self.incorrect_orders.append(order_id)

    def orderCorrect(self, order_id):
        print(f'Order Number: {order_id} is correct!')
        self.close_current_order()
        self.correct_orders.append(order_id)

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

    def getOrders(self):
        return self.orders

    def get_incorrect_orders(self):
        return self.incorrect_orders

    def get_correct_orders(self):
        return self.correct_orders