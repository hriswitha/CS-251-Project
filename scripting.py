from pwn import*
import random

def login(c, name, password):
    print(11)
    print(c.recvuntil(b': '))
    print(12)
    c.sendline("reg".encode())
    print(13)
    print(c.recvuntil(b': '))
    print(14)
    c.sendline(name.encode())
    print(15)
    print(c.recvuntil(b': '))
    print(16)
    c.sendline(password.encode())

def sendmessage(c, name, message):
    c.recvline()
    c.sendline("SEND TEXT".encode())
    c.recvline()
    c.sendline(name.encode())
    c.recvline()
    c.sendline(message.encode())

def sendimage(c, name, image):
    c.recvline()
    c.sendline("SEND TEXT".encode())
    c.recvline()
    c.sendline(name.encode())
    c.recvline()
    c.sendline(image.encode())

def recieve(c):
    c.recvline()
    c.sendline("REFRESH")


client = {}

c1 = process(["./client.py", "9999"])
client[1] = c1
c2 = process(["./client.py", "9999"])
client[2] = c2
c3 = process(["./client.py", "9999"])
client[3] = c3
c4 = process(["./client.py", "9999"])
client[4] = c4
c5 = process(["./client.py", "9999"])
client[5] = c5
c6 = process(["./client.py", "9999"])
client[6] = c6
c7 = process(["./client.py", "9999"])
client[7] = c7
c8 = process(["./client.py", "9999"])
client[8] = c8
c9 = process(["./client.py", "9999"])
client[9] = c9
c10 = process(["./client.py", "9999"])
client[10] = c10

# c1.interactive()

for i in range (10):
    print(i)
    login(client[i+1],f"name{str(i+1)}", f"pass{str(i+1)}")
    time.sleep(1)
    
for i in range (25):
    x = randint()%10 + 1
    y = randint()%10 + 1
    sendmessage(client[x], f"name{y}", f"A message from name{x} to name{y}")
    recieve(client[y])

