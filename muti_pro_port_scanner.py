#!/usr/bin/env python3
import sys
import socket
import multiprocessing

def ports(ports_service):
    for port in list(range(1, 100))+[143,145,113,443,445,3306,3389,8080]:
        try:
            ports_service[port] = socket.getservbyport(port)
        except socket.error:
            pass


def ports_scan(host, posts_service):
    ports_open = []
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('socket creation error')
        sys.exit()
    for port in ports_service:
        try:
            sock.connect((host, port))
            ports_open.append(port)
            sock.close()
        except socket.error:
            pass
    return ports_open

if __name__ == '__main__':
    m = multiprocessing.Manager()
    ports_service = dict()
    results = dict()
    ports(ports_service)
    pool = multiprocessing.Pool(processes = 8)
    net = '127.0.0.'
    for host_number in map(str, range(1,2)):
        host = net + host_number
        results[host] = pool.apply_async(ports_scan, (host, ports_service))
        print("starting: "+host+'.....')
    pool.close()
    pool.join()
    for host in results:
        print('='*30)
        print(host,'.'*10)
        for port in results[host].get():
            print(port,'.', ports_service[port])
