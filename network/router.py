import sys
import json
import os
from network import dhcp
from network import networkManager
import datetime

with open(r"network\network.json") as f:
    NWData = json.load(f)

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


def createVRouter(networkAD: str, deviceName: str, deviceDescription: str = None, networkType: str = "WiFi", DHCPEnabled: bool = True, isDHCPServer: bool = True, DHCPServer: str = "localhost", portConfig: dict = defaultPorts, startIP: str = ".1", endIP: str = ".255", overwrite: bool = False):
    if networkAD + ".0" not in NWData:
        if overwrite == True:
            networkManager.createNewNetwork(networkAD=networkAD)
        else:
            return "DVNP-002 || Cannot resolve Network-Adress. Creating Network not possible, because overwrite equals False"

    if DHCPEnabled == False and isDHCPServer == True:
        return "DVNP-001 || Device cannot be DHCP-Server with disabled DHCP"

    routerIP = dhcp.dhcpGenerateIpv4(networkAD)
    if routerIP == None:
        return "DVNP-006 || Failed to assign IP, because no IP is free."
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
            "ip": f"{routerIP}",
            "expiring": str(expireDate)
        }
    }
    NWData[networkAD + ".0"][DHCP]["DHCP-Server"]["clients"].update(construction)

    routerMAC = dhcp.dhcpGenerateMac(networkAD)
    publicIP = dhcp.dhcpGenerateIpv4(networkAD, 10) # Generate Public IP

    if isDHCPServer == True:
        safeLock = False
        for x in NWData[networkAD + ".0"]:
            if NWData[networkAD + ".0"][x]["isDHCPServer"] == True:
                safeLock = True

        if safeLock == True and overwrite == True:
            today = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
            expireDate = today + datetime.timedelta(days=10)
            construction = {
                routerIP: {
                    "ip": routerIP,
                    "mac": routerMAC,
                    "name": deviceName,
                    "type": "router",
                    "network-type": networkType,
                    "isGateway": True,
                    "Gateway": {
                        "publicIP": publicIP,
                        "hostname": ""
                    },
                    "WiFi": {
                        "networks": {
                            "amount": 0
                        }
                    },
                    "description": deviceDescription,
                    "DHCP-enabled": DHCPEnabled,
                    "DHCP": {
                        "DHCP-server": DHCPServer
                    },
                    "isDHCPServer": isDHCPServer,
                    "DHCP-Server": {
                        "IPRange": {
                            "type": "A",
                            "hostAdress": networkAD,
                            "startIP": networkAD + startIP,
                            "endIP": networkAD + endIP
                        },
                        "clients": {
                            "[::]:1": {
                                "ip": routerIP,
                                "expiring": str(expireDate)
                            }
                        }
                    },
                    "ports": portConfig
                }
            }
        elif safeLock == True and overwrite == False:
            return "DVNP-007 || Failed to create Router, because DHCP-Server is already in Network. (use overwrite=True to disable this error)"
        elif safeLock == False:
            today = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
            expireDate = today + datetime.timedelta(days=10)
            construction = {
                routerIP: {
                    "ip": routerIP,
                    "mac": routerMAC,
                    "name": deviceName,
                    "type": "router",
                    "network-type": networkType,
                    "WiFi": {
                        "networks": {
                            "amount": 0
                        }
                    },
                    "description": deviceDescription,
                    "DHCP-enabled": DHCPEnabled,
                    "DHCP": {
                        "DHCP-server": DHCPServer
                    },
                    "isDHCPServer": isDHCPServer,
                    "DHCP-Server": {
                        "IPRange": {
                            "type": "A",
                            "hostAdress": networkAD,
                            "startIP": networkAD + startIP,
                            "endIP": networkAD + endIP
                        },
                        "clients": {
                            "[::]:1": {
                                "ip": routerIP,
                                "expiring": str(expireDate)
                            }
                        }
                    },
                    "ports": portConfig
                }
            }
    else:
        construction = {
            routerIP: {
                "ip": routerIP,
                "mac": routerMAC,
                "name": deviceName,
                "type": "router",
                "network-type": networkType,
                "WiFi": {
                    "networks": {
                        "amount": 0
                    }
                },
                "description": deviceDescription,
                "DHCP-enabled": DHCPEnabled,
                "DHCP": {
                    "DHCP-server": DHCPServer
                },
                "isDHCPServer": isDHCPServer,
                "ports": portConfig
            }
        }

    NWData[networkAD + ".0"].update(construction)
    with open(r"network\network.json", "w+") as c:
        c.write(json.dumps(NWData, indent=4))
    
    f = open(f"network/config/{routerIP}.json", "x")
    f.writelines("{}")
    f.close()
    defaultConfig = {
        "firewall": {
            "active": True,
            "portForwarding": {
            }
        },
        "DNS-suffix": f"{deviceName}.local",
        "host-name": f"{deviceName}",
        "ip-routing-enabled": False,
        "proxy-enabled": False,
        "proxy": {
            "proxy-server": ""
        }
    }
    with open(f"network/config/{routerIP}.json") as f:
        data = json.load(f)
    data["config"] = defaultConfig
    with open(f"network/config/{routerIP}.json", "w+") as f:
        f.write(json.dumps(data, indent=4))

    pass


def deleteVRouter(networkAD: str, ipv4: str):
    networkAD = networkAD + ".0"
    try:
        if NWData[networkAD][ipv4]["type"] == "router":
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
                    endIpv4.append(
                        NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["LAN"][activePortsDevice1]["link"]["ip"])
                    activePorts.append(
                        NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["LAN"][activePortsDevice1])
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


def changeDNSSuffix(routerIP: str, newDNSSuffix: str):
    if os.path.exists(f"network\\config\\{routerIP}.json"):
        with open(f"network\\config\\{routerIP}.json") as f:
            data = json.load(f)

        data["config"]["DNS-suffix"] = newDNSSuffix

        with open(f"network\\config\\{routerIP}.json", "w+") as c:
            c.write(json.dumps(data, indent=4))
    else:
        return "DVNP-008 || Failed to resolve IP-Adress"

def changeHostName(routerIP: str, newHostname: str):
    if os.path.exists(f"network\\config\\{routerIP}.json"):
        with open(f"network\\config\\{routerIP}.json") as f:
            data = json.load(f)

        data["config"]["host-name"] = newHostname

        with open(f"network\\config\\{routerIP}.json", "w+") as c:
            c.write(json.dumps(data, indent=4))
    else:
        return "DVNP-008 || Failed to resolve IP-Adress"

def addProxyServer(routerIP: str, proxyServer: str):
    if os.path.exists(f"network\\config\\{routerIP}.json"):
        with open(f"network\\config\\{routerIP}.json") as f:
            data = json.load(f)

        data["config"]["proxy-enabled"] = True
        data["config"]["proxy"]["proxy-server"] = proxyServer

        with open(f"network\\config\\{routerIP}.json", "w+") as c:
            c.write(json.dumps(data, indent=4))
    else:
        return "DVNP-008 || Failed to resolve IP-Adress"

def removeProxyServer(routerIP: str):
    if os.path.exists(f"network\\config\\{routerIP}.json"):
        with open(f"network\\config\\{routerIP}.json") as f:
            data = json.load(f)

        data["config"]["proxy-enabled"] = False
        data["config"]["proxy"]["proxy-server"] = ""

        with open(f"network\\config\\{routerIP}.json", "w+") as c:
            c.write(json.dumps(data, indent=4))
    else:
        return "DVNP-008 || Failed to resolve IP-Adress"

def addPortForwarding(routerIP: str, port: str, hostAdress: str):
    if os.path.exists(f"network\\config\\{routerIP}.json"):
        with open(f"network\\config\\{routerIP}.json") as f:
            data = json.load(f)

        countPortForwarded = len(data["config"]["firewall"]["portForwarding"]) + 1
        usedPorts = []
        for x in data["config"]["firewall"]["portForwarding"]:
            usedPorts.append(data["config"]["firewall"]["portForwarding"][x]["port"])

        if port in usedPorts:
            return "DVNP-009 || Port already forwareded"

        construction = {
            f"[::]:{countPortForwarded}": {
                "port": port,
                "to": hostAdress
            }
        }
        data["config"]["firewall"]["portForwarding"].update(construction)
        with open(f"network\\config\\{routerIP}.json", "w+") as c:
            c.write(json.dumps(data, indent=4))
    else:
        return "DVNP-008 || Failed to resolve IP-Adress"

def removePortForwarding(routerIP: str, port: str):
    if os.path.exists(f"network\\config\\{routerIP}.json"):
        with open(f"network\\config\\{routerIP}.json") as f:
            data = json.load(f)

        success = False
        for x in data["config"]["firewall"]["portForwarding"]:
            if data["config"]["firewall"]["portForwarding"][x]["port"] == port:
                del data["config"]["firewall"]["portForwarding"][x]
                success = True
                break
        
        if success == False:
            return "DVNP-010 || Port-Forwarding not found"

        with open(f"network\\config\\{routerIP}.json", "w+") as c:
            c.write(json.dumps(data, indent=4))
    else:
        return "DVNP-008 || Failed to resolve IP-Adress"

def enableFirewall(routerIP: str):
    if os.path.exists(f"network\\config\\{routerIP}.json"):
        with open(f"network\\config\\{routerIP}.json") as f:
            data = json.load(f)

        data["config"]["firewall"]["active"] = True

        with open(f"network\\config\\{routerIP}.json", "w+") as c:
            c.write(json.dumps(data, indent=4))
    else:
        return "DVNP-008 || Failed to resolve IP-Adress"

def disableFirewall(routerIP: str):
    if os.path.exists(f"network\\config\\{routerIP}.json"):
        with open(f"network\\config\\{routerIP}.json") as f:
            data = json.load(f)
        
        data["config"]["firewall"]["active"] = False

        with open(f"network\\config\\{routerIP}.json", "w+") as c:
            c.write(json.dumps(data, indent=4))
    else:
        return "DVNP-008 || Failed to resolve IP-Adress"