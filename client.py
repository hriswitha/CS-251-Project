import socket
import threading
import sys

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

name = ""       #Username of this purticular client

messages = {}   #Dict for storing messages

#A function to listen messages 
def LISTEN(listening_socket):

    while True:
        #A message may be recieved at any moment so, keeping it in a while loop

        from_user = listening_socket.recv(1024).decode()
        print('\nA New message from ' + from_user + ": ")
        #Username of the sender as from_user

        listening_socket.send(str.encode("Message"))
        message = listening_socket.recv(1024).decode()
        print("\n" + message)
        #Recieving message

        #Adding this message to the messages dictionary
        if from_user in messages.keys():
            messages[from_user].append(message)
        else:
            messages[from_user] = [message]

        #Just a random thing to send of no use
        listening_socket.send(str.encode("MESSAGE RECIEVED"))

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
        4) 'GET CHAT' - get chat of a purticular chat or group
        """

        if (operation == "SEND"):
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

        elif (operation == "CREATE GROUP"):
            pass

        elif (operation == "ENTER GROUP"):
            sending_socket.send(operation.encode())
            pass

        elif (operation == "GET_CHAT"):
            pass


        elif (operation == "EXIT"):
            pass

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
    sending_socket.send(password.encode())
    reply = sending_socket.recv(1024).decode()

    #Case when typed password is incorrect
    while (reply == "--- INCORRECT PASSWORD ---\nPASSWORD: "):
        password = input(reply)
        sending_socket.send(password.encode())
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
    sending_socket.send(password.encode())
    print(sending_socket.recv(1024).decode())

    name = username

    #Getting into the chatroon
    chatroom(sending_socket, listening_socket)

else:
    sending_socket.send(log.encode())
    sending_socket.close()
    listening_socket.close()
