import sys
import os


def onGetPath():
    path = os.path.dirname(__file__)
    path = os.path.normpath(path)
    A = path.split(os.sep)
    if len(A) >= 10:
        return "Zu Groß"
    elif len(A) == 1:
        return "International Error | Falscher Ordner"
    elif len(A) == 2:
        sys.path.append(f"{A[0]}/{A[2]}/")
        P = f"{A[0]}/"
        T = P.split("/")
        return f"{T[0]}/{A[2]}/"
    elif len(A) == 3:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/")
        P = f"{A[0]}/{A[1]}"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{A[2]}/"
    elif len(A) == 4:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{A[3]}/"
    elif len(A) == 5:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{T[3]}/{A[4]}/"
    elif len(A) == 6:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{T[3]}/{T[4]}/{A[5]}/"
    elif len(A) == 7:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{T[3]}/{T[4]}/{T[5]}/{A[6]}/"
    elif len(A) == 8:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{T[3]}/{T[4]}/{T[5]}/{T[6]}/{A[7]}/"
    elif len(A) == 9:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/{A[8]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/{[A[8]]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{T[3]}/{T[4]}/{T[5]}/{T[6]}/{T[7]}/{A[8]}/"
    elif len(A) == 10:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/{A[8]}/{A[9]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/{[A[8]]}/{A[9]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{T[3]}/{T[4]}/{T[5]}/{T[6]}/{T[7]}/{A[8]}/{A[9]}/"
    elif len(A) == 11:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/{A[8]}/{A[9]}/{A[10]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/{[A[8]]}/{A[9]}/{A[10]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{T[3]}/{T[4]}/{T[5]}/{T[6]}/{T[7]}/{A[8]}{A[9]}/{A[10]}/"
    elif len(A) == 12:
        sys.path.append(f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/{A[8]}/{A[9]}/{A[10]}/{A[11]}/")
        P = f"{A[0]}/{A[1]}/{A[2]}/{A[3]}/{A[4]}/{A[5]}/{A[6]}/{A[7]}/{[A[8]]}/{A[9]}/{A[10]}/{A[11]}/"
        T = P.split("/")
        return f"{T[0]}/{T[1]}/{T[2]}/{T[3]}/{T[4]}/{T[5]}/{T[6]}/{T[7]}/{A[9]}/{A[10]}/{A[11]}/"


def send(args=[]):
    file = open(f"{onGetPath()}module/data/backdata.json", "a+")
    file.write(args[0])
    file.close()
    return "Successfully written data to file 'backdata.json'"


def clear():
    file = open(f"{onGetPath()}data/backdata.json", "r+")
    file.truncate()
    return "Successfully cleared data in file 'backdata.json'"

import socket
import time
import sysconfig
import threading
import datetime
import random
import abc
import sys
import json

ownipaddress = socket.gethostname()


def root_key_generation():
    number = random.random()
    r = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
         'w', 'x', 'y', 'z']
    s = []
    for i in range(10):
        rd = random.choice(r)
        s.append(rd)
    strs = f"-{s[0]}{s[1]}{s[2]}{s[3]}{s[4]}-{s[5]}{s[6]}290347{s[7]}{s[8]}-{s[9]}{number}#"
    return strs


def client(endip, endport):
    # Connecting To Server
    c = socket.socket()
    server_host = endip

    try:
        c.connect((server_host, endport))
        print(f"Connected with {endip}")
    except socket.gaierror as e:
        print("Couldn't connect to IP")
    
def back_client(ip, error):
    c = socket.socket()
    c.connect((ip, 18583))
    c.send("error".encode('ascii'))
    c.close()

def connect_client(ip, port, add):
    # Connecting To Server
    toolbar_width = 24

    # setup toolbar
    sys.stdout.write("[%s]" % (" " * toolbar_width))
    sys.stdout.flush()
    sys.stdout.write("\b" * (toolbar_width+1))

    for i in range(toolbar_width):
        time.sleep(0.1) 
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")
    c = socket.socket()
    server_host = ip

    try:
        c.connect((server_host, port))
        time.sleep(1)

        print("--- Please Authorize ---\n")
        inp_c = input(f"remote/{ip}/")
        args = inp_c.split(" ")
        #Statement: login --username "{username}" --password "{password}"
        if args[0] == "login":
            if args[1].startswith("--"):
                if args[1] == "--username":
                    if args[2].startswith('"'):
                        if args[2].endswith('"'):
                            if args[3].startswith("--"):
                                if args[3] == "--password":
                                    if args[4].startswith('"'):
                                        if args[4].endswith('"'):
                                            uid_arg = args[2].split('"')[1]
                                            pwd_arg = args[4].split('"')[1]
                                            c.send(f"USERDATAREQUEST: {uid_arg} {pwd_arg} {add}".encode('ascii'))
                                        else:
                                            print("Wrong Statement")
                                    else:
                                        print("Wrong Statement")
                                else:
                                    print("Wrong Statement")
                            else:
                                print("Wrong Statement")
                        else:
                            print("Wrong Statement")
                    else:
                        print("Wrong Statement")
                else:
                    print("Wrong Statement")
            else:
                print("Wrong Statement")

        print(f"Established Connection with {ip}")
        
    except socket.gaierror as e:
        time.sleep(1)
        print("Couldn't connect to IP\n")
    finally:
        time.sleep(1)
        command(add)




def server():
    s = socket.socket()

    host_name = socket.gethostname()
    s_ip = socket.gethostbyname(host_name)
    s.bind((s_ip, 18583))
    s.listen()

    # Receiving / Listening Function
    def receive():
        client(ownipaddress, 18583)
        while True:
            # Accept Connection
            c, address = s.accept()
            requests = c.recv(1024).decode('ascii')
            if requests.startswith("USERDATAREQUEST: "):
                args = requests.split(" ")
                back_ip = args[3]
                username = args[1]
                password = args[2]

                with open("users.json") as f:
                    data = json.load(f)
                if data['Users'][str(back_ip)]['username'] == username:
                    if data['Users'][str(back_ip)]['password'] == password:
                        back_client(back_ip, "ConnectedandAuthorized")
                    else:
                        back_client(back_ip, "Wrong password")
                else:
                    back_client(back_ip, "Wrong username")
            elif requests.startswith("Wrong"):
                print(requests)
            elif requests == "ConnectedandAuthorized":
                print(requests)
                
            else:
                command(address)
            


    receive()


def command(add):
    t = input("command--/")
    args = t.split(" ")
    if args[0] == "connect":
        if args[1].startswith("--"):
            if args[1] == "--ip":
                if args[2].startswith('"'):
                    if args[2].endswith('"'):
                        args = args[2].split('"')
                        print("Setting up Connection...")
                        time.sleep(1)
                        connect_client(args[1], 18583, add)
                    else:
                        print("Wrong Statement")
                else:
                    print("Wrong Statement")
            else:
                print("Wrong Statement")
        else:
            print("Wrong Statement")
    else:
        pass

def main():
    server()


main()
