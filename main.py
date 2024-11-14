import tkinter as Tk
import tkinter.messagebox as msg
from window import Welcome
import sqlite3
import bcrypt

class Login(Tk.Tk):
    def __init__(self):
        super().__init__()

        self.conn = sqlite3.connect('myData.db')
        self.cur = self.conn.cursor()

        self.title('Login Page')
        self.resizable(0,0)
        self.geometry('300x150')

        self.username_lbl = Tk.Label(self, text='Username')
        self.username_lbl.pack()
        self.username_entry = Tk.Entry(self)
        self.username_entry.pack()

        self.password_lbl = Tk.Label(self, text='Password')
        self.password_lbl.pack()
        self.password_entry = Tk.Entry(self, show="*")
        self.password_entry.pack()

        self.login_button = Tk.Button(self, text='Login', command=self.Validate_Login)
        self.login_button.pack()
        self.signup_button = Tk.Button(self, text='Signup', command=self.Validate_Signup)
        self.signup_button.pack()

    def Validate_Signup(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == '' or password == '':
            msg.showerror('Error', 'Please enter all fields')
        else:
            self.cur.execute("SELECT * FROM loginApp WHERE Username=?", (username,))
            result = self.cur.fetchone()

            if result is None:
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

                enterThese = (username, hashed_password)
                self.cur.execute("INSERT into loginApp VALUES(?,?)", (enterThese))
                self.conn.commit()

                msg.showinfo('Success', 'You have successfully signed up!')
            else:
                msg.showerror('Error', 'Username already exists')

    def Validate_Login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == '' or password == '':
            msg.showerror('Error', 'Please enter all fields')
        else:
            self.cur.execute("SELECT * FROM loginApp WHERE Username=?", (username,))
            result = self.cur.fetchone()

            if result is None:
                msg.showerror('Error', 'Username does not exist')
            else:
                if bcrypt.checkpw(password.encode('utf-8'), result[1]):
                    myWelcome = Welcome(self.conn, self.cur).setBanner(self.username_entry.get())
                    # self.withdraw()
                else:
                    msg.showerror('Error', 'Password is not valid')

if __name__ == '__main__':
    myApp = Login()
    myApp.mainloop()