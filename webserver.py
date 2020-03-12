import os
import socket
import threading
import sys
import time

HOST = '127.0.0.1'      # localhost
PORT = int(sys.argv[1]) # Port
base_path = './Upload'  # base directory for content in server

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

def handler(conn, addr):
    response_content = b''
    path = ''
    try:    
        # Parse html request
        request = bytes.decode(data)
        request_words = request.split(' ')
        
        # Get the method type
        request_method = request_words[0]
        print("Method: ", request_method)
        print("Request: ", request)
        
        if request_method == 'GET':
            # Get the path
            path = request_words[1]
            response_content = b''
            server_header = b''
        
            # if there is no given path, use index.html
            if path[-1] == '/':
                path += 'index.html'
            cur_path = base_path + path
            
            # Check whether the file exists (For 404)
            if os.path.isfile(cur_path):
                # Check Permission (For 403)
                if(os.access(cur_path, os.R_OK)):
                    with open(cur_path, 'rb') as fr:
                        response_content = fr.read()
                    server_header = 'HTTP/1.1 200 OK\r\n'
                else:
                    server_header = 'HTTP/1.1 403 Forbidden\r\n'
            else:
                server_header = 'HTTP/1.1 404 Not Found\r\n'
        else:
            # we only support GET method now
            server_header = 'HTTP/1.1 405 Method Not Allowed\r\n'
    except:
        # some exeption happens: internal server error
        server_header = 'HTTP/1.1 500 Internal Server Error\r\n'
    # get file format
    words = path.split('.')
    file_format = ''
    if len(words) >= 2:
        file_format = path.split('.')[1]
    
    # send header remaining part
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    server_header += 'Date: {}\r\n'.format(current_time)
    server_header += 'Server: Eric-Server\r\n'
    
    # determine content-type (support url, jpg, and gif) 
    # If not I don't add content-type
    if file_format == 'html':
        server_header += 'Content-Type: text/html\r\n'
    elif file_format == 'jpg':
        server_header += 'Content-Type: image/jpeg\r\n'
    elif file_format == 'gif':
        server_header += 'Content-Type: image/gif\r\n'
    server_header += 'Connection: close\r\n\r\n'
    print(server_header)
    conn.sendall(server_header.encode())
    conn.sendall(response_content)
    conn.close()
    
if __name__ == '__main__':
    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)
        x = threading.Thread(target=handler, args=(conn, addr))
        x.start()
    conn.close()
    s.close()
    
