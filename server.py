from engine import *
from config import BATCH_SIZE, SERVER_TIMEOUT
from math import inf
MIL = 1000000

server = start_server()
servcon = establish_connection(server)

batch_set = set()
batch_num = inf
send_time = None
last_time = None
started = False

try:
    while len(batch_set) < batch_num:
        send_time, batch_num, curr_batch = parse_package(use_recv(servcon)[0])
        last_time = datetime.now()
        batch_set.add(curr_batch)
        if not started:
            servcon.settimeout(SERVER_TIMEOUT)
            started = True
except socket.timeout:
    pass

time_delta = last_time - send_time
time_delta = MIL * time_delta.seconds + time_delta.microseconds
speed = BATCH_SIZE * len(batch_set) / time_delta

print('Packages sent:    ', batch_num)
print('Packages received:', len(batch_set))
print('Total time:', time_delta / MIL, 's')
print('Speed:', speed, 'MB/s')
