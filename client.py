import tkinter
from engine import *
from config import DEFAULT_IP, DEFAULT_PORT
DEFAULT_BATCH_NUM = 5


def button_pressed():
    send_button['text'] = 'Отправка...'
    root.after(1, send_time)


def send_time():
    ip = ip_entry.get()
    port = int(port_entry.get())
    address = (ip, port)
    batch_num = int(pack_entry.get())

    client = start_client(address)
    timed_send(client, address, batch_num)

    send_button['text'] = 'Отправить'


root = tkinter.Tk()
root.title('UDP sender' if MODE == Connection.UDP else 'TCP sender')

tkinter.Label(text='IP получателя:').grid(row=0, column=0, sticky=tkinter.W, pady=5, padx=5)
ip_entry = tkinter.Entry()
ip_entry.insert(0, DEFAULT_IP)
ip_entry.grid(row=0, column=1, padx=5)

tkinter.Label(text='Порт получателя:').grid(row=1, column=0, sticky=tkinter.W, pady=5, padx=5)
port_entry = tkinter.Entry()
port_entry.insert(0, str(DEFAULT_PORT))
port_entry.grid(row=1, column=1)

tkinter.Label(text='Кол-во пакетов:').grid(row=2, column=0, sticky=tkinter.W, pady=5, padx=5)
pack_entry = tkinter.Entry()
pack_entry.insert(0, str(DEFAULT_BATCH_NUM))
pack_entry.grid(row=2, column=1)

send_button = tkinter.Button(text='Отправить', command=button_pressed)
send_button.grid(row=3, column=0, columnspan=2, pady=5, padx=5)

root.mainloop()
