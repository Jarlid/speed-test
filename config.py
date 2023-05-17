from enum import Enum


class Connection(Enum):
    UDP = 0
    TCP = 1


MODE = Connection.TCP

DEFAULT_IP = '127.0.0.1'
DEFAULT_PORT = 6666
DEFAULT_ADDRESS = (DEFAULT_IP, DEFAULT_PORT)

TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
TIME_FORMAT_SIZE = 26

BATCH_SIZE = 1024
SERVER_TIMEOUT = 3
