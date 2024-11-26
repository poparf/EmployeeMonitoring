import socket
import os
import platform
from threading import Thread

""""
System tracker class find general information about the PC.
- Username of the user logged in
- Computer name
- OS type
- IP Address
"""
class SystemTracker(Thread):
    def __init__(self):
        super().__init__()
        self.system_info = {}

    def run(self):
        try:
            self.system_info = {
                'username': self.get_username(),
                'computer_name': self.get_computer_name(),
                'os': self.get_os(),
                'ip': self.get_ip()
            }
        except Exception as e:
            print(f"System tracking error: {e}")

    # find the computer name
    def get_computer_name(self):
        return socket.gethostname()

    # find the ip
    def get_ip(self):
        return socket.gethostbyname(socket.gethostname())

    # find the os type
    def get_os(self):
        return platform.platform()

    # get the username of the user logged in windows
    def get_username(self):
        return os.getlogin()
    
s = SystemTracker()
s.start()
s.join()