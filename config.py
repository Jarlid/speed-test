from enum import Enum


class Connection(Enum):
    UDP = 0
    TCP = 1


MODE = Connection.TCP

PORT = 6666
IP = '127.0.0.1'
DEFAULT_ADDRESS = (IP, PORT)

TIME_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
TIME_FORMAT_SIZE = 26

BATCH_SIZE = 1024
SERVER_TIMEOUT = 3
