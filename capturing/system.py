import psutil
import socket
import os
import platform
import requests

# find the computer name
def get_computer_name():
    return socket.gethostname()

# find the ip
def get_ip():
    return socket.gethostbyname(socket.gethostname())

# find the os type
def get_os():
    return platform.platform()

# get the username of the user logged in windows
def get_username():
    return os.getlogin()

print(get_ip())
print(get_os())
print(get_computer_name())
print(os.getlogin())