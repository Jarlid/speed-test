from engine import *

client = start_client()

batch_num = int(input('BATCH_NUM: '))
timed_send(client, DEFAULT_ADDRESS, batch_num)
