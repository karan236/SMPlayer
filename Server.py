import socket
import pickle
import mysql.connector
from threading import *

class Server:
    def __init__(self):

        self.database=mysql.connector.connect(host='localhost',user='root',passwd='84406232',database='social_media_player')
        self.cursor=self.database.cursor()

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
                query = "INSERT INTO DATA VALUES(" + "\"" f"{data[0]}" + "\"" + "," + "\"" f"{data[1]}" + "\"" + "," + "\"" f"{data[2]}" + "\"" + "," + "\"" f"{data[3]}" + "\"" + ")"
                self.cursor.execute(query)
                self.database.commit()
                return
            else:
                data=self.receive_object(client)
                query = "select * from data where username=" + "\"" f"{data[0]}" + "\"" + " and " + "password=" + "\"" + f"{data[1]}" + "\""
                self.cursor.execute(query)
                if len(list(self.cursor))!=0:
                    client.send(bytes(f"{len('true'):<20}" + 'true', 'utf-8'))
                    print('success')
                    return
                else:
                    client.send(bytes(f"{len('false'):<20}" + 'false', 'utf-8'))

s=Server()