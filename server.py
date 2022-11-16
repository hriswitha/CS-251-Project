import socket
import threading
import sys

port = int(sys.argv[1])

server_socket = socket.socket()
server_socket.bind(('localhost', port))
server_socket.listen(100)

print("Waiting for connections...")


pass_dict = {}          #Dictionary for storing passwords
send_socket_dict = {}   #Dictionary of sending sockets
listen_socket_dict = {} #Dictionary of listening sockets


#The function for chatroom that happens in server
def chatroom(name, sending_socket):

    while True:
        operation = sending_socket.recv(1024).decode()
        #recieving username from client
        if (operation == "SEND"):
            sending_socket.send(str.encode("A Message to :"))
            username = sending_socket.recv(1024).decode()
            
            while not username in pass_dict.keys():
                #case when usename is not registered Asking to retype username
                sending_socket.send(str.encode("ERROR: USERNAME " + username + " NOT FOUND\nRETYPE USERNAME: "))
                username = sending_socket.recv(1024).decode()
            
            #Recieving message from client
            sending_socket.send(str.encode("TYPE MESSAGE: "))
            message = sending_socket.recv(1024).decode()

            #Sending message to client using listening socket dictionary
            listen_socket_dict[username].send(name.encode())
            listen_socket_dict[username].recv(1024).decode()
            listen_socket_dict[username].send(message.encode())
            print(listen_socket_dict[username].recv(1024).decode())
        elif (operation == "CREATE GROUP"):
            sending_socket.send(str.encode("Select Users:"))
            pass
        elif (operation == "ENTER GROUP"):
            pass


#Function for logging in
def LOGIN(sending_socket, listening_socket):
    #Logging in with username
    sending_socket.send(str.encode("USERNAME: "))
    username = sending_socket.recv(1024).decode()

    #case when username is not registered
    while not username in pass_dict.keys():
        sending_socket.send(str.encode("--- USERNAME NOT FOUND ---\nUSERNAME: "))
        username = sending_socket.recv(1024).decode()
    
    #Asking for password
    sending_socket.send(str.encode("PASSWORD: "))
    password = sending_socket.recv(1024).decode()

    #Case when incorrect password is typed
    while not (password == pass_dict[username]):
        sending_socket.send(str.encode("--- INCORRECT PASSWORD ---\nPASSWORD: "))
        password = sending_socket.recv(1024).decode()
    
    #Succesful login yayy
    sending_socket.send(str.encode("--- LOGIN SUCCESSFUL ---\nWELCOME TO THE CHAT ROOM"))
    
    #closing the previous connections of that user in case they are open
    if username in send_socket_dict.keys():
        send_socket_dict[username].close()
    if username in listen_socket_dict.keys():
        listen_socket_dict[username].close()
    
    #updating the socket dictionaries
    send_socket_dict[username] = sending_socket
    listen_socket_dict[username] = listening_socket

    #Going to chatroom as the logging in is complete
    chatroom(username, sending_socket)


def REGISTRATION(sending_socket, listening_socket):
    #Registartion for new user
    sending_socket.send(str.encode("USERNAME: "))
    username = sending_socket.recv(1024).decode()
    #Getting user name

    #Case when username is already registered
    while username in pass_dict.keys():
        sending_socket.send(str.encode("--- Username already exists! Try new one ---\nUSERNAME: "))
        username = sending_socket.recv(1024).decode()

    #Setting up password
    sending_socket.send(str.encode("PASSWORD: "))
    password = sending_socket.recv(1024).decode()
    #Updating password in password dictionary
    pass_dict[username] = password
    sending_socket.send(str.encode("REGISTRATION SUCCESFUL :)"))

    #Updating socket dictionaries
    send_socket_dict[username] = sending_socket
    listen_socket_dict[username] = listening_socket

    #Entering chatroom as registration is complete
    chatroom(username, sending_socket)


def AUTHENTICATION(sending_socket, listening_socket):
    #Authentication

    log = sending_socket.recv(1024).decode()
    #The operation they want to do, whether log in or register or quit

    if (log == 'log'):
        #Logging in
        LOGIN(sending_socket, listening_socket)

    elif (log == 'reg'):
        #Registering
        REGISTRATION(sending_socket, listening_socket)

    else:
        #quitting
        sending_socket.close()
        listening_socket.close()


while True:
    #Each True case for each run of client.py file

    sending_socket, addr1 = server_socket.accept()
    listening_socket, addr2 = server_socket.accept()
    #sending and listening socket

    #Threading for each user
    client_handler = threading.Thread(
        target=AUTHENTICATION,
        args = (sending_socket, listening_socket)
    )
    #Starting the thread
    client_handler.start()

server_socket.close()
