import threading
from multiclient import make_connection
import time

def t_connection(host, port, d):
    start = time.time()
    make_connection(host, port, d)
    print d, 'took', time.time() - start



if __name__ == '__main__':

    import sys
    host, port = sys.argv[1].split(':')
    data_to_send = sys.argv[2:]

    threads = []
    overallstart = time.time()
    for d in data_to_send:
        t = threading.Thread(target=t_connection, args=(host, int(port), d))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    print 'finished in', time.time() - overallstart


