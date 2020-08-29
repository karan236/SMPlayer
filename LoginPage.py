from tkinter import *
from tkinter import messagebox
import CreateNewAccount
import StartingPage
import pickle
import socket

class login:
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

        self.login_button=Button(self.login_window,text="Login",width=10,command=self.login_action)
        self.login_button.grid(row=4,column=0)

        self.create_new_account_button = Button(self.login_window, text="Create New Account",width=25,command=self.create_new_account_action)
        self.create_new_account_button.grid(row=4,column=1)

        self.login_window.mainloop()



    def receive_data(self,server):
        full_msg = b''
        new_msg = True
        msglen=0
        while True:
            msg = server.recv(64)
            if new_msg:
                msglen = int(msg[:20])
                new_msg = False

            full_msg += msg

            if len(full_msg) - 20 == msglen:
                new_msg = True
                return full_msg[20:].decode()


    def login_action(self):
        if self.username_text.get()=="" or self.password_text.get()=="":
            messagebox.showerror('Error!','Please fill up all the details.')
        else:
            data = []
            data.append(self.username_text.get())
            data.append(self.password_text.get())
            message = pickle.dumps(data)
            message = bytes(f"{len(message):<20}", 'utf-8') + message
            try:
                StartingPage.server.send(bytes(f"{len('login'):<20}" + 'login', 'utf-8'))
                StartingPage.server.send(message)
                check=self.receive_data(StartingPage.server)
                if check=='true':
                    messagebox.showinfo('Success', 'Login Successfull!')
                else:
                    messagebox.showerror('Error','Invalid User Name or Password.')
            except:
                messagebox.showerror('Error',
                                     'An error occured while creating a new account. Please restart the app and try again.')
                self.login_window.destroy()


    def create_new_account_action(self):
        self.login_window.destroy()
        CreateNewAccount.create_new_account()