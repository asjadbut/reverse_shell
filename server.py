import socket
import sys
host = "103.104.214.235"
port = 9999

#function for creating a socket 
def create_socket():
    global s
    try:
        s = socket.socket()
    except:
        print("Error: " + str(socket.error))

create_socket()

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

bind_socket()

#function for establishing a connection with client (socket must be listening )
def accept_connection ():
    print("Accepting the connection!")
    connection,address  = s.accept()
    print("Connection established! IP: {} Port: {}".format(address[0],str(address[1])))

def send_commands(connection):
    print("Sending the data over the connection!")
    connection.send()