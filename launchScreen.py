import tkinter as tk

class LaunchScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Launch Screen")

        # Create input fields
        self.fields = []
        fields_data = ["Secret Key:", "Shared Key 2:", "Nep-Organization:", "Nep-Enterprise-Unit:"]
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

if __name__ == "__main__":
    launch()
