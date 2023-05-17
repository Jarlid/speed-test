import socket
from config import Connection, MODE, DEFAULT_ADDRESS, TIME_FORMAT, TIME_FORMAT_SIZE, BATCH_SIZE

from random import randbytes
from datetime import datetime


def start_server(bind=DEFAULT_ADDRESS):
    print('Starting server.')
    if MODE == Connection.UDP:
        server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        server.bind(bind)
    else:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.bind(bind)
    print('Server started!', end='\n\n')
    return server


def start_client(address=DEFAULT_ADDRESS, timeout=None):
    if MODE == Connection.UDP:
        client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    else:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect(address)
    client.settimeout(timeout)
    return client


def establish_connection(server):
    if MODE == Connection.UDP:
        return server
    else:
        print('Waiting for connection...')
        server.listen()
        connection, _ = server.accept()
        print('Connected!', end='\n\n')
        return connection


def use_recv(servcon):
    if MODE == Connection.UDP:
        return servcon.recvfrom(BATCH_SIZE)
    else:
        return servcon.recv(BATCH_SIZE), None


def use_send(servcon, message, address):
    if MODE == Connection.UDP:
        servcon.sendto(message, address)
    else:
        servcon.send(message)


def timed_send(servcon, address, batch_num, batch_size=BATCH_SIZE):
    packages = generate_packages(batch_num, batch_size)
    time_prefix = datetime.now().strftime(TIME_FORMAT).encode('ascii')

    print('Sending packages...')
    for package in packages:
        use_send(servcon, time_prefix + package, address)
    print('Packages sent!', end='\n\n')


def generate_packages(batch_num, batch_size):
    print('Generating packages...')
    packages = []
    for i in range(1, batch_num + 1):
        package = '#' + str(batch_num) + '#' + str(i) + '#'
        package = package.encode('ascii')

        rand_size = batch_size - len(package) - TIME_FORMAT_SIZE
        if rand_size < 0:
            raise Exception('BATCH_SIZE is too small')
        package += randbytes(rand_size)

        packages.append(package)
    print('Packages generated!', end='\n\n')
    return packages


def parse_package(package):
    time_prefix, batch_num, curr_batch, *_ = package.split(b'#')
    return datetime.strptime(time_prefix.decode('ascii'), TIME_FORMAT),\
        int(batch_num.decode('ascii')), int(curr_batch.decode('ascii'))
