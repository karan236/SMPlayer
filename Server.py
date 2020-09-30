import socket
import pickle
import mysql.connector
from threading import *
import pickle
import random

class Server:
    def __init__(self):

        self.database=mysql.connector.connect(host='localhost',user='root',passwd='1234',database='social_media_player')
        self.cursor=self.database.cursor()
        self.admin_objects={}
        self.admin_file_length={}
        self.member_objects={}
        self.server=socket.socket()
        host=''
        port=9999
        self.server.bind((host,port))
        print('server is ready')
        self.server.listen(5)
        self.accept_connection()

    def accept_connection(self):
        while True:
            client,address=self.server.accept()
            login_create_account=Thread(target=self.login_create_new_account,args=(client,))
            login_create_account.start()

    def receive_object(self,client):
        full_msg = b''
        new_msg = True
        msglen=0
        while True:
            msg = client.recv(64)
            if new_msg:
                msglen = int(msg[:20])
                new_msg = False

            full_msg += msg

            if len(full_msg) - 20 == msglen:
                new_msg = True
                return pickle.loads(full_msg[20:])

    def receive_data(self,client):
        full_msg = b''
        new_msg = True
        msglen=0
        while True:
            msg = client.recv(64)
            if new_msg:
                msglen = int(msg[:20])
                new_msg = False

            full_msg += msg

            if len(full_msg) - 20 == msglen:
                new_msg = True
                return full_msg[20:].decode()


    def login_create_new_account(self,client):
        while(True):
            action=self.receive_data(client)
            if action=='new_account':
                data=self.receive_object(client)
                query = "select * from data where username=" + "\"" f"{data[2]}" + "\""
                self.cursor.execute(query)
                if len(list(self.cursor))==0:
                    client.send(bytes(f"{len('true'):<20}" + 'true', 'utf-8'))
                    query = "INSERT INTO DATA VALUES(" + "\"" f"{data[0]}" + "\"" + "," + "\"" f"{data[1]}" + "\"" + "," + "\"" f"{data[2]}" + "\"" + "," + "\"" f"{data[3]}" + "\"" + ")"
                    self.cursor.execute(query)
                    self.database.commit()
                    return
                else:
                    client.send(bytes(f"{len('false'):<20}" + 'false', 'utf-8'))

            else:
                data=self.receive_object(client)
                query = "select * from data where username=" + "\"" f"{data[0]}" + "\"" + " and " + "password=" + "\"" + f"{data[1]}" + "\""
                self.cursor.execute(query)
                if len(list(self.cursor))!=0:
                    client.send(bytes(f"{len('true'):<20}" + 'true', 'utf-8'))
                    mode_selection=Thread(target=self.mode_selection,args=(client, data[0],))
                    mode_selection.start()
                    return
                else:
                    client.send(bytes(f"{len('false'):<20}" + 'false', 'utf-8'))


    def mode_selection(self,client,user_id):
        while True:
            action=self.receive_data(client)

            if action=='create':
                roomid = "id" + user_id
                password=str(random.randint(100000,999999))
                message=pickle.dumps([roomid,password])
                message = bytes(f"{len(message):<20}", 'utf-8') + message
                client.send(message)
                #client.send(bytes(f"{len('hello'):<20}" + 'hello', 'utf-8'))
                query = "INSERT INTO ADMIN_DATA VALUES(" + "\"" f"{roomid}" + "\"" + "," + "\"" f"{password}" + "\"" + "," + "\"" f"{roomid[2:]}" + "\"" ")"
                self.cursor.execute(query)
                self.database.commit()
                self.admin_objects[roomid[2:]]=client
                admin_thread=Thread(target=self.admin_thread,args=(client,roomid[2:],))
                admin_thread.start()
                return
            else:
                data=self.receive_object(client)
                query = "select * from admin_data where room_id=" + "\"" f"{data[0]}" + "\"" + " and " + "room_password=" + "\"" + f"{data[1]}" + "\""
                self.cursor.execute(query)
                if len(list(self.cursor))!=0:
                    query = "select * from admin_data where room_id=" + "\"" f"{data[0]}" + "\"" + " and " + "room_password=" + "\"" + f"{data[1]}" + "\""
                    self.cursor.execute(query)
                    admin_id=list(self.cursor)[0][-1]
                    query = "INSERT INTO MEMBER_DATA VALUES(" + "\"" f"{admin_id}" + "\"" + "," + "\"" f"{data[0]}" + "\"" + "," + "\"" f"{data[1]}" + "\"" + "," + "\"" f"{user_id}" + "\"" ")"
                    self.cursor.execute(query)
                    self.database.commit()
                    client.send(bytes(f"{len('true'):<20}" + 'true', 'utf-8'))
                    message = pickle.dumps(self.admin_file_length[admin_id])
                    message = bytes(f"{len(message):<20}", 'utf-8') + message
                    client.send(message)
                    self.member_objects[user_id]=client
                    if self.receive_data(client)=='sync':
                        self.admin_objects[admin_id].send(bytes(f"{len('sync'):<20}" + 'sync', 'utf-8'))
                        if self.receive_data(client)=='stop':
                            query = "DELETE FROM MEMBER_DATA WHERE member_id=" + "\"" f"{user_id}" + "\""
                            self.cursor.execute(query)
                            self.database.commit()
                            print("deleted")
                    return
                else:
                    client.send(bytes(f"{len('false'):<20}" + 'false', 'utf-8'))


    def admin_thread(self,client,admin_id):
        while(True):
            try:
                action=self.receive_data(client)
            except:
                return

            print(action)

            if action=='new file':
                file_name,file_length=self.receive_object(client)
                self.admin_file_length[admin_id]=[file_name, file_length]

            elif action=='play':
                time = self.receive_data(client)
                time = str(time)
                query = "select * from member_data where admin_id=" + "\"" f"{admin_id}" + "\""
                self.cursor.execute(query)
                for i in list(self.cursor):
                    self.member_objects[i[-1]].send(
                        bytes(f"{len('play'):<20}" + 'play', 'utf-8'))
                    print("slider sent")
                    self.member_objects[i[-1]].send(bytes(f"{len(time):<20}" + time, 'utf-8'))
                    print("time sent")

            elif action=='pause':
                query = "select * from member_data where admin_id=" + "\"" f"{admin_id}" + "\""
                self.cursor.execute(query)
                for i in list(self.cursor):
                    self.member_objects[i[-1]].send(bytes(f"{len('pause'):<20}" + 'pause', 'utf-8'))

            elif action=='empty':
                query = "select * from member_data where admin_id=" + "\"" f"{admin_id}" + "\""
                self.cursor.execute(query)
                for i in list(self.cursor):
                    self.member_objects[i[-1]].send(bytes(f"{len('empty'):<20}" + 'empty', 'utf-8'))

            elif action=='stop':
                query = "select * from member_data where admin_id=" + "\"" f"{admin_id}" + "\""
                self.cursor.execute(query)
                for i in list(self.cursor):
                    self.member_objects[i[-1]].send(bytes(f"{len('stop'):<20}" + 'stop', 'utf-8'))

    def member_thread(self,client,member_id):
        pass


s=Server()