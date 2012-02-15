import socket
import todo
import pdb

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

def clean_uri(uri):
    if "/" in uri:
        slash, value = uri.split("/")
    return value


def handle_request(uri, method):
    value = clean_uri(uri)
    # list comprehension, you dumbass
    commands = {
            'GET': ['show',{'which':value}],
            'DELETE':['delete',{'which':value}],
            'POST':[],
            'PUT':[],
            }

    result = todo.run_command(commands[method][0],commands[method][1])

    output = sock.send(str(result) + "\n")
    #return output

def main_loop():
    server = server_socket(host, int(port))
    print 'starting %s on %s...' % (host, port)
    try:
        while true:
            sock, client_address = server.accept()

            todo.load_todo_list()
            sock.send("todo list loaded.\r\n\r\n")

            request = parse_request(sock)
            uri = request[1]
            method = request[0]
            protocol = request[2]
            sock.send("uri: '%s' \nmethod: '%s'\r\n\r\n" % (uri, method))

            handle_request(uri, method)
            todo.save_todo_list()
            sock.send("todo list saved.\r\n\r\n")

            sock.close()
    except keyboardinterrupt:
        print 'shutting down...'
    server.close()

if __name__ == '__main__':
    main_loop()
