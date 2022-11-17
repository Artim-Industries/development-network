import io
from network import dhcp, router
import json

with open("network/network.json") as f:
    NWData = json.load(f)

def createModem(networkAD: str, dhcpEnabled: bool = True, dhcpServer: str = None, ipv4: str = None, mac: str = None):
    if dhcpEnabled == True:
        ipv4 = dhcp.dhcpGenerateIpv4(networkAD)
        mac = dhcp.dhcpGeneratrMac(networkAD)
    pass

def deleteModem(networkAD: str, ipv4: str):
    pass