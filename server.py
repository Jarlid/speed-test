import tkinter
from engine import *
from config import DEFAULT_IP, DEFAULT_PORT, BATCH_SIZE, SERVER_TIMEOUT
from math import inf
MIL = 1000000


def button_pressed():
    recv_button['text'] = 'Получение...'
    root.after(1, recv_time)


def recv_time():
    ip = ip_entry.get()
    port = int(port_entry.get())
    address = (ip, port)

    server = start_server(address)
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

    pack_label['text'] = f'{len(batch_set)} из {batch_num}'
    time_label['text'] = f'{time_delta / MIL} c'
    speed_label['text'] = '%.6f МБ/c' % speed

    recv_button['text'] = 'Получить'


root = tkinter.Tk()
root.title('UDP receiver' if MODE == Connection.UDP else 'TCP receiver')

tkinter.Label(text='IP получения:').grid(row=0, column=0, sticky=tkinter.W, pady=5, padx=5)
ip_entry = tkinter.Entry()
ip_entry.insert(0, DEFAULT_IP)
ip_entry.grid(row=0, column=1, padx=5)

tkinter.Label(text='Порт получения:').grid(row=1, column=0, sticky=tkinter.W, pady=5, padx=5)
port_entry = tkinter.Entry()
port_entry.insert(0, str(DEFAULT_PORT))
port_entry.grid(row=1, column=1)

tkinter.Label(text='Пакетов получено:').grid(row=2, column=0, sticky=tkinter.W, pady=5, padx=5)
pack_label = tkinter.Label(text='-')
pack_label.grid(row=2, column=1, sticky=tkinter.W, padx=5)

tkinter.Label(text='Время:').grid(row=3, column=0, sticky=tkinter.W, pady=5, padx=5)
time_label = tkinter.Label(text='-')
time_label.grid(row=3, column=1, sticky=tkinter.W, padx=5)

tkinter.Label(text='Скорость:').grid(row=4, column=0, sticky=tkinter.W, pady=5, padx=5)
speed_label = tkinter.Label(text='-')
speed_label.grid(row=4, column=1, sticky=tkinter.W, padx=5)

recv_button = tkinter.Button(text='Получить', command=button_pressed)
recv_button.grid(row=5, column=0, columnspan=2, pady=5, padx=5)

root.mainloop()
