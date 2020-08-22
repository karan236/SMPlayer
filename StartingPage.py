from tkinter import *
import ContinueWithoutLogin

class Starting_Page:
    def __init__(self):
        self.root = Tk()
        self.root.title("Social Player")
        self.root.geometry("725x275")
        self.root.resizable(False, False)

        img = PhotoImage(file="imge.png")

        self.welcome_image = Label(self.root, image=img)
        self.welcome_image.pack()

        self.about_button = Button(self.root, text="About", width=10, command=lambda: self.about(self.root))
        self.about_button.pack(side="left", padx=2)

        self.login_button = Button(self.root, text="Login", width=10, command=lambda: self.login(self.root))
        self.login_button.pack(side="right", padx=2)

        self.continue_without_login_button = Button(self.root, text="Continue Without Login", width=30,
                                               command=lambda: self.continue_without_login_action(self.root))
        self.continue_without_login_button.pack(side="right", padx=2)

        self.root.mainloop()

    def about(self,root):
        pass

    def login(self,root):
        root.destroy()

    def continue_without_login_action(self,root):
        root.destroy()
        ContinueWithoutLogin.continue_without_login()