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

def clean_uri(uri):
    if "/" in uri:
        slash, value = uri.split("/")
    return value

def handle_request(method):
    if method == "GET":
        todo.load_todo_list()
        if len(uri)==1: # Root URL Parsed
            output = sock.send(todo.run_command('show',{'which':"All"}) + "\n")
        elif len(uri)>1: # Specific todo given
            value = clean_uri(uri)
            output = sock.send(todo.run_command('show',{'which':value}) + "\n")

    if method == "DELETE":
        value = clean_uri(uri) # Don't check len(), delete todo mod will catch
        output = sock.send(todo.run_command('delete',{'which':value}) +
        "\n")

    if method == "POST":
        pass

    if method == "PUT":
        pass

    return output

if __name__ == '__main__':
    server = server_socket(host, int(port))
    print 'starting %s on %s...' % (host, port)
    try:
        while True:
            sock, client_address = server.accept()

            todo.load_todo_list()
            sock.send("Todo list loaded.\r\n\r\n")

            request = parse_request(sock)
            uri = request[1]
            method = request[0]
            protocol = request[2]
            sock.send("URI: '%s' \nMethod: '%s'\r\n\r\n" % (uri, method))

            handle_request(method)

            todo.save_todo_list()
            sock.send("Todo list saved.\r\n\r\n")

            sock.close()
    except KeyboardInterrupt:
        print 'shutting down...'
    server.close()
