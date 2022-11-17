import array
import sys
import json
import os
from network import dhcp
import datetime

defaultPorts = {
    "LAN": {
        "amount": 2,
        "[::]:1": {
            "protocol": "TCP",
            "link": {
                "ip": "",
                "type": "",
                "sameNetwork": True
            },
            "state": "LISTENING"
        },
        "[::]:2": {
            "protocol": "TCP",
            "link": {
                "ip": "",
                "type": "",
                "sameNetwork": True
            },
            "state": "LISTENING"
        }
    }
}

with open(r"network\network.json") as f:
    NWData = json.load(f)

def createVPC(name: str, networkAD: str, defaultDHCP: bool = True, ports: dict = defaultPorts, DHCP: str = None):
    if defaultDHCP == True:
        ipv4 = dhcp.dhcpGenerateIpv4(networkAD)
        DHCP = ""
        for x in NWData[networkAD + ".0"]:
            if NWData[networkAD + ".0"][x]["isDHCPServer"] == True:
                DHCP = NWData[networkAD + ".0"][x]["ip"]
                break

        thisClient = len(NWData[networkAD + ".0"][DHCP]["DHCP-Server"]["clients"]) + 1
        today = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
        expireDate = today + datetime.timedelta(days=10)
        construction = {
            f"[::]:{thisClient}": {
                "ip": f"{ipv4}",
                "expiring": str(expireDate)
            }
        }
        NWData[networkAD + ".0"][DHCP]["DHCP-Server"]["clients"].update(construction)
        mac = dhcp.dhcpGenerateMac(networkAD)
        DHCPServer = dhcp.getDHCPServer(networkAD)
    else:
        DHCPServer = DHCP
        ipv4 = dhcp.getIPv4FromExternalDHCPServer(networkAD, DHCP)
        mac = dhcp.dhcpGenerateMac(networkAD)

    for x in NWData[networkAD + ".0"]:
        if NWData[networkAD + ".0"][x]["name"] == name:
            return "DVNP-011 || Name already assigned"

    construction = {
        f"{ipv4}": {
            "ip": f"{ipv4}",
            "mac": f"{mac}",
            "name": f"{name}",
            "type": "pc",
            "DHCP-enabled": True,
            "DHCP": {
                "DHCP-server": f"{DHCPServer}"
            },
            "ports": ports
        }
    }
    NWData[networkAD + ".0"].update(construction)
    with open(r"network\network.json", "w+") as c:
        c.write(json.dumps(NWData, indent=4))

    f = open(f"network/config/{ipv4}.json", "x")
    f.writelines("{}")
    f.close()

    with open(f"network\\config\\{DHCPServer}.json") as f:
        CFGData = json.load(f)

    DNSSuffix = CFGData["config"]["DNS-suffix"]
    const = {
        "config": {
            "firewall": {
                "active": True,
                "portForwarding": {}
            },
            "DNS-suffix": DNSSuffix,
            "host-name": str(name),
            "proxy-enabled": False,
            "proxy": {
                "proxy-server": ""
            }
        }
    }

    with open(f"network\\config\\{ipv4}.json") as f:
        configData = json.load(f)
    configData.update(const)
    with open(f"network\\config\\{ipv4}.json", "w+") as c:
        c.write(json.dumps(configData, indent=4))

   

def deleteVPC(networkAD: str, ipv4: str):
    networkAD = networkAD + ".0"
    try:
        if NWData[networkAD][ipv4]["type"] == "pc":
            portsDevice1 = []
            for port in NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["LAN"]:
                if port == "amount":
                    continue
                else:
                    portsDevice1.append(port)
            endIpv4 = []
            activePorts = []
            for activePortsDevice1 in portsDevice1:
                if NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["LAN"][activePortsDevice1]["state"] == "ESTABLISHED":
                    endIpv4.append(NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["LAN"][activePortsDevice1]["link"]["ip"])
                    activePorts.append(NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["LAN"][activePortsDevice1])
            for x in endIpv4:
                    for y in NWData[f"{networkAD}"][f"{x}"]["ports"]["LAN"]:
                        if y == "amount":
                            continue
                        else:
                            if ipv4 == NWData[f"{networkAD}"][f"{x}"]["ports"]["LAN"][y]["link"]["ip"]:
                                if NWData[f"{networkAD}"][f"{x}"]["ports"]["LAN"][str(y)]["state"] == "ESTABLISHED":
                                    NWData[f"{networkAD}"][f"{x}"]["ports"]["LAN"][y]["state"] = "LISTENING"
                                    NWData[f"{networkAD}"][f"{x}"]["ports"]["LAN"][y]["link"]["ip"] = ""
                                    NWData[f"{networkAD}"][f"{x}"]["ports"]["LAN"][y]["link"]["type"] = ""
                                    NWData[f"{networkAD}"][f"{x}"]["ports"]["LAN"][y]["link"]["sameNetwork"] = True
            del NWData[networkAD][ipv4]
            with open(r"network\network.json", "w+") as c:
                c.write(json.dumps(NWData, indent=4))
            os.remove(f"network/config/{ipv4}.json")
            return "No Error"
        else:
            return "This device is not a router"
    except KeyError:
        return "Ipv4 doesn't exists"

def createNetworkProfile(networkAD: str, ipv4: str):
    pass