import tkinter as Tk
import tkinter.messagebox as msg

class Welcome(Tk.Toplevel):
    def __init__(self, connection, cursor):
        super().__init__()

        self.connection = connection
        self.cursor = cursor

        self.title('Welcome Page')
        self.resizable(0, 0)
        self.geometry('330x300')
        self.configure(bg='#fee6e1')

        self.banner = Tk.StringVar(self)

        self.hello_lbl = Tk.Label(self, textvariable=self.banner, bg='#fee6e1')
        self.hello_lbl.place(x=35, y=20)

        self.frame = Tk.Frame(self, bg='#fee6e1')
        self.frame.place(x=35, y=60, width=260, height=120)

        self.scrollbar = Tk.Scrollbar(self.frame)
        self.scrollbar.pack(side=Tk.RIGHT, fill=Tk.Y)

        self.listbox = Tk.Listbox(self.frame, selectmode=Tk.SINGLE, yscrollcommand=self.scrollbar.set, width=30, height=6)
        self.listbox.pack(side=Tk.LEFT, fill=Tk.BOTH)
        self.scrollbar.config(command=self.listbox.yview)

        self.add_btn = Tk.Button(self, text="Add", command=self.open_add_window)
        self.add_btn.place(x=35, y=200)
        self.edit_btn = Tk.Button(self, text="Edit", command=self.open_edit_window)
        self.edit_btn.place(x=130, y=200)
        self.delete_btn = Tk.Button(self, text="Delete", command=self.delete_data)
        self.delete_btn.place(x=225, y=200)

        self.refresh_btn = Tk.Button(self, text="Refresh", command=self.refresh_list)
        self.refresh_btn.place(x=130, y=240)

        self.refresh_list()

    def setBanner(self, welcomeName):
        self.banner.set(f"Welcome {welcomeName}")

    def refresh_list(self):
        self.listbox.delete(0, Tk.END)
        self.cursor.execute("SELECT * FROM customers")
        results = self.cursor.fetchall()

        for item in results:
            self.insert_to_list(item)

    def insert_to_list(self, item):
        id = item[0]
        firstName = item[1]
        lastName = item[2]

        self.listbox.insert(Tk.END, f"{id} | {firstName} {lastName}")

    def delete_data(self):
        try:
            selected_index = self.listbox.curselection()[0]
            selected_item = self.listbox.get(selected_index)
            selected_id = selected_item.split(" | ")[0]

            self.cursor.execute("DELETE FROM customers WHERE ID = ?", (selected_id,))
            self.connection.commit()

            self.refresh_list()
        except IndexError:
            msg.showwarning("Delete Data", "Please select an item to delete.")

    def open_add_window(self):
        self.open_input_window()

    def open_edit_window(self):
        try:
            selected_index = self.listbox.curselection()[0]
            selected_item = self.listbox.get(selected_index)
            selected_id = selected_item.split(" | ")[0]

            self.cursor.execute("SELECT * FROM customers WHERE ID = ?", (selected_id,))
            customer = self.cursor.fetchone()

            if customer:
                self.open_input_window(customer)
        except IndexError:
            msg.showwarning("Edit Data", "Please select an item to edit.")

    def open_input_window(self, customer=None):
        input_window = Tk.Toplevel(self)
        input_window.title("Customer Information")
        input_window.geometry("300x200")

        Tk.Label(input_window, text="First Name:").pack()
        first_name_entry = Tk.Entry(input_window)
        first_name_entry.pack()

        Tk.Label(input_window, text="Last Name:").pack()
        last_name_entry = Tk.Entry(input_window)
        last_name_entry.pack()

        Tk.Label(input_window, text="Email:").pack()
        email_entry = Tk.Entry(input_window)
        email_entry.pack()

        if customer:
            first_name_entry.insert(0, customer[1])
            last_name_entry.insert(0, customer[2])
            email_entry.insert(0, customer[3])

        save_button = Tk.Button(input_window, text="Save",
                                command=self.save_window_data(input_window, first_name_entry, last_name_entry,
                                                                      email_entry, customer))
        save_button.pack()

        cancel_button = Tk.Button(input_window, text="Cancel", command=input_window.destroy)
        cancel_button.pack()

    def save_window_data(self, input_window, first_name_entry, last_name_entry, email_entry, customer=None):
        def command():
            self.save_data(input_window, first_name_entry.get(), last_name_entry.get(), email_entry.get(), customer)

        return command

    def save_data(self, window, first_name, last_name, email, customer=None):
        if not first_name or not last_name or not email:
            msg.showwarning("Input Error", "All fields are required.")
            return

        if customer:
            self.cursor.execute("UPDATE customers SET FirstName = ?, LastName = ?, Email = ? WHERE ID = ?",
                                (first_name, last_name, email, customer[0]))
            self.connection.commit()

            self.refresh_list()
        else:
            self.cursor.execute("INSERT INTO customers (FirstName, LastName, Email) VALUES (?, ?, ?)",
                                (first_name, last_name, email))
            self.connection.commit()

            self.refresh_list()

        window.destroy()
        msg.showinfo("Success", "Customer data saved successfully.")
