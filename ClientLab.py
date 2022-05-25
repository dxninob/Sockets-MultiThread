# ********************************************************************************************
    # Lab: Introduction to sockets
    # Course: ST0255 - Telemática
    # TCP-Socket Client
# ********************************************************************************************

#Import libraries for networking communication...


import socket
import constants
import time
import re


def main():
    print('***********************************')
    print('Client is running...')
    print('Enter \"QUIT\" to exit')
    print('Input commands:')
    command_to_send = input()

    while True:
        client_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        client_socket.connect((constants.IP_SERVER,constants.PORT))
        if command_to_send == '':
            print('Please input a valid command...')
            command_to_send = input()    
        elif (command_to_send == constants.QUIT):
            break
        else:
            command_to_send += '\r\n\r\n'
            client_socket.send(bytes(command_to_send,constants.ENCONDING_FORMAT))
            file_content = b''
            while True:
                data_received = client_socket.recv(constants.RECV_BUFFER_SIZE)
                # print(data_received)
                if (len(data_received) < 1): break
                time.sleep(0.25)
                file_content = file_content + data_received
            response = file_content.split(b'\r\n\r\n')
            header = response[0].decode(constants.ENCONDING_FORMAT)
            print(header)
            if len(response) == 2 and response[1] != b'':
                f_name = file_name(header, command_to_send) 
                body = response[1]
                f = open(f_name, 'wb')
                f.write(body)
                f.close()
            command_to_send = input()
        client_socket.close() 
    print('BYE BYE...')


def file_name (header, request):
    name = ''
    header = header.split('\r\n')
    if '400 Bad Request' in header[0]:
        name = 'bad_request'
    else:
        try:
            name = request.split(' ')[1]
            name = name.split('?')[0]
            name = name.split('/')
            name = name[-1]
            name = ''.join(name.split('.')[:-1])
        except:
            name = 'name_error'
        
    
    mime_type = ''
    for line in header:
        if line.startswith('Content-Type:'):
            mime_type = line
            break
    mime_type = mime_type.split(';')
    mime_type = mime_type[0].split(' ')
    mime_type = mime_type[1]
    if(mime_type == 'image/jpg'):
        name += '.jpg'
    if(mime_type == 'image/jpeg'):
        name += '.jpeg'
    if(mime_type == 'image/png'):
        name += '.png'
    elif(mime_type == 'text/css'):
        name += '.css'
    elif(mime_type == 'text/csv'):
        name += '.csv'
    elif(mime_type == 'application/pdf'):
        name += '.pdf'
    elif(mime_type == 'application/msword'):
        name += '.doc'
    elif(mime_type == 'text/html'):
        name += '.html'
    elif(mime_type == 'application/json'):
        name += '.json'
    elif(mime_type == 'text/plain'):
        name += '.txt'
    return name


if __name__ == '__main__':
    main()