# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # MultiThread TCP-SocketServer
# ********************************************************************************************

# Import libraries for networking communication and concurrency...

import socket
import threading
import constants
import os
import datetime


# Defining a socket object...
server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_address = constants.IP_SERVER


def main():
    print("***********************************")
    print("Server is running...")
    print("Dir IP:",server_address )
    print("Port:", constants.PORT)
    server_execution()
    

# Handler for manage incomming clients conections...
def handler_client_connection(client_connection,client_address):
    print(f'New incomming connection is coming from: {client_address[0]}:{client_address[1]}')
    is_connected = True
    while is_connected:
        data_recevived = client_connection.recv(constants.RECV_BUFFER_SIZE)
        remote_string = str(data_recevived.decode(constants.ENCONDING_FORMAT))
        remote_command = remote_string.split()
        command = remote_command[0]
        print (f'Data received from: {client_address[0]}:{client_address[1]}')

        if (command == constants.HEAD or command == constants.GET or command == constants.DELETE):
            success, myfile = search_file(remote_string)
            if (success == 1):
                try:
                    if (command.startswith(constants.HEAD)):
                        data_to_send = send_header(client_connection, 'HTTP/1.1 200 OK', myfile)
                        client_connection.sendall(data_to_send.encode(constants.ENCONDING_FORMAT))
                    elif (command.startswith(constants.GET)):
                        data_to_send = send_header(client_connection, 'HTTP/1.1 200 OK', myfile)
                        client_connection.sendall(data_to_send.encode(constants.ENCONDING_FORMAT))
                        f = open(myfile, 'r')
                        l = f.read(constants.RECV_BUFFER_SIZE)
                        while (l):
                            client_connection.send(l)
                            l = f.read(constants.RECV_BUFFER_SIZE)
                        f.close()
                    elif (command.startswith(constants.DELETE)):
                        os.remove(myfile)
                        data_to_send = send_header(client_connection, 'HTTP/1.1 200 OK', myfile)
                        client_connection.sendall(data_to_send.encode(constants.ENCONDING_FORMAT))     
                except:
                    data_to_send = send_header(client_connection, 'HTTP/1.1 500 Internal Server Error', 0)
                    client_connection.sendall(data_to_send.encode(constants.ENCONDING_FORMAT))
            else:
                data_to_send = send_header(client_connection, 'HTTP/1.1 404 Not Found', 0)
                client_connection.sendall(data_to_send.encode(constants.ENCONDING_FORMAT))
                client_connection.sendto('\\'.encode(constants.ENCONDING_FORMAT),('127.0.0.1',80))
        else:
            data_to_send = send_header(client_connection, 'HTTP/1.1 400 Bad Request', 0)
            client_connection.sendall(data_to_send.encode(constants.ENCONDING_FORMAT))
    
    print(f'Now, client {client_address[0]}:{client_address[1]} is disconnected...')
    client_connection.close()


#Function to start server process...
def server_execution():
    tuple_connection = (server_address,constants.PORT)
    server_socket.bind(tuple_connection)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print ('Socket is bind to address and port...')
    server_socket.listen(5)
    print('Socket is listening...')
    while True:
        client_connection, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handler_client_connection, args=(client_connection,client_address))
        client_thread.start()
    print('Socket is closed...')
    server_socket.close()


def send_header (client_connection, header, myfile):
    header += '\r\n'
    header += 'Date: ' + str(datetime.datetime.now()) + '\r\n'
    header += 'Server: ' + constants.IP_SERVER + '/' + str(constants.PORT) + '\r\n'
    if (myfile != 0):
        header += 'Content-Length: ' + str(os.stat(myfile).st_size) + '\r\n'
        header += 'Content-Type: ' + file_type(myfile) + '\r\n'
    header += '\r\n'
    return header


def search_file(command_received):
    myfile = command_received[1]
    myfile = myfile.split('?')[0]
    myfile = myfile.lstrip('/')
    exists = os.path.exists(myfile)
    if (exists):
        return 1, myfile
    else:
        return 0, myfile


# Return MIME type of the file
def file_type (myfile):
    if(myfile.endswith('.JPG')):
        return 'image/jpg'
    elif(myfile.endswith('.CSS')):
        return 'text/css'
    elif(myfile.endswith('.CSV')):
        return 'text/csv'
    elif(myfile.endswith('.PDF')):
        return 'application/pdf'
    elif(myfile.endswith('.DOC')):
        return 'application/msword'
    elif(myfile.endswith('.HTML')):
        return 'text/html'
    elif(myfile.endswith('.JSON')):
        return 'application/json'
    elif(myfile.endswith('.TXT')):
        return 'text/plain'
    else:
        return 'application/octet-stream'


if __name__ == "__main__":
    main()