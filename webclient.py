import socket
import sys                        
  
host = sys.argv[1]
port = int(sys.argv[2])
file_name = sys.argv[3] 
requet = 'GET {}'.format(file_name)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Connecting to {}:{}'.format(host, port))
sock.connect((host, port))

if file_name == '/':
    file_name = '/index.html'
request = 'GET {0}'.format(file_name)
sock.sendall(request)

resp_data = b''
while True:
    data = sock.recv(1024)
    if data == b'':
        break
    resp_data += data
response_words = resp_data.split(b'\r\n\r\n')
info = response_words[0]
method = int(response_words[0].split()[1])
output_data = response_words[-1]
print info

if method == 200:
    with open('./Download' + file_name, 'wb') as fw:
        fw.write(output_data)
else:
    print 'failed! I will download nothing!'

print('Close socket')
sock.close()