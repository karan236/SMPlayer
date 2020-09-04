from tkinter import *
import Admin
import Member
import StartingPage
import pickle
from tkinter import messagebox
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

        self.join_button=Button(self.mode_selection_window,text='Join',state="disabled",command=self.join_room_button_action)
        self.join_button.pack(pady=5)

        self.create_button=Button(self.mode_selection_window,text='Create',state="disabled",command=self.create_room_button_action)
        self.create_button.pack()

        self.mode_selection_window.mainloop()

    def receive_object(self,server):
        full_msg = b''
        new_msg = True
        msglen=0
        while True:
            print("before recieve")
            msg = server.recv(64)
            print()
            if new_msg:
                msglen = int(msg[:20])
                new_msg = False

            full_msg += msg

            if len(full_msg) - 20 == msglen:
                new_msg = True
                print('here')
                return pickle.loads(full_msg[20:])

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

    def create_room_button_action(self):
        self.mode_selection_window.destroy()
        StartingPage.server.send(bytes(f"{len('create'):<20}" + 'create', 'utf-8'))
        print("Create Sent to server")
        Admin.admin_window()

    def join_room_button_action(self):
        print("here")
        if self.room_id_text.get()=="" or self.room_password_text.get()=="":
            messagebox.showerror("Incomplete Data","Please provide room id and password.")

        else:
            data = []
            data.append(self.room_id_text.get())
            data.append(self.room_password_text.get())
            message = pickle.dumps(data)
            StartingPage.server.send(bytes(f"{len('join'):<20}" + 'join', 'utf-8'))
            message = bytes(f"{len(message):<20}", 'utf-8') + message
            StartingPage.server.send(message)
            if self.receive_data(StartingPage.server)=="true":
                self.mode_selection_window.destroy()
                Member.member_window()
            else:
                messagebox.showerror("Invaid Data!","Invalid Room ID or Password.")