# CS-251-Project

## Team: DEBUGGERS (Hriswitha, Vivek, Sohith)

## FastChat 
This project is a chat room with one server and multiple clients. The server provides a chat room for clients to join. After joining the chat, the clients can send messages to the chat room where all chat messages are logged and displayed.

### This project covers main domains:
- Authentication
- client-socket interaction
- Multi-server load balancing (To be done)
- Encryption (To be done)
- Databasing

Client has been implemented in `client.py` and server in `server.py`.

### Tech stack
1. `python3`
   libraries
   - `socket` for server and client interaction
   - `hashlib` for password encryption
   - `psycopg2` for databasing
   - `threading` for multiple client threads
   - `rsa` and  for message encryption
2. PostgreSQL for databasing

### Running the chat
1. Setup the database in PostgreSQL. In out code it has been named `testdb`
2. Run the server as 
  ```
  python3 server.py <PORT>
  ```
  For now we are giving server from command line argument, but it will be changed in the end
3. Run the client as 
  ```
  python3 client.py <PORT>
  ```
  Here make sure the port number for server and client should be the same.
4. Now by following the instructions that will appear on the client proceed your safe message 


### Team members contributions:
1. Hriswitha - Databasing, image sending
2. Vivek - Direct messages and interface
3. Sohith - Group working
