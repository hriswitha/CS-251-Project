import socket
import psycopg2
import sys

# conn = psycopg2.connect(database = 'testdb', user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
# cur = conn.cursor()
# cur.execute("drop table if exists messages;")
# cur.execute("create table messages(group text, from_user text not null, to_user not null, message bytea, image bytea);")

load_balance_socket = socket.socket()
load_balance_socket.bind(('localhost', int(sys.argv[1])))
load_balance_socket.listen(100)


def get_min():
    """Gets the minimum balances
    connect to database and returns the port with minimum load balance(in this case mini no of connections)

    :return: port number
    :rtype: int
    """
    conn = psycopg2.connect(database = 'testdb', user = "postgres", password = "1234", host = "127.0.0.1", port = "5432")
    cur = conn.cursor()
    cur.execute("SELECT * FROM server_conn_list WHERE server_status = 'online' ORDER BY balance asc;")
    try:
        return cur.fetchone()[0]
    except IndexError:
        return -1

while(True):
    c, addr = load_balance_socket.accept()
    c.send(str(get_min()).encode())
    c.close()
