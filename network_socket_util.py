from collections.abc import Callable, Iterable, Mapping
import socket
import threading
from typing import *
from typing import Any

def server_listener(HOST: str, PORT: int, callable_event_trigger: callable, buffer_size: int = 1024, **kwargs) -> callable:

    def instance():
        _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        _socket.bind((HOST, PORT))
        _socket.listen(1)

        while True:
            c_socket, c_address = _socket.accept()
            message = c_socket.recv(buffer_size).decode("utf-8")
            callable_event_trigger(message)

            c_socket.close()

    return instance

def client_sender(HOST: str, PORT: int, message: Union[callable, str], after_sent_callback: Optional[callable] = None) -> callable:
    def instance():
        _message: str =  message if not callable(message) and isinstance(message, str) else str(message())
        #automatically convert the message from a list
        
        try:
            _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            _socket.connect((HOST, PORT))
            _socket.send(_message.encode("utf-8"))
            if callable(after_sent_callback):
                after_sent_callback()
            _socket.close()
        except Exception as e:
            print(e)

    return instance

'''class default_threading(threading.Thread):
    def __init__(target: Callable[..., object]) -> None:
        super().__init__(target = target, daemon = True)'''


class network_sender:
    def __init__(self, target_ip:str, sending_port:int, own_ip: str = None, stat_receiving_port:int = None,
                 receiving_callback: Callable[[int], None] = None, **kwargs) -> None:
        self.target_ip = target_ip
        self.sending_port = sending_port

        self.own_ip = own_ip
        self.stat_receiving_port = stat_receiving_port
        
        self._receiving_callback = receiving_callback

        self.status_receiver = server_listener(self.own_ip, self.stat_receiving_port, self.receive_callback)
        self.threads = threading.Thread(target= self.status_receiver)
        self.threads.daemon = True
        self.threads.start()

    def config(self, **kwargs):
        if "sending_port" in kwargs:
            self.sending_port = kwargs["sending_port"]
        elif "target_ip" in kwargs:
            self.target_ip = kwargs["target_ip"]

    def send(self, message: Optional[Union[str, callable]], after_sent_callback: Optional[callable] = None):
        _message: str =  message if not callable(message) and isinstance(message, str) else str(message())
        format_message = f"{self.own_ip}//{self.stat_receiving_port}~/{_message}"
        temp:client_sender = client_sender(self.target_ip, self.sending_port, format_message, after_sent_callback)
        temp()

    def receive_callback(self, m: str):
        messages: List[str] = m.split('~/')
        status: int = int(messages[0] == f"{self.own_ip}//{self.stat_receiving_port}")
        if self._receiving_callback is not None:
            self._receiving_callback(status)

class network_receiver:
    def __init__(self, own_ip: str = None, own_port:int = None,
                 receiving_callback: Callable[[str], None] = None, buffer_size:int = 1024, **kwargs) -> None:

        self.own_ip = own_ip
        self.own_port = own_port

        def receiving_sequence(m):
            message_list: List[str] = m.split("~/")
            raw_message: str = message_list[-1]
            sender_address: tuple = message_list[0].split("//")
            client_sender(sender_address[0], int(sender_address[1]), f"{sender_address[0]}//{sender_address[1]}~/Complete")()

            receiving_callback(raw_message)

        self.receiver = server_listener(self.own_ip, self.own_port, receiving_sequence, buffer_size)
        self.threads = threading.Thread(target= self.receiver)
        self.threads.daemon = True

    def start_receiving(self):
        if self.threads:
            self.threads.start()