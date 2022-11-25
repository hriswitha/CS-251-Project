# CS-251-Project

## Team: DEBUGGERS (Hriswitha, Vivek, Sohith)

## FastChat 
This project is a chat room with one server and multiple clients. The server provides a chat room for clients to join. After joining the chat, the clients can send messages to the chat room where all chat messages are logged and displayed.

### This project covers main domains:
- Password Authentication
- client-socket interaction
- Multi-server load balancing
- Message Encryption
- Shared Databasing
- Retrieving offline messages
- Groups and Personal Chats
- Performance Analysis (Done till logging, got errors in scripting)

Client has been implemented in `client.py`, server in `server.py` and load balancer in `loadbalancer.py`.

### Tech stack
1. `python3`
   libraries
   - `socket` for server and client interaction
   - `hashlib` for password encryption
   - `psycopg2` for databasing
   - `threading` for multiple client threads
   - `rsa` for assymmetric message encryption
   - `Fernet` for symmetric encryption
   - `logging` for creating log file of clients
2. PostgreSQL for databasing

### Running the chat
1. Setup the database in PostgreSQL. In out code it has been named `testdb`
2. Run the load balancer as 
   ```
   python3 loadbalancer.py <PORT1>
   ```
   Run this only once
3. Run the server as 
  ```
  python3 server.py <SERVER_PORT>
  ```
  We can run as many servers as we want but each with different server port
4. Run the client as 
  ```
  python3 client.py <PORT1>
  ```
  Here make sure the port number for client and load balancer as many as possible
5. Now by following the instructions that will appear on the client proceed your safe message 




### Team members contributions:
1. Hriswitha - Databasing, image sending
2. Vivek - Direct messages and message encryption
3. Sohith - Group working, interface, load balancing
