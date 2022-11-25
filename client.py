# --------------------------CLIENT ------------------------------

import sys
import socket
import threading
import os
import getpass
import hashlib
from cryptography.fernet import Fernet
import base64, hashlib
import rsa
import base64

import logging



# Connecting to load balancer
load_port = socket.socket()
load_port.connect(('localhost', int(sys.argv[1])))


#Recieving server port after load balancing
port = int(load_port.recv(1024).decode(),10)
load_port.close()



listening_socket = socket.socket()
sending_socket = socket.socket()
sending_socket.connect(('localhost', port))
listening_socket.connect(('localhost', port))
#Creating and connectiong sockets to server socket

log = input("Select log for login, reg for regestration, quit for QUITTING: ")
#Choosing the opeartion
"""
1) 'log' - means logging into the existing user
2) 'reg' - means registering as a new user
3) 'quit' - means quitting/ending the program
"""

name = ""       #Username of this particular client
pwd = ""

priv = ""

messages = {}   #Dict for storing messages


def gen_fernet_key(passcode:bytes) -> bytes:
    """Generates fernet key
    Ggenerates a symmetric fernet key
    
        :param passcode: The passcode from which we are genarating key
        :type passcode:bytes
        :return: A fernet key
        :rtype: bytes
        """

    assert isinstance(passcode, bytes)
    hlib = hashlib.md5()
    hlib.update(passcode)
    return base64.urlsafe_b64encode(hlib.hexdigest().encode('latin-1'))

def encrypt_priv(n, passcode):
    """Encrypt private
    Encrypts n using fernet genarated by passcode
    
        :param n: integer we are encoding
        :type n: int
        :param passcode: passcode we are using
        :type passcode: string
        :return: An encrypted n
        :rtype: bytes
    """
    key = gen_fernet_key(passcode.encode('utf-8'))
    fernet = Fernet(key)
    return fernet.encrypt(bytes(hex(n).encode()))

def decrypt_priv(n, passcode):
    """Decrypts private
    Decrypts priv using fernet genarated by passcode
    
        :param n: encrypted int
        :type n: bytes
        :param passcode: passcode
        :type passcode: string
        :return: decrypted n
        :rtype: int
        """


    key = gen_fernet_key(passcode.encode('utf-8'))
    fernet = Fernet(key)
    return int(fernet.decrypt(n).decode('utf-8'), 16)

#A function to listen messages 
def LISTEN(listening_socket):
    """Listen function for socket type object
    Listens a text message or imagedata from both groups and clients and correspondingly prints the text or writes the image data into named files.
    Text messages get directly printed where a image from a particular client gets stored as clientname_count.jpg on local host
    Similarly image from client in a group gets stored as groupname_clientname_count.jpg

        :param listening_socket:Listening socket
        :type listening_socket:socket
        """
    try:
        while True:
            #A message may be recieved at any moment so, keeping it in a while loop
            type = listening_socket.recv(1024).decode()
            listening_socket.send(str.encode("User"))

            from_user = listening_socket.recv(1024).decode()
            if type == "A text from contact":
                print('\nA New message from ' + from_user + ": ")
                listening_socket.send(str.encode("Message"))
                message = rsa.decrypt(listening_socket.recv(1024), priv)
                # message = listening_socket.recv(1024).decode()
                print(message.decode())

                #Recieving message
                #Username of the sender as from_user
                #Adding this message to the messages dictionary
                if from_user in messages.keys():
                    messages[from_user].append(message)
                else:
                    messages[from_user] = [message]

                #Just a random thing to send of no use
                logging.debug(f'message {from_user} {name}')
                listening_socket.send(str.encode("MESSAGE RECIEVED"))
            #Recieving message
            if type == "An image from contact":
                x = 0
                while (os.path.isfile(f'{from_user}_{str(x)}.jpg')):
                    x += 1
                y = str(x)
                
                print('\nA New image from ' + from_user + ": ")
                listening_socket.send(str.encode("Image"))
                imgdata = listening_socket.recv(1166400)
                imgfile = open(f'{from_user}_{y}.jpg','wb')
                imgfile.write(imgdata)
                imgfile.close()
                print(f"Image stored as {from_user}_{y}.jpg")
                #Just a random thing to send of no use
                logging.debug(f'image {from_user} {name}')
                listening_socket.send(str.encode("IMAGE RECIEVED"))
                
            if type == "a message from group":
                listening_socket.send(str.encode("groupname"))
                groupname = listening_socket.recv(1024).decode()
                print('\nUser '+from_user+' posted a new message in '+groupname+': ')
                listening_socket.send(str.encode("Message"))
                message = listening_socket.recv(1024).decode()

                print("\n" + message)
                #Recieving message
                #Username of the sender as from_user
                #Adding this message to the messages dictionary
                if from_user in messages.keys():
                    messages[from_user].append(message)
                else:
                    messages[from_user] = [message]

                #Just a random thing to send of no use
                # logging.debug(f'message {from_user} {name}')
                listening_socket.send(str.encode("MESSAGE RECIEVED"))
            
            elif type == "An image from group":
                listening_socket.send(str.encode("Groupname"))
                groupname = listening_socket.recv(1024).decode()
                print('\nUser '+from_user+' sent an image in '+groupname+': ')
                listening_socket.send("Image".encode())
                imgdata = listening_socket.recv(1166400)

                x = 0
                while (os.path.isfile(f'{groupname}_{from_user}_{str(x)}.jpg')):
                    x += 1
                y = str(x)

                imgfile = open(f'{groupname}_{from_user}_{y}.jpg','wb')
                imgfile.write(imgdata)
                imgfile.close()
                print(f"Image stored as {groupname}_{from_user}_{y}.jpg")
                #Just a random thing to send of no use
                # logging.debug(f'image {from_user} {name}')
                listening_socket.send(str.encode("IMAGE RECIEVED"))


                pass
    except BrokenPipeError:
        pass

#client side of the chatroom
def chatroom(sending_socket, listening_socket):
    """Chatroom function for a client with valid operations - ('SEND TEXT' , 'SEND IMAGE' , 'CREATE GROUP' , 'GROUP' , 'EXIT' , 'HELP' , 'GET_CONTACTS' , 'GET_CHAT')


        :param name:Username of Client
        :type name:string
        :param sending_socket:Sending socket
        :type sending_socket:socket
        """

    #A thread to keep on listening messages at any movement of time
    listen_messages = threading.Thread(
        target=LISTEN,
        args=(listening_socket,)
    )
    listen_messages.start()
    
    print("""
        1) 'SEND TEXT' - means we are sending a text message to a user
        2) 'SEND IMAGE' - means we are sending a image to a user
        3) 'CREATE GROUP' - Creates a group with admin and users(if any)
        4) 'GROUP' - Enters int group and can choose operations like SEND , IMAGE , VIEW , ADD , REMOVE , DELETE
        5) 'EXIT' - Logout's the user (not force shut down)
        6) 'HELP' - Lists all valid operations
        7) 'REFRESH' - To get all the unread messages he got till now.
        """)

	


    while True:
        
        
        operation = input("CHOOSE AN OPERATION: ")
        if operation == "REFRESH":
            
            sending_socket.send(operation.encode())
            sending_socket.recv(1024)
            

        elif (operation == "SEND TEXT"):
            
            #Sending a message
            sending_socket.send(operation.encode())

            reply = sending_socket.recv(1024).decode()
            username = input(reply)
            sending_socket.send(username.encode())
            #Username to whom we are sending message

            reply = sending_socket.recv(1024).decode()
            #Case when username is not registered already
            while not (reply == "TYPE MESSAGE: "):
                #Asking to retry the username
                username = input(reply)
                sending_socket.send(username.encode())
                reply = sending_socket.recv(1024).decode()

            logging.debug(f'message {name} {username}')

            sending_socket.send("send n".encode())
            priv_n = int(sending_socket.recv(2048).decode(), 16)
            sending_socket.send("send e".encode())
            priv_e = int(sending_socket.recv(2048).decode(), 16)

            pub = rsa.PublicKey(priv_n, priv_e)
            
            #Getting message and sending to server
            message = input(reply)
            while (len(message) > 100):
                message = input("Only messages of size/length upto 100 are allowed\nRetype text: ")
            sending_socket.send(rsa.encrypt(message.encode(), pub))
            
            

        elif (operation == "SEND IMAGE"):
            #Sending a message
            sending_socket.send(operation.encode())

            reply = sending_socket.recv(1024).decode()
            username = input(reply)
            sending_socket.send(username.encode())
            #Username to whom we are sending message

            reply = sending_socket.recv(1024).decode()
            #Case when username is not registered already
            while not (reply == "Image file name: "):
                #Asking to retry the username
                username = input(reply)
                sending_socket.send(username.encode())
                reply = sending_socket.recv(1024).decode()
            
            logging.debug(f'image {name} {username}')

            #Getting image file name and sending data to server
            imgfilename= input(reply)
            imgfile = open(imgfilename,'rb')
            imgdata = imgfile.read(116640)
            sending_socket.send(imgdata)
            reply = sending_socket.recv(1024).decode()
            print(reply)
            

        elif (operation == "CREATE GROUP"):
            sending_socket.send(operation.encode())
            reply = sending_socket.recv(1024).decode()
            while not (reply == "Type Group Name: "):
                username  = input(reply)
                sending_socket.send(username.encode())
                reply = sending_socket.recv(1024).decode()

            groupname = input(reply)
            sending_socket.send(groupname.encode())
            reply = sending_socket.recv(1024).decode()
            while not (reply == "Group Succesfully created yay!"):
                groupname = input(reply)
                sending_socket.send(groupname.encode())
                reply = sending_socket.recv(1024).decode()
            print(reply)
            

        elif (operation == "GROUP"):
            sending_socket.send(operation.encode())
            reply = sending_socket.recv(1024).decode()
            groupname = input(reply)
            sending_socket.send(groupname.encode())
            reply = sending_socket.recv(1024).decode()
            
            
            if  (reply == "Groupname not found or you are not a member of the group\n"):
                print(reply)
            elif (reply == "Type SEND to send message\nIMAGE to send image\nVIEW to view participants\n"):
                op = input(reply)
                if (op == "SEND"):
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    message = input(reply)
                    sending_socket.send(message.encode())
                    reply = sending_socket.recv(1024).decode()
                    print(reply)
                    

                elif (op == "IMAGE"):
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    filename = input(reply)
                    file = open(filename, 'rb')
                    imgdata = file.read(1166400)
                    sending_socket.send(imgdata)
                    print(sending_socket.recv(1024).decode())
                    
                elif op == "VIEW":
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    i = 1
                    while not reply == "END":
                        if i == 1:
                            print(i, ". ", reply + " (Admin)")
                        else:
                            print(i, ". ", reply)
                        i = i + 1
                        sending_socket.send(str.encode(" "))
                        reply = sending_socket.recv(1024).decode()
                    
                else:
                    sending_socket.send("E".encode())
                    print(sending_socket.recv(1024).decode())
                    
            else:
                op = input(reply)
                if op == "ADD":
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    username = input(reply)
                    sending_socket.send(username.encode())
                    reply = sending_socket.recv(1024).decode()
                    while (reply == ("user with name " + username + " doesn't exist")):
                        username = input(reply)
                        sending_socket.send(username.encode())
                        reply = sending_socket.recv(1024).decode()
                    print(reply)
                    
                elif op == "REMOVE":
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    username = input(reply)
                    sending_socket.send(username.encode())
                    reply = sending_socket.recv(1024).decode()
                    print(reply)
                    

                elif (op == "SEND"):
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    message = input(reply)
                    sending_socket.send(message.encode())
                    reply = sending_socket.recv(1024).decode()
                    print(reply)
                    

                elif (op == "IMAGE"):
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    filename = input(reply)
                    file = open(filename, 'rb')
                    imgdata = file.read(1166400)
                    sending_socket.send(imgdata)
                    print(sending_socket.recv(1024).decode())
                    


                elif op == "DEL":
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    print(reply)
                    
                    
                elif op == "VIEW":
                    sending_socket.send(op.encode())
                    reply = sending_socket.recv(1024).decode()
                    i = 1
                    while not reply == "END":
                        if i == 1:
                            print(i, ". ", reply + " (Admin)")
                        else:
                            print(i, ". ", reply)
                        i = i + 1
                        sending_socket.send(str.encode(" "))
                        reply = sending_socket.recv(1024).decode()
                else:
                    sending_socket.send("E".encode())
                    print(sending_socket.recv(1024).decode())

        elif (operation == "EXIT"):
            sending_socket.send(operation.encode())
            listen_messages.join()
            sending_socket.close()
            listening_socket.close()
            
            break

        elif (operation == "HELP"):
            print("""
    1) 'SEND TEXT' - means we are sending a text message to a user
    2) 'SEND IMAGE' - means we are sending a image to a user
    3) 'CREATE GROUP' - Creates a group with admin and users(if any)
    4) 'GROUP' - Enters into group and can choose operations like SEND , IMAGE , VIEW , ADD , REMOVE , DELETE
    5) 'EXIT' - Logout's the user (not force shut down)
        """)
            

        else:
            print("Invalid operation\nuse 'HELP' for getting list all all commands")
            
        


while not (log == 'log' or log == 'reg' or log == 'quit'):
    #case when an invalid inpt is gicen
    print("--- INVALID INPUT ---")
    log = input("Select log for login, reg for regestration, quit for QUITTING: ")


if (log == 'log'):
    #Logging in to an existing user

    #updating server that it is a logging in process
    sending_socket.send('log'.encode())
    reply = sending_socket.recv(1024).decode()

    #getting username and sending to server
    username = input(reply)
    sending_socket.send(username.encode())
    reply = sending_socket.recv(1024).decode()

    #Case when username is not registered
    while not (reply == "PASSWORD: "):
        #Asking to re enter username
        username = input(reply)
        sending_socket.send(username.encode())
        reply = sending_socket.recv(1024).decode()
    
    #Sending password to server
    password = getpass.getpass(reply)
    sending_socket.send(hashlib.md5(password.encode()).digest())
    reply = sending_socket.recv(1024).decode()

    #Case when typed password is incorrect
    while (reply == "--- INCORRECT PASSWORD ---\nPASSWORD: "):
        password = getpass.getpass(reply)
        sending_socket.send(hashlib.md5(password.encode()).digest())
        reply = sending_socket.recv(1024).decode()

    print(reply)

    name = username
    pwd = password

    logging.basicConfig(filename=f"{name}.txt",level=logging.DEBUG,format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",filemode="a")


    sending_socket.send("send n".encode())
    priv_n = int(sending_socket.recv(2048).decode(), 16)
    sending_socket.send("send e".encode())
    priv_e = int(sending_socket.recv(2048).decode(), 16)
    sending_socket.send("send d".encode())
    priv_d = decrypt_priv(sending_socket.recv(2048), pwd)
    sending_socket.send("send p".encode())
    priv_p = decrypt_priv(sending_socket.recv(2048), pwd)
    sending_socket.send("send q".encode())
    priv_q = decrypt_priv(sending_socket.recv(2048), pwd)
    
    priv = rsa.PrivateKey(n = priv_n, e = priv_e, d = priv_d, p = priv_p, q = priv_q)

    #Succesfully logged in going to chatroom
    chatroom(sending_socket, listening_socket)
    



elif (log == 'reg'):
    #Registering a new user
    
    #updating server that it is a registration process
    sending_socket.send(log.encode())
    reply = sending_socket.recv(1024).decode()
    
    #Entering a new username
    username = input(reply)
    sending_socket.send(username.encode())
    reply = sending_socket.recv(1024).decode()

    #Case when the username is already present
    while not (reply == "PASSWORD: "):
        username = input(reply)
        sending_socket.send(username.encode())
        reply = sending_socket.recv(1024).decode()

    
    #Getting password
    password = getpass.getpass(reply)
    while len(password) < 4:
        password = getpass.getpass("---A weak password---\nPassword should atleast contain 8 characters\nRETYPE PASSWORD:")
    sending_socket.send(hashlib.md5(password.encode()).digest())


    
    print(sending_socket.recv(1024).decode())

    name = username
    pwd = password

    logging.basicConfig(filename=f"{name}.txt",level=logging.DEBUG,format="%(asctime)s [%(filename)s:%(lineno)d] %(message)s",filemode="a")


    (pub, priv) = rsa.newkeys(1024)

    sending_socket.send(hex(priv.n).encode())
    sending_socket.recv(1024)
    sending_socket.send(hex(priv.e).encode())
    sending_socket.recv(1024)
    sending_socket.send(encrypt_priv(priv.d, pwd))
    sending_socket.recv(1024)
    sending_socket.send(encrypt_priv(priv.p, pwd))
    sending_socket.recv(1024)    
    sending_socket.send(encrypt_priv(priv.q, pwd))
    sending_socket.recv(1024)


    #Getting into the chatroon
    chatroom(sending_socket, listening_socket)

else:
    sending_socket.send(log.encode())
    sending_socket.close()
    listening_socket.close()

