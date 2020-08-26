from tkinter import *
from tkinter import messagebox
import StartingPage
import socket
import pickle


class create_new_account:
    def __init__(self):
        self.create_new_account_window=Tk()
        self.create_new_account_window.title("Create new account")
        self.create_new_account_window.geometry("400x250")
        self.create_new_account_window.resizable(False,False)

        self.first_name_label=Label(self.create_new_account_window,text="First Name:",font=("Courier",15))
        self.first_name_label.grid(row=0,column=0,pady=10)

        self.first_name_text=Entry(self.create_new_account_window,width=30)
        self.first_name_text.grid(row=0,column=1)

        self.last_name_label=Label(self.create_new_account_window,text="Last Name:",font=("Courier",15))
        self.last_name_label.grid(row=1,column=0,padx=30)

        self.last_name_text = Entry(self.create_new_account_window, width=30)
        self.last_name_text.grid(row=1, column=1)

        self.username_label = Label(self.create_new_account_window, text="User Name:", font=("Courier", 15))
        self.username_label.grid(row=2, column=0, pady=10)

        self.username_text = Entry(self.create_new_account_window, width=30)
        self.username_text.grid(row=2, column=1)

        self.password_label = Label(self.create_new_account_window, text="Password:", font=("Courier", 15))
        self.password_label.grid(row=3, column=0, padx=30)

        self.password_text = Entry(self.create_new_account_window, show="*", width=30)
        self.password_text.grid(row=3, column=1)

        self.fill=Label(self.create_new_account_window,text="")
        self.fill.grid(row=4,column=0)
        self.fill.grid(row=4,column=1)

        self.create_new_account_button = Button(self.create_new_account_window, text="Create New Account",width=25,command=self.create_new_account_action)
        self.create_new_account_button.grid(row=5,column=1)

        self.create_new_account_window.mainloop()


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




    def create_new_account_action(self):
        if self.first_name_text.get()=="" or self.last_name_text.get()=="" or self.username_text.get()=="" or self.password_text.get()=="":
            messagebox.showerror('Error','Please fill all the details.')
        else:
            data=[]
            data.append(self.first_name_text.get())
            data.append(self.last_name_text.get())
            data.append(self.username_text.get())
            data.append(self.password_text.get())
            message=pickle.dumps(data)
            message=bytes(f"{len(message):<20}",'utf-8')+message
            try:
                StartingPage.server.send(bytes(f"{len('new_account'):<20}" + 'new_account', 'utf-8'))
                StartingPage.server.send(message)
                check=self.receive_data(StartingPage.server)
                if check=='true':
                    messagebox.showinfo('Success','Successfully created new account. Please retart the app and login to continue.')
                    self.create_new_account_window.destroy()
                else:
                    messagebox.showerror('Username already exists','Username already exists. Please choose a different user name.')
            except:
                messagebox.showerror('Error','An error occured while creating a new account. Please restart the app and try again.')
                self.create_new_account_window.destroy()

