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
            server_header = ''
        
            if path == '/':
                path = '/index.html'
            cur_path = base_path + path
            
            # Check whether the file exists (For 404)
            if os.path.exists(cur_path):
                # Check Permission (For 403)
                if(bool(os.stat(cur_path).st_mode)):
                    with open(base_path + path, 'rb') as fr:
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
        server_header = 'HTTP/1.1 500 Internal Server Error\r\n'
    
    # send header remaining part
    current_time = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    server_header += 'Date: {}\r\n'.format(current_time)
    server_header += 'Server: Eric-Server\r\n'
    server_header += 'Connection: close\r\n\r\n'
    print(server_header)
    conn.sendall(server_header)
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
    