import socket
import todo

host = '' 
port = 7600 

def server_socket(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))
    s.listen(1)
    return s

def parse_request(sock):
    data = sock.recv(4096)
    if not data:
        print "Bad request: no data"
        return ''
    line = data[0:data.find("\r")]
    print line
    headers = data[0:data.find("\r\n\r\n")]
    print headers

    method, uri, protocol = line.split()
    return [method, uri, protocol]

if __name__ == '__main__':
    server = server_socket(host, int(port))
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            sock, client_address = server.accept()
            request = parse_request(sock)
            sock.send("Successfully Connected!\r\n\r\n")

            uri = request[1]
            method = request[0]
            protocol = request[2]

            sock.send("URI: '%s' \nMethod: '%s'\r\n\r\n" % (uri, method))

            if len(uri)==1: # Root URL Parsed
                todo.load_todo_list()
                sock.send(todo.run_command('show',{'which':"All"}) + "\n")
            elif len(uri)>1: # Specific todo given
                if "/" in uri:
                    slash, value = uri.split("/")
                    sock.send(todo.run_command('show',{'which':value}) + "\n")

            sock.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()
