import socket
import os
import platform

""""
System tracker class find general information about the PC.
- Username of the user logged in
- Computer name
- OS type
- IP Address
"""
class SystemTracker():
    _instance = None
    system_info = {}
    
    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = SystemTracker()
            try:
                SystemTracker.system_info = {
                    'username': os.getlogin(),
                    'computer_name': socket.gethostname(),
                    'os': platform.platform(),
                    'ip': socket.gethostbyname(socket.gethostname())
                }
            except Exception as e:
                print(f"System tracking error: {e}")
        return cls._instance        