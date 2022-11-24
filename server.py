# -------------------------- SERVER------------------------------

import socket
import threading
import sys
import psycopg2

port = int(sys.argv[1])


server_socket = socket.socket()
server_socket.bind(('localhost', port))
server_socket.listen(100)

print("Waiting for connections...")

def convertTuple(tup):
    """Convert-Tuple function
    Converts items in a tuple into string 

        :param tup:Tuple
        :type tup:tuple
        :return: String generated from items of the input tuple
        :rtype:string
        """
    
    str = ''
    for item in tup:
        str = str + item
    return str

def searchtable(obj,col,table,db):
    """Search-Table function
    Connects to the database in input and searches for a object in specific column of a table of that database

        :param obj:Generally Username of Client
        :type obj:string
        :param col:Column name
        :type col:string
        :param table:Table name
        :type table:string
        :param db:DataBase name
        :type db:string
        :return: Boolean value if the object is found in the table of database or not
        :rtype:bool
        """

    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("SELECT " + col + " FROM " + table)
    data = cur.fetchall()
    for d in data:
        if obj == convertTuple(d):
            conn.commit()
            conn.close()
            return True
    if conn:
        conn.commit()
        conn.close()
    return False

def valuebykey(key,colno,table,db):
    """Value-By-Key function
    Connects to the database in input and returns the element in given column number of the row where the primary key is present table of that database

        :param key:Generally Username of Client
        :type key:string
        :param colno:Column number
        :type colno:integer
        :param table:Table name
        :type table:string
        :param db:DataBase name
        :type db:string
        :return: value of corresponding column number
        :rtype:optional
        """
    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM " + table)
    rows = cur.fetchall()
    for row in rows:
        if key == row[0]:
            return row[colno-1]
    if conn:
        conn.commit()
        conn.close()
    return 

def insert(un,pwd,stat,conn_port,table,db):
    """Insert function
    Connects to the database and inserts the given parameters into that specific table

        :param un:Username of Client
        :type un:string
        :param pwd:Password
        :type pwd:bytea
        :param stat:Online/Offline status of client
        :type stat:string
        :param table:Table name
        :type table:string
        :param db:DataBase name
        :type db:string
        :return: Insertion into table
        :rtype:optional
        """
    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO "+ table +"(UN,PWD,status,connected_port) VALUES(%s,%s,%s,%s)",(un , pwd ,stat,conn_port))
    conn.commit()
    conn.close()

def insert_group(gn,ul,table,db):
    """Insert function
    Connects to the database and inserts the given parameters into that specific table

        :param un:Username of Client
        :type un:string
        :param pwd:Password
        :type pwd:bytea
        :param stat:Online/Offline status of client
        :type stat:string
        :param table:Table name
        :type table:string
        :param db:DataBase name
        :type db:string
        :return: Insertion into table
        :rtype:optional
        """
    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO "+ table +"(GROUPNAME,user_list) VALUES(%s,%s)",(gn,ul))
    conn.commit()
    conn.close()

def insert_port(pno,cul,stat,bal,table,db):
    """Insert function
    Connects to the database and inserts the given parameters into that specific table

        :param un:Username of Client
        :type un:string
        :param pwd:Password
        :type pwd:bytea
        :param stat:Online/Offline status of client
        :type stat:string
        :param table:Table name
        :type table:string
        :param db:DataBase name
        :type db:string
        :return: Insertion into table
        :rtype:optional
        """
    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO "+ table +"(port_no,conn_user_list,server_status,balance) VALUES(%s,%s,%s,%s)",(pno,cul,stat,bal))
    conn.commit()
    conn.close()


def update(unkey,obj,colname,table,db):
    """Insert function
    Connects to the database and inserts the given parameters into that specific table

        :param un:Username of Client
        :type un:string
        :param pwd:Password
        :type pwd:bytea
        :param stat:Online/Offline status of client
        :type stat:string
        :param table:Table name
        :type table:string
        :param db:DataBase name
        :type db:string
        :return: Insertion into table
        :rtype:optional
        """

    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("UPDATE "+ table +" SET "+colname+" = '"+obj+"' WHERE un = '"+unkey+"';")
    conn.commit()
    conn.close()

def update_port(portkey,obj,colname,table,db):
    
    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute(f"UPDATE {table} SET {colname} = {obj} WHERE port_no = '{portkey}'")
    conn.commit()
    conn.close()

def delrow(gn,table,db):
    """Insert function
    Connects to the database and inserts the given parameters into that specific table

        :param un:Username of Client
        :type un:string
        :param pwd:Password
        :type pwd:bytea
        :param stat:Online/Offline status of client
        :type stat:string
        :param table:Table name
        :type table:string
        :param db:DataBase name
        :type db:string
        :return: Insertion into table
        :rtype:optional
        """

    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("DELETE FROM TABLE "+ table +" WHERE GROUPNAME = "+gn+";")
    conn.commit()
    conn.close()


# pass_dict = {}          #Dictionary for storing passwords
send_socket_dict = {}   #Dictionary of sending sockets
listen_socket_dict = {} #Dictionary of listening sockets
# groups = {}             #Dictionaries of groups, key is groupname, value is list of users, first element of list is admin


#The function for chatroom that happens in server
def chatroom(name, sending_socket):
    """Chatroom function for a client with valid operations - ('SEND TEXT' , 'SEND IMAGE' , 'CREATE GROUP' , 'GROUP' , 'EXIT' , 'HELP' , 'GET_CONTACTS' , 'GET_CHAT')

        :param name:Username of Client
        :type name:string
        :param sending_socket:Sending socket
        :type sending_socket:socket
        """

    try:
        while True:
            operation = sending_socket.recv(1024).decode()
            #recieving username from client
            if (operation == "SEND TEXT"):
                sending_socket.send(str.encode("Send text to :"))
                username = sending_socket.recv(1024).decode()
                
                while not searchtable(username,"UN","PASS_DICT","testdb"):
                    #case when usename is not registered Asking to retype username
                    sending_socket.send(str.encode("ERROR: USERNAME " + username + " NOT FOUND\nRETYPE USERNAME: "))
                    username = sending_socket.recv(1024).decode()
                
                #Recieving message from client
                sending_socket.send(str.encode("TYPE MESSAGE: "))
                message = sending_socket.recv(1024).decode()

                #Sending message to client using listening socket dictionary
                listen_socket_dict[username].send(str.encode("A text from contact"))
                listen_socket_dict[username].recv(1024).decode()
                listen_socket_dict[username].send(name.encode())
                listen_socket_dict[username].recv(1024).decode()
                listen_socket_dict[username].send(message.encode())
                print(listen_socket_dict[username].recv(1024).decode())
            
            elif (operation == "SEND IMAGE"):
                sending_socket.send(str.encode("Send image to :"))
                username = sending_socket.recv(1024).decode()
                while not searchtable(username,"UN","PASS_DICT","testdb"):
                    #case when usename is not registered Asking to retype username
                    sending_socket.send(str.encode("ERROR: USERNAME " + username + " NOT FOUND\nRETYPE USERNAME: "))
                    username = sending_socket.recv(1024).decode()
                
                #Recieving imagedata from client
                sending_socket.send(str.encode("Image file name: "))
                imgdata = sending_socket.recv(1166400)
                # imgfile = open(imgfilename,'rb')
                # imgdata = imgfile.read(1024)
                # imgfile.close()

                #Sending imagedata to client using listening socket dictionary
                listen_socket_dict[username].send(str.encode("An image from contact"))
                listen_socket_dict[username].recv(1024).decode()
                listen_socket_dict[username].send(name.encode())
                listen_socket_dict[username].recv(1024).decode()
                listen_socket_dict[username].send(imgdata)
                print(listen_socket_dict[username].recv(1024).decode())
                
            elif (operation == "CREATE GROUP"):
                sending_socket.send(str.encode("Select Users"))
                username = sending_socket.recv(1024).decode()
                usernames = [name]
                while not username == "END":
                    while (not searchtable(username,"UN","PASS_DICT","testdb")) or (username in usernames):
                        sending_socket.send(str.encode("The name " + username + " Doesn't exist or already been added\nTry some other name\nSelect Users"))
                        username = sending_socket.recv(1024).decode()
                        if username == "END":
                            break
                    if not username == "END":
                        usernames.append(username)
                        sending_socket.send(str.encode("Select Users:"))
                        username = sending_socket.recv(1024).decode()

                sending_socket.send(str.encode("Type Group Name: "))
                groupname = sending_socket.recv(1024).decode()
                while searchtable(groupname,"UN","PASS_DICT","testdb") or searchtable(groupname,"GROUPNAME","GROUPS","testdb"):
                    sending_socket.send(str.encode("The name " + groupname + " already exists as an existing user or as another group name\nPlease Try another name\nType Group Name: "))
                    groupname = sending_socket.recv(1024).decode()
                
                # groups[groupname] = usernames
                insert_group(groupname,usernames,"GROUPS","testdb")

                sending_socket.send(str.encode("Group Succesfully created yay!"))
                # print(groups)

            elif (operation == "GROUP"):
                sending_socket.send(str.encode("Enter Group Name: "))
                groupname = sending_socket.recv(1024).decode()
                if not searchtable(groupname,"GROUPNAME","GROUPS","testdb"):
                    sending_socket.send(str.encode("Groupname not found or you are not a member of the group\n"))
                elif (not name in valuebykey(groupname,2,"GROUPS","testdb")):
                    sending_socket.send(str.encode("Groupname not found or you are not a member of the group\n")) 
                else:
                    if not valuebykey(groupname,2,"GROUPS","testdb")[0] == name:
                        sending_socket.send(str.encode("Type SEND to send message\nVIEW to view participants\n"))
                        op = sending_socket.recv(1024).decode()
                        if op == "SEND":
                            sending_socket.send(str.encode("TYPE MESSAGE: "))
                            message = sending_socket.recv(1024).decode()
                            for user in valuebykey(groupname,2,"GROUPS","testdb"):
                                if not user == name:
                                    listen_socket_dict[user].send(str.encode("a message from group"))
                                    print(listen_socket_dict[user].recv(1024).decode())
                                    listen_socket_dict[user].send(name.encode())
                                    print(listen_socket_dict[user].recv(1024).decode())
                                    listen_socket_dict[user].send(groupname.encode())
                                    print(listen_socket_dict[user].recv(1024).decode())
                                    listen_socket_dict[user].send(message.encode())
                                    print(listen_socket_dict[user].recv(1024).decode())
                            sending_socket.send(str.encode("Succesfully sent your message to everyone in the group!\n"))

                        elif op == "VIEW":
                            for username in valuebykey(groupname,2,"GROUPS","testdb"):
                                sending_socket.send(username.encode())
                                sending_socket.recv(1024).decode()
                            sending_socket.send(str.encode("END"))
                        else:
                            pass
                    else:
                        sending_socket.send(str.encode("Type SEND to send message\nType ADD to add participants\nREMOVE to remove participants\nVIEW to view participants\nDEL to delete group"))
                        op = sending_socket.recv(1024).decode()
                        if op == "SEND":
                            sending_socket.send(str.encode("TYPE MESSAGE: "))
                            message = sending_socket.recv(1024).decode()
                            for user in valuebykey(groupname,2,"GROUPS","testdb"):
                                if not user == name:
                                    listen_socket_dict[user].send(str.encode("a message from group"))
                                    print(listen_socket_dict[user].recv(1024).decode())
                                    listen_socket_dict[user].send(name.encode())
                                    print(listen_socket_dict[user].recv(1024).decode())
                                    listen_socket_dict[user].send(groupname.encode())
                                    print(listen_socket_dict[user].recv(1024).decode())
                                    listen_socket_dict[user].send(message.encode())
                                    print(listen_socket_dict[user].recv(1024).decode())
                            sending_socket.send(str.encode("Succesfully sent your message to everyone in the group!\n"))
                            
                        elif (op == "IMAGE"):
                            sending_socket.send(str.encode("Type image file name: "))
                            imgdata = sending_socket.recv(116640)
                            for user in valuebykey(groupname,2,"GROUPS","testdb"):
                                if not user == name:
                                    temp_sock = listen_socket_dict[user]
                                    temp_sock.send("An image from group".encode())
                                    temp_sock.recv(1024).decode()
                                    temp_sock.send(name.encode())
                                    temp_sock.recv(1024).decode()
                                    temp_sock.send(groupname.encode())
                                    temp_sock.recv(1024).decode()
                                    temp_sock.send(imgdata)
                                    print(temp_sock.recv(1024).decode())

                            sending_socket.send("Successfully sent your image to everyone in the group!\n".encode())

                        elif op == "VIEW":
                            for username in valuebykey(groupname,2,"GROUPS","testdb"):
                                sending_socket.send(username.encode())
                                sending_socket.recv(1024).decode()
                            sending_socket.send(str.encode("END"))


                        elif op == "ADD":
                            sending_socket.send(str.encode("Select User: "))
                            username = sending_socket.recv(1024).decode()
                            while (not searchtable(username,"UN","PASS_DICT","testdb")) and (not username == "END"):
                                sending_socket.send(str.encode("user with name " + username + " doesn't exist"))
                                username = sending_socket.recv(1024).decode()

                            if username == "END":
                                sending_socket.send(str.encode("Adding process aborted"))
                            elif username in valuebykey(groupname,2,"GROUPS","testdb"):
                                sending_socket.send(str.encode("User " + username + " already in the group"))
                            else:
                                valuebykey(groupname,2,"GROUPS","testdb").append(username)
                                sending_socket.send(str.encode("User " + username + " successfully added to group " + groupname))

                        elif op == "REMOVE":
                            sending_socket.send(str.encode("Select user: "))
                            username = sending_socket.recv(1024).decode()
                            if username == name:
                                sending_socket.send(str.encode("You can't be removed from the group as you are admin, select DEL to delete the group"))
                            elif username == "END":
                                sending_socket.send(str.encode("--- Process Aborted ---"))
                            elif username not in valuebykey(groupname,2,"GROUPS","testdb"):
                                sending_socket.send(str.encode("The user " + username + " is not in this group"))
                            else:
                                valuebykey(groupname,2,"GROUPS","testdb").remove(username)
                                sending_socket.send(str.encode("User " + username + " successfully removed from this group"))
                            
                        elif op == "DEL":
                            # groups.pop(groupname)
                            delrow(groupname,"GROUPS","testdb")
                            sending_socket.send(str.encode("Group " + groupname + " succesfully deleted"))

            elif (operation == "EXIT"):
                sending_socket.close()
                listen_socket_dict[name].close()
                update(name,"offline","status","PASS_DICT","testdb")
                update(name,'0',"connected_port","PASS_DICT","testdb")
                b = valuebykey(port,4,"server_conn_list","testdb")
                update_port(port,b-1,"balance","server_conn_list","testdb")
                if name in valuebykey(port,2,"server_conn_list","testdb"):
                    l = valuebykey(port,2,"server_conn_list","testdb").remove(name)
                    
                    le = len(str(l))
                    lraw = str(l)[1:le-1].replace("'","")
                    n = name.replace("'","")
                    lraw = lraw.replace(","+n+",","")
                    lraw = "'{"+lraw+"}'"
                    
                    update_port(port,lraw,"conn_user_list","server_conn_list","testdb")

                pass
            elif (operation == ""):
                update(name,"offline","status","PASS_DICT","testdb")
                update(name,'0',"connected_port","PASS_DICT","testdb")
                b = valuebykey(port,4,"server_conn_list","testdb")
                update_port(port,b-1,"balance","server_conn_list","testdb")
                if name in valuebykey(port,2,"server_conn_list","testdb"):
                    l = valuebykey(port,2,"server_conn_list","testdb")
                    le = len(str(l))
                    lraw = str(l)[1:le-1].replace(","+name+",","")
                    lraw = lraw.replace("'","")
                    lraw = "'{"+lraw+"}'"
                    update_port(port,lraw,"conn_user_list","server_conn_list","testdb")
                print(f"User {name} got disconnected")
                break
    except OSError:
        update(name,"offline","status","PASS_DICT","testdb")
        print(f"User {name} got disconnected")



#Function for logging in
def LOGIN(sending_socket, listening_socket):
    """Login function for existing clients

        :param listening_socket:Listening socket
        :type listening_socket:socket
        :param sending_socket:Sending socket
        :type sending_socket:socket
        """
    #Logging in with username
    sending_socket.send(str.encode("USERNAME: "))
    username = sending_socket.recv(1024).decode()

    #case when username is not registered
    while not searchtable(username,"UN","PASS_DICT","testdb"):
        sending_socket.send(str.encode("--- USERNAME NOT FOUND ---\nUSERNAME: "))
        username = sending_socket.recv(1024).decode()
    
    #Asking for password
    sending_socket.send(str.encode("PASSWORD: "))
    password = sending_socket.recv(1024)

    #Case when incorrect password is typed
    while not (password == bytes(valuebykey(username,2,"PASS_DICT","testdb"))):
        sending_socket.send(str.encode("--- INCORRECT PASSWORD ---\nPASSWORD: "))
        password = sending_socket.recv(1024)
    
    #Succesful login yayy
    sending_socket.send(str.encode("--- LOGIN SUCCESSFUL ---\nWELCOME TO THE CHAT ROOM"))
    update(username,"online","status","PASS_DICT","testdb")
    update(username,f'{port}',"connected_port","PASS_DICT","testdb")
    b = valuebykey(port,4,"server_conn_list","testdb")
    update_port(port,b+1,"balance","server_conn_list","testdb")
    if username not in valuebykey(port,2,"server_conn_list","testdb"):
        l = valuebykey(port,2,"server_conn_list","testdb") + [username]
        le = len(str(l))
        lraw = str(l)[1:le-1].replace("'","")
        lraw = "'{"+lraw+"}'"
        update_port(port,lraw,"conn_user_list","server_conn_list","testdb")

    
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
    """Registration function for new clients

        :param listening_socket:Listening socket
        :type listening_socket:socket
        :param sending_socket:Sending socket
        :type sending_socket:socket
        """
    #Registartion for new user
    sending_socket.send(str.encode("USERNAME: "))
    username = sending_socket.recv(1024).decode()
    #Getting user name

    #Case when username is already registered
    while searchtable(username,"UN","PASS_DICT","testdb"):
        sending_socket.send(str.encode("--- Username already exists! Try new one ---\nUSERNAME: "))
        username = sending_socket.recv(1024).decode()

    #Setting up password
    sending_socket.send(str.encode("PASSWORD: "))
    password = sending_socket.recv(1024)
    #Updating password in password dictionary
    # pass_dict[username] = password
    insert(username,password,"online",port,"PASS_DICT","testdb")
    sending_socket.send(str.encode("REGISTRATION SUCCESFUL :)"))
    b = valuebykey(port,4,"server_conn_list","testdb")
    update_port(port,b+1,"balance","server_conn_list","testdb")
    if username not in valuebykey(port,2,"server_conn_list","testdb"):
        l = valuebykey(port,2,"server_conn_list","testdb") + [username]
        le = len(str(l))
        lraw = str(l)[1:le-1].replace("'","")
        lraw = "'{"+lraw+"}'"
        update_port(port,lraw,"conn_user_list","server_conn_list","testdb")


    #Updating socket dictionaries
    send_socket_dict[username] = sending_socket
    listen_socket_dict[username] = listening_socket

    #Entering chatroom as registration is complete
    chatroom(username, sending_socket)

def AUTHENTICATION(sending_socket, listening_socket):
    """Authentication function for users with operations ('log','reg','quit')

        :param listening_socket:Listening socket
        :type listening_socket:socket
        :param sending_socket:Sending socket
        :type sending_socket:socket
        """
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


insert_port(port,[],"online",0,"server_conn_list","testdb")
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

