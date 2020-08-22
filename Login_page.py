from tkinter import *

class LogIn:
    def __init__(self):
        self.login_window=Tk()
        self.login_window.title("Login")
        self.login_window.geometry("400x150")
        self.login_window.resizable(False,False)

        self.username_label=Label(self.login_window,text="User Name:",font=("Courier",15))
        self.username_label.grid(row=0,column=0,pady=10)

        self.username_text=Entry(self.login_window,width=30)
        self.username_text.grid(row=0,column=1)

        self.password_label=Label(self.login_window,text="Password:",font=("Courier",15))
        self.password_label.grid(row=1,column=0,padx=30)

        self.password_text = Entry(self.login_window, show="*", width=30)
        self.password_text.grid(row=1, column=1)

        self.fill=Label(self.login_window,text="")
        self.fill.grid(row=2,column=0)
        self.fill.grid(row=2,column=1)
        self.fill.grid(row=3, column=0)

        self.login_button=Button(self.login_window,text="Login",width=10)
        self.login_button.grid(row=4,column=0)

        self.create_new_account_button = Button(self.login_window, text="Create New Account",width=25)
        self.create_new_account_button.grid(row=4,column=1)

        self.login_window.mainloop()


LogIn()