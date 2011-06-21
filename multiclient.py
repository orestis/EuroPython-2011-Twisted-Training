import socket

def make_connection(host, port, data_to_send):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(data_to_send)
    s.send('\r\n')
    b = []
    while True:
        data = s.recv(1024)
        if data:
            b.append(data)
        else:
            break

    return ''.join(b)


if __name__ == '__main__':

    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    for d in data_to_send:
        print 'sending', d
        print make_connection(host, int(port), d)


