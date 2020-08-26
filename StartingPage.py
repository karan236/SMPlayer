from tkinter import *
import ContinueWithoutLogin
import LoginPage
import socket
from tkinter import messagebox

server=socket.socket()

class Starting_Page:
    def __init__(self):
        self.host='localhost'
        self.port=9999

        self.root = Tk()
        self.root.title("Social Player")
        self.root.geometry("725x275")
        self.root.resizable(False, False)

        img = PhotoImage(file="imge.png")

        self.welcome_image = Label(self.root, image=img)
        self.welcome_image.pack()

        self.about_button = Button(self.root, text="About", width=10, command=self.about)
        self.about_button.pack(side="left", padx=2)

        self.login_button = Button(self.root, text="Login", width=10, command=self.login)
        self.login_button.pack(side="right", padx=2)

        self.continue_without_login_button = Button(self.root, text="Continue Without Login", width=30,
                                               command=self.continue_without_login_action)
        self.continue_without_login_button.pack(side="right", padx=2)

        self.root.mainloop()

    def about(self):
        pass

    def login(self):
        try:
            server.connect((self.host,self.port))
            self.root.destroy()
            LoginPage.login()
        except:
            messagebox.showerror('Connection Error!','Please check you internet connection and retry.')

    def continue_without_login_action(self):
        self.root.destroy()
        ContinueWithoutLogin.continue_without_login()