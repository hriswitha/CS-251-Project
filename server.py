# -------------------------- SERVER------------------------------

import socket
import threading
import sys
import psycopg2


port = int(sys.argv[1])

server_socket = socket.socket()
server_socket.bind(('localhost', port))
server_socket.listen(100)

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


insert_port(port,[],"online",0,"server_conn_list","testdb")

print("Waiting for connections...")

def push_message(groupname, sender, reciever, message):
    """Push function
    Connects to database and pushes the message into the m table

        :param groupname: Groupname or none
        :param groupname: string
        :param sender: Sender name
        :param sender: string
        :param reciever: reciever name
        :param recieer: string
        :param message: bytes
        
    """
    conn = psycopg2.connect(user = 'postgres', password='1234', host = 'localhost', port='5432', database = 'testdb')
    cur = conn.cursor()
    if groupname == "":
        cur.execute("INSERT INTO M (GROUPNAME, FROM_USER, TO_USER, MESSAGE) VALUES(%s, %s, %s, %s)",('NULL',sender, reciever, message))
    else:
        cur.execute("INSERT INTO M (GROUPNAME, FROM_USER, TO_USER, MESSAGE) VALUES(%s, %s, %s, %s)",(groupname,sender, reciever, message))
    
    conn.commit()
    conn.close()

def push_image(groupname, sender, reciever, image):
    """Push function
    Connects to database and pushes the message into the m table

        :param groupname: Groupname or none
        :param groupname: string
        :param sender: Sender name
        :param sender: string
        :param reciever: reciever name
        :param recieer: string
        :param image: bytes
        
    """

    conn = psycopg2.connect(user = 'postgres', password='1234', host = 'localhost', port='5432', database = 'testdb')
    cur = conn.cursor()
    bimage = psycopg2.Binary(image)
    if groupname == "":
        cur.execute("INSERT INTO I (GROUPNAME, FROM_USER, TO_USER, IMAGE) VALUES(%s, %s, %s, %s)",('NULL',sender, reciever, bimage))
    else:
        cur.execute("INSERT INTO I (GROUPNAME, FROM_USER, TO_USER, IMAGE) VALUES(%s, %s, %s, %s)",(groupname,sender, reciever, bimage))
    
    conn.commit()
    conn.close()

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

def insert(un,pwd,stat,conn_port,table,db, n, e, d, p, q):
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
        :param n: N needed to construct priv key
        :type n: bytes
        :param e: E needed to construct priv key
        :type e: bytes
        :param d: D needed to construct priv key
        :type d: bytes
        :param p: P needed to construct priv key
        :type p: bytes
        :param q: Q needed to construct priv key
        :type q: bytes
        :return: Insertion into table
        :rtype:optional
        """
    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO "+ table +"(UN,PWD,status,connected_port, priv_n, priv_e, priv_d, priv_p, priv_q) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(un , pwd ,stat,conn_port, n, e, d, p, q))
    conn.commit()
    conn.close()

def insert_group(gn,ul,table,db):
    """Insert function
    Connects to the database and inserts the given parameters into that specific table

        :param gn: groupname we need to insert
        :type gn: string
        :param ul: users list we are inserting
        :type ul: list
        :param table: table name
        :type table: string
        :param db: database name
        :type db: string
        """
    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("INSERT INTO "+ table +"(GROUPNAME,user_list) VALUES(%s,%s)",(gn,ul))
    conn.commit()
    conn.close()

def update(unkey,obj,colname,table,db):
    """Update table 
    connects to database and updates table of specific column

        :param unkey: username 
        :type unkey: string
        :param obj: object we need to update
        :type obj: optional
        :param colname: column name we need to update
        :type colname: string
        :param table: table name
        :type table: string
        :param db: database name
        :type db: string
        """

    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("UPDATE "+ table +" SET "+colname+" = '"+obj+"' WHERE un = '"+unkey+"';")
    conn.commit()
    conn.close()

def update_group(gnkey,obj,colname,table,db):
    """Update group table
    connects to database and updates groups table into specific column

        :param gnkey: Groupname
        :param gnkey: string
        :param obj: obj we need to update
        :type obj: optional
        :param colname: column we need to update
        :type colname: string
        :param table: table name
        :type table: string
        :param db: database name
        :type db: string

    """


    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute(f"UPDATE {table} SET {colname} = ARRAY{obj} WHERE groupname = '{gnkey}';")
    conn.commit()
    conn.close()

def update_port(portkey,obj,colname,table,db):
    """Updates port
    connects to database and updates port of specific portkey

        :param portkey: port number
        :type portkey: int
        :param obj: object we are changing
        :type obj: optional
        :param colname: column name
        :type colname: string
        :param table: table name
        :type table: string
        :param db: database name
        :type db: string
    """


    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    if type(obj) == list:
        if obj == []:
            cur.execute("UPDATE " + table + " SET " + colname + " = %s WHERE port_no = %s;", (obj, portkey))
        else:
            cur.execute(f"UPDATE {table} SET {colname} = ARRAY{obj} WHERE port_no = '{portkey}';")
    else:
        cur.execute(f"UPDATE {table} SET {colname} = {obj} WHERE port_no = '{portkey}';")
    conn.commit()
    conn.close()

def delrow(gn,table,db):
    """delete group
    connects to database and delete group

        :param gn: groupname
        :type gn: string
        :param table: table name
        :type table: string
        :param db: database name
        :type db: string
        """

    conn = psycopg2.connect(database = db, user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("DELETE FROM "+ table +" WHERE GROUPNAME = '" + gn + "';")
    conn.commit()
    conn.close()

def offline_messages(name):
    """Offline messages recieving
    Connects to database and recieves all the messages it got till now
    
    :param name: Username or name of the client
    :type name: string
    :return: prints messages
    :rtype: None
    """

    conn = psycopg2.connect(database = 'testdb', user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute(f"select * FROM M WHERE TO_USER = '{name}'" )
    Off_mess = cur.fetchall()
    for Mess in Off_mess:
        groupname = Mess[0]
        from_user = Mess[1]
        Message = Mess[3]
        if groupname == 'NULL':
            listen_socket_dict[name].send(str.encode("A text from contact"))
            listen_socket_dict[name].recv(1024).decode()
            listen_socket_dict[name].send(from_user.encode())
            listen_socket_dict[name].recv(1024).decode()
            listen_socket_dict[name].send(Message)
            print(listen_socket_dict[name].recv(1024).decode())
        else:
            listen_socket_dict[name].send(str.encode("a message from group"))
            print(listen_socket_dict[name].recv(1024).decode())
            listen_socket_dict[name].send(from_user.encode())
            print(listen_socket_dict[name].recv(1024).decode())
            listen_socket_dict[name].send(groupname.encode())
            print(listen_socket_dict[name].recv(1024).decode())
            listen_socket_dict[name].send(Message)
            print(listen_socket_dict[name].recv(1024).decode())
    cur.execute(f"DELETE FROM M WHERE TO_USER = '{name}';")
    conn.commit()

def offline_images(name):
    """Offline images recieving
    Connects to database and recieves all the images it got till now
    
    :param name: Username or name of the client
    :type name: string
    :return: prints images
    :rtype: None
    """
    conn = psycopg2.connect(database = 'testdb', user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute(f"select * FROM I WHERE TO_USER = '{name}'" )
    Off_mess = cur.fetchall()
    for Mess in Off_mess:
        groupname = Mess[0]
        from_user = Mess[1]
        Image = Mess[3]
        if groupname == 'NULL':
            listen_socket_dict[name].send(str.encode("An image from contact"))
            listen_socket_dict[name].recv(1024).decode()
            listen_socket_dict[name].send(from_user.encode())
            listen_socket_dict[name].recv(1024).decode()
            listen_socket_dict[name].send(Image)
            print(listen_socket_dict[name].recv(1024).decode())
        else:
            temp_sock = listen_socket_dict[name]
            temp_sock.send("An image from group".encode())
            temp_sock.recv(1024).decode()
            temp_sock.send(from_user.encode())
            temp_sock.recv(1024).decode()
            temp_sock.send(groupname.encode())
            temp_sock.recv(1024).decode()
            temp_sock.send(Image)
            print(temp_sock.recv(1024).decode())
    cur.execute(f"DELETE FROM I WHERE TO_USER = '{name}';")
    conn.commit()

send_socket_dict = {}   #Dictionary of sending sockets
listen_socket_dict = {} #Dictionary of listening sockets


#The function for chatroom that happens in server
def chatroom(name, sending_socket):
    """Chatroom function for a client with valid operations - ('REFRESH','SEND TEXT' , 'SEND IMAGE' , 'CREATE GROUP' , 'GROUP' , 'EXIT' , 'HELP' , 'GET_CONTACTS' , 'GET_CHAT')

        :param name:Username of Client
        :type name:string
        :param sending_socket:Sending socket
        :type sending_socket:socket
        """
    try:
        while True:
            print("----------------")
            operation = sending_socket.recv(1024).decode()
            
            #recieving username from client
            if operation == "REFRESH":
                offline_messages(name)
                offline_images(name)
                sending_socket.send("dummy".encode())
                print(f"\n---------------Got unread messages of {name}------------------\n")
            elif (operation == "SEND TEXT"):
                sending_socket.send(str.encode("Send text to :"))
                username = sending_socket.recv(1024).decode()
                
                while not searchtable(username,"UN","PASS_DICT","testdb"):
                    
                    #case when usename is not registered Asking to retype username
                    sending_socket.send(str.encode("ERROR: USERNAME " + username + " NOT FOUND\nRETYPE USERNAME: "))
                    username = sending_socket.recv(1024).decode()
                
                #Recieving message from client
                sending_socket.send(str.encode("TYPE MESSAGE: "))

                sending_socket.recv(1024)
                sending_socket.send(bytes(valuebykey(username, 5, 'pass_dict', 'testdb')))
                sending_socket.recv(1024)
                sending_socket.send(bytes(valuebykey(username, 6, 'pass_dict', 'testdb')))

                message = sending_socket.recv(1024)

                push_message(groupname="", sender = name, reciever = username, message = message)

                print(f"\n----------------Message sent from {name} to {username}------------------\n")

            
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
                push_image(groupname="", sender = name, reciever = username, image=imgdata)
                print(f"\n----------------Image sent from {name} to {username}------------------\n")

                
                sending_socket.send(str.encode("Image sent succesfully"))
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

                print(f"\n-------------------Group formed by {name}---------------------\n")
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
                        sending_socket.send(str.encode("Type SEND to send message\nIMAGE to send image\nVIEW to view participants\n"))
                        op = sending_socket.recv(1024).decode()
                        if op == "SEND":
                            sending_socket.send(str.encode("TYPE MESSAGE: "))
                            message = sending_socket.recv(1024).decode()
                            for user in valuebykey(groupname,2,"GROUPS","testdb"):
                                if not user == name:
                                    push_message(groupname=groupname, sender = name, reciever = user, message = message.encode())
                            sending_socket.send(str.encode("Succesfully sent your message to everyone in the group!\n"))

                        elif op == "VIEW":
                            for username in valuebykey(groupname,2,"GROUPS","testdb"):
                                sending_socket.send(username.encode())
                                sending_socket.recv(1024).decode()
                            sending_socket.send(str.encode("END"))
                        elif (op == "IMAGE"):
                            sending_socket.send(str.encode("Type image file name: "))
                            imgdata = sending_socket.recv(1166400)
                            for user in valuebykey(groupname,2,"GROUPS","testdb"):
                                if not user == name:
                                    push_image(groupname=groupname, sender = name, reciever = user, image=imgdata)
                                    
                            sending_socket.send("Successfully sent your image to everyone in the group!\n".encode())
                        elif op == "E":
                            sending_socket.send("------INVALID OPERATION IN GROUP---------".encode())

                    else:
                        sending_socket.send(str.encode("Type SEND to send message\nType IMAGE to send image\nType ADD to add participants\nREMOVE to remove participants\nVIEW to view participants\nDEL to delete group\n"))
                        op = sending_socket.recv(1024).decode()
                        if op == "SEND":
                            sending_socket.send(str.encode("TYPE MESSAGE: "))
                            message = sending_socket.recv(1024).decode()
                            for user in valuebykey(groupname,2,"GROUPS","testdb"):
                                if not user == name:
                                    push_message(groupname=groupname, sender = name, reciever = user, message = message.encode())
                                    
                            sending_socket.send(str.encode("Succesfully sent your message to everyone in the group!\n"))
                            
                        elif (op == "IMAGE"):
                            sending_socket.send(str.encode("Type image file name: "))
                            imgdata = sending_socket.recv(1166400)
                            for user in valuebykey(groupname,2,"GROUPS","testdb"):
                                if not user == name:
                                    push_image(groupname=groupname, sender = name, reciever = user, image=imgdata)
                                   
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
                                l = valuebykey(groupname,2,"GROUPS","testdb")
                                l.remove(username)
                                update_group(groupname,l,"user_list","groups","testdb")

                                sending_socket.send(str.encode("User " + username + " successfully removed from this group"))
                            
                        elif op == "DEL":
                            # groups.pop(groupname)
                            delrow(groupname,"GROUPS","testdb")
                            sending_socket.send(str.encode("Group " + groupname + " succesfully deleted"))
                        elif op == "E":
                            sending_socket.send("------INVALID OPERATION IN GROUP---------".encode())
                print(f"-------------------------------GROUP BY {name}-----------------------------------")
            elif (operation == "EXIT"):
                sending_socket.close()
                listen_socket_dict[name].close()
                update(name,"offline","status","PASS_DICT","testdb")
                update(name,'0',"connected_port","PASS_DICT","testdb")
                b = valuebykey(port,4,"server_conn_list","testdb")
                update_port(port,b-1,"balance","server_conn_list","testdb")
                if name in valuebykey(port,2,"server_conn_list","testdb"):
                    l = valuebykey(port,2,"server_conn_list","testdb")
                    l.remove(name)
                    update_port(port,l,"conn_user_list","server_conn_list","testdb")
                
            elif (operation == ""):
                update(name,"offline","status","PASS_DICT","testdb")
                update(name,'0',"connected_port","PASS_DICT","testdb")
                b = valuebykey(port,4,"server_conn_list","testdb")
                update_port(port,b-1,"balance","server_conn_list","testdb")
                if name in valuebykey(port,2,"server_conn_list","testdb"):
                    l = valuebykey(port,2,"server_conn_list","testdb")
                    l.remove(name)
                    update_port(port,l,"conn_user_list","server_conn_list","testdb")
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

    sending_socket.recv(1024)
    sending_socket.send(bytes(valuebykey(username, 5, 'pass_dict', 'testdb')))
    sending_socket.recv(1024)
    sending_socket.send(bytes(valuebykey(username, 6, 'pass_dict', 'testdb')))
    sending_socket.recv(1024)
    sending_socket.send(bytes(valuebykey(username, 7, 'pass_dict', 'testdb')))
    sending_socket.recv(1024)
    sending_socket.send(bytes(valuebykey(username, 8, 'pass_dict', 'testdb')))
    sending_socket.recv(1024)
    sending_socket.send(bytes(valuebykey(username, 9, 'pass_dict', 'testdb')))
    


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

    offline_messages(username)
    offline_images(name=username)

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
    sending_socket.send(str.encode("REGISTRATION SUCCESFUL :)"))

    priv_n = sending_socket.recv(2048)
    sending_socket.send("N recieved".encode())
    priv_e = sending_socket.recv(2048)
    sending_socket.send("E recieved".encode())
    priv_d = sending_socket.recv(2048)
    sending_socket.send("D recieved".encode())
    priv_p = sending_socket.recv(2048)
    sending_socket.send("P recieved".encode())
    priv_q = sending_socket.recv(2048)
    sending_socket.send("Q recieved".encode())
    

    insert(username,password,"online",port,"PASS_DICT","testdb", priv_n, priv_e, priv_d, priv_p, priv_q)

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