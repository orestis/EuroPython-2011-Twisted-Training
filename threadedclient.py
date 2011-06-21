import threading
from multiclient import make_connection

def t_connection(host, port, d):
    print 'sending', d
    print make_connection(host, port, d)



if __name__ == '__main__':

    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    threads = []
    for d in data_to_send:
        t = threading.Thread(target=t_connection, args=(host, int(port), d))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print 'finished'


