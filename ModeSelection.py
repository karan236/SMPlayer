from tkinter import *
from threading import *
import time

class Mode_Selection:
    def __init__(self):
        self.running=True

        self.mode_selection_window=Tk()
        self.mode_selection_window.title("Room")
        self.mode_selection_window.geometry("400x250")
        self.mode_selection_window.resizable(False,False)
        self.radio_button_input=IntVar()

        self.join_room_radiobutton = Radiobutton(self.mode_selection_window, text="Join room.", variable=self.radio_button_input, value=1,
                                       font=('Courier', 10),command=self.join_room_action)
        self.join_room_radiobutton.pack()

        self.room_id_label=Label(self.mode_selection_window,text='Room Id: ',state="disabled")
        self.room_id_label.pack()

        self.room_id_text=Entry(self.mode_selection_window,width=30,state="disabled")
        self.room_id_text.pack()

        self.room_password_label=Label(self.mode_selection_window,text="Room Password: ",state="disabled")
        self.room_password_label.pack()

        self.room_password_text=Entry(self.mode_selection_window,show='*',width=30,state="disabled")
        self.room_password_text.pack()

        self.create_room_radiobutton=Radiobutton(self.mode_selection_window,text="Create room.",variable=self.radio_button_input,value=2,font=('Courier',10),command=self.create_room_action)
        self.create_room_radiobutton.pack(pady=20)

        self.join_button=Button(self.mode_selection_window,text='Join',state="disabled")
        self.join_button.pack(pady=5)

        self.create_button=Button(self.mode_selection_window,text='Create',state="disabled")
        self.create_button.pack()

        self.mode_selection_window.mainloop()

    def join_room_action(self):
        self.join_button.config(state='normal')
        self.room_id_label.config(state='normal')
        self.room_id_text.config(state='normal')
        self.room_password_label.config(state='normal')
        self.room_password_text.config(state='normal')
        self.create_button.config(state='disabled')

    def create_room_action(self):
        self.join_button.config(state='disable')
        self.room_id_label.config(state='disable')
        self.room_id_text.config(state='disable')
        self.room_password_label.config(state='disable')
        self.room_password_text.config(state='disable')
        self.create_button.config(state='normal')

Mode_Selection()