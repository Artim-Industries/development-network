import network
import sys
import os
import json
import network
from network import switch
from network import bridge, lan, pc
import time
import hashlib
import random
from http.server import BaseHTTPRequestHandler, HTTPServer

from network import router
from network import networkManager
from network import dhcp

def loop(networkAD):
    #print("loop!")
    with open(r"network\network.json") as r:
        NWData = json.load(r)
    switchIps = []
    for ip in NWData[f"{networkAD}.0"]:
        if NWData[f"{networkAD}.0"][ip]["type"] == "switch":
            switchIps.append(ip)
    for ip in switchIps:
        switch.initSwitch(networkAD=networkAD, ipv4=ip)


    bridgeIps = []
    for ip in NWData[f"{networkAD}.0"]:
        if NWData[f"{networkAD}.0"][ip]["type"] == "bridge":
            bridgeIps.append(ip)
    for ip in bridgeIps:
        bridge.initBridge(networkAD=networkAD, ipv4=ip)
        bridge.splitNetworkViaBridge(networkAD=networkAD, ipv4=ip)

    time.sleep(5)
    loop(networkAD)
    
#router.createVRouter("Router-1", networkAD="192.178.34")
#router.deleteVRouter(ipv4="192.178.34.1", networkAD="192.178.34")
#pc.deleteVPC(ipv4="192.178.34.2", networkAD="192.178.34")
#switch.createVSwitch(routerIpv4="192.178.34.1", networkAD="192.178.34")
#print(switch.deleteVSwitch("192.178.34", "192.178.34.6"))
#print(request.requestConnectionViaSwitch(networkAD="192.178.34", ipv4Switch="192.178.34.3", ipv4Device1="192.178.34.2", ipv4Device2="192.178.34.4", alreadyConnected=True))
#bridge.createVBridge(networkAD="192.178.34")
#router.changeDNSSuffix("10.10.10.1", "lemgen.local")

os.system("title Network Error Console")

#bridge.createVBridge("10.10.10", deviceName="V-Bridge-01")
#bridge.initBridge("10.10.10", "10.10.10.252")
#print(lan.createVConnection("10.10.10", "10.10.10.112", "10.10.10.252"))

#bridge.splitNetworkViaBridge("10.10.10", "10.10.10.252")
#print(dhcp.dhcpGenerateIpv4("10.10.10"))
#networkManager.connectToWiFi("10.10.10", "Great Balls of Fire", "10.10.10.223", "Mariella")
#networkManager.createWiFiNetwork("10.10.10.1", "Great Balls of Fire", "Mariella")
#switch.createVSwitch(routerIpv4="10.10.10.1", networkAD="10.10.10", deviceName="V-Switch-01")
#print(switch.deleteVSwitch("10.10.10", "10.10.10.194"))
#print(lan.createVConnection("10.10.10", "10.10.10.112", "10.10.10.223"))
#print(lan.deleteVConnection("10.10.10", "10.10.10.112", "10.10.10.1"))
#print(lan.deleteRouterConnection("10.10.10", "10.10.10.1", "10.10.10.112"))
#pc.deleteVPC("10.10.10", "10.10.10.123")
#print(pc.createVPC("V-PC-03", "10.10.10"))
#router.createVRouter(networkAD="10.10.10", deviceName="Router 10.10.10", deviceDescription="Router for the Network 10.10.10", overwrite=True)
#networkManager.createWiFiNetwork("10.10.10.1", "PS4 Netzwerk", "123", True)
#networkManager.deleteWiFiNetwork("10.10.10.1", "PS4 Netzwerk", "123")

#loop(networkAD="10.10.10")