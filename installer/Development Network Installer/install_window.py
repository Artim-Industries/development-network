import tkinter as tk
from tkinter import ttk
import os
import socket

def connect():
    lblError.place_forget()
    server = STRServer.get()
    id = STRID.get()
    if server != "" and id != "" and server != None and id != None:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            s.connect((server, 7077))
            s.send("SYN".encode())
            rcvdData = s.recv(1024).decode()
            if (rcvdData == "SYN ACK"):
                s.send("ACK RECEIVED".encode())
                start = s.recv(1024).decode()
                if (start == "file_start"):
                    s.send("ready".encode())
                    while True:
                        filetype = s.recv(1024).decode()
                        if (filetype == "stop"):
                            break
                        elif filetype == "dir":
                            dirname = s.recv(1024).decode()
                            if os.path.exists(dirname) == False:
                                os.mkdir(dirname)
                            print(f"[DIR] {dirname} got created")
                            s.send("continue".encode())
                            next = s.recv(1024).decode()
                            if (next == "next"):
                                print("[SERVER] Continuing")
                                continue
                            else:
                                break
                        elif filetype == "file":
                            filename = s.recv(1024).decode()
                            print(f"[FILE TRANSFER] {filename} got created")
                            with open(filename, "wb") as f:
                                while True:
                                    bytes_read = s.recv(4096)
                                    f.write(bytes_read)
                                    break
                                print("[FILE TRANSFER] Closed")
                            f.close()
                            s.send("continue".encode())
                            next = s.recv(1024).decode()
                            if (next == "next"):
                                print("[SERVER] Continuing")
                                continue
                            else:
                                break
                    print("[SOCKET] Closed")
                    s.close()
            else:
                lblError.configure(text="Server send an invalid response")
                lblError.place(x=90, y=450)
        except Exception:
            lblError.configure(text="Server is unreachable")
            lblError.place(x=90, y=450)
    else:
        lblError.configure(text="Please provide a Server and an ID")
        lblError.place(x=90, y=450)

window = tk.Tk()
window.resizable(False,False)
window.geometry("320x500")

window.iconbitmap('favicon.ico')
window.title("Development-Network Installer")


img = tk.PhotoImage(file="lg.png")
lblImage = tk.Label(window, image=img).pack()

STRServer = tk.StringVar(window)
lblServer = tk.Label(window, text="Server").place(x=40, y=360)
txtServer = ttk.Entry(window, width=28, textvariable=STRServer).place(x=90, y=360)

STRID = tk.StringVar(window)
lblID = tk.Label(window, text="ID").place(x=40, y=390)
txtID = ttk.Entry(window, width=28, textvariable=STRID).place(x=90, y=390)

def openLicense():
    os.startfile("license.txt")

lblError = tk.Label(window, text="Server is unreachable", foreground="red")
btnConnect = ttk.Button(window, text="Connect", command=connect).place(x=190, y=420)
btnConnect = ttk.Button(window, text="License", command=openLicense).place(x=90, y=420)
lbldata = ttk.Label(window, text="I agree to the data protection and license terms").place(x=40, y=480)

window.mainloop()