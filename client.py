import socket
import threading
import sys
import os
import hashlib

port = int(sys.argv[1])
#port number from command line arguments

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

messages = {}   #Dict for storing messages

#A function to listen messages 
def LISTEN(listening_socket):
    try:
        while True:
            #A message may be recieved at any moment so, keeping it in a while loop
            type = listening_socket.recv(1024).decode()
            listening_socket.send(str.encode("User"))

            from_user = listening_socket.recv(1024).decode()
            if type == "A text from contact":
                print('\nA New message from ' + from_user + ": ")
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
                listening_socket.send(str.encode("IMAGE RECIEVED"))


                pass
    except BrokenPipeError:
        pass

#client side of the chatroom
def chatroom(sending_socket, listening_socket):

    #A thread to keep on listening messages at any movement of time
    listen_messages = threading.Thread(
        target=LISTEN,
        args=(listening_socket,)
    )
    listen_messages.start()



    while True:
        
        operation = input("CHOOSE AN OPERATION\n")
        """
        1) 'SEND' - means we are sending a message to a user or group
        2) 'QUIT' - quit user
        3) 'GET CONTACTS' - get all the contacts this user has till now
        4) 'GET CHAT' - get chat of a particular chat or group
        """


        if (operation == "SEND TEXT"):
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
            
            #Getting message and sending to server
            message = input(reply)
            sending_socket.send(message.encode())

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

            #Getting image file name and sending data to server
            imgfilename= input(reply)
            imgfile = open(imgfilename,'rb')
            imgdata = imgfile.read(116640)
            sending_socket.send(imgdata)


        elif (operation == "CREATE GROUP"):
            sending_socket.send(operation.encode())
            reply = sending_socket.recv(1024).decode()
            while not (reply == "Type Group Name: "):
                username  = input(reply + ": ")
                sending_socket.send(username.encode())
                reply = sending_socket.recv(1024).decode()

            groupname = input(reply + ": ")
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
            elif (reply == "Type SEND to send message\nVIEW to view participants\n"):
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
                    
        elif (operation == "EXIT"):
            sending_socket.send(operation.encode())
            listen_messages.join()
            sending_socket.close()
            listening_socket.close()
            break

        elif (operation == "HELP"):
            pass

        elif (operation == "GET_CONTACTS"):
            pass

        else:
            print("Invalid operation\nuse 'HELP' for getting list all all commands")
        


while not (log == 'log' or log == 'reg' or log == 'quit'):
    #case when an invalid inpt is gicen
    print("--- INVALID INPUT ---")
    log = input("Select log for login, reg for regestration, quit for QUITTING: ")


if (log == 'log'):
    #Logging in to an existing user

    #updating server that it is a logging in process
    sending_socket.send(log.encode())
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
    password = input(reply)
    sending_socket.send(hashlib.md5(password.encode()).digest())
    reply = sending_socket.recv(1024).decode()

    #Case when typed password is incorrect
    while (reply == "--- INCORRECT PASSWORD ---\nPASSWORD: "):
        password = input(reply)
        sending_socket.send(hashlib.md5(password.encode()).digest())
        reply = sending_socket.recv(1024).decode()

    print(reply)

    name = username
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
    password = input(reply)
    sending_socket.send(hashlib.md5(password.encode()).digest())
    print(sending_socket.recv(1024).decode())

    name = username

    #Getting into the chatroon
    chatroom(sending_socket, listening_socket)

else:
    sending_socket.send(log.encode())
    sending_socket.close()
    listening_socket.close()

