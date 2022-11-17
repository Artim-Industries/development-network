import sys
import json
import os
from network import dhcp
import network
import datetime

with open(r"network\network.json") as f:
    NWData = json.load(f)

defaultConfiguration = {
    "layer": {
        "amount": 2,
        "[LAYER]:1": {
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
        },
        "[LAYER]:2": {
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
    }
}


def createVBridge(networkAD: str, deviceName: str = "Virtuelle Bridge", decription: str = None, defaultDhcp: bool = True, dhcpServer: str = None, ipv4: str = None, mac: str = None, portsConfiguration: dict = defaultConfiguration):
    if defaultDhcp == True:
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
    if dhcpServer != None:
        device = dhcpServer
    else:
        for device in NWData[f"{networkAD}.0"]:
            if NWData[f"{networkAD}.0"][f"{device}"]["isDHCPServer"] == True:
                break
    construction = {
        f"{ipv4}": {
            "ip": f"{ipv4}",
            "mac": f"{mac}",
            "name": f"{deviceName}",
            "decription": f"{decription}",
            "type": "bridge",
            "DHCP-enabled": defaultDhcp,
            "DHCP": {
                "DHCP-server": f"{device}"
            },
            "ports": portsConfiguration
        }
    }
    f = open(f"network/config/{ipv4}.json", "x")
    f.writelines('{"config": {}, "table":{}, "network":{}}')
    f.close()
    NWData[networkAD + ".0"].update(construction)
    with open(r"network\network.json", "w+") as c:
        c.write(json.dumps(NWData, indent=4))
    with open(rf"network\config\{ipv4}.json") as f:
        CFGData = json.load(f)
    CFGData["config"]["onlySwitchConnectable"] = True
    for layer in NWData[f"{networkAD}.0"][f"{ipv4}"]["ports"]["layer"]:
        if layer == "amount":
            continue
        else:
            ports = []
            for port in NWData[f"{networkAD}.0"][f"{ipv4}"]["ports"]["layer"][f"{layer}"]["LAN"]:
                if port == "amount":
                    continue
                else:
                    ports.append(port)
            for layer in NWData[f"{networkAD}.0"][f"{ipv4}"]["ports"]["layer"]:
                if layer == "amount":
                    continue
                TempLayerConfig = {
                    f"{layer}": {}
                }
                for port in ports:
                    TempPortConfig = {
                        f"{port}": {
                            "ipv4": "",
                            "mac": ""
                        }
                    }
                    TempLayerConfig[layer].update(TempPortConfig)
                CFGData["table"].update(TempLayerConfig)
    with open(rf"network\config\{ipv4}.json", "w+") as w:
        w.write(json.dumps(CFGData, indent=4))


def initBridge(networkAD: str, ipv4: str):
    with open(r"network\network.json") as f:
        NWData = json.load(f)
    networkAD = networkAD + ".0"
    with open(rf"network\config\{ipv4}.json") as r:
        CFGData = json.load(r)
    for layer in NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["layer"]:
        if layer == "amount":
            continue
        else:
            # print(f"---------- LAYER: {layer} ----------")
            connectedports = []
            notConnectedPorts = []
            for port in NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["layer"][layer]["LAN"]:
                if port == "amount":
                    continue
                else:
                    if NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["layer"][f"{layer}"]["LAN"][port]["state"] == "ESTABLISHED":
                        connectedports.append(port)
                    else:
                        notConnectedPorts.append(port)
            connectedPortsIP = []
            for connectedPort in connectedports:
                ip = NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["layer"][layer]["LAN"][connectedPort]["link"]["ip"]
                connectedPortsIP.append(ip)
            connectedPortsMAC = []
            for ip in connectedPortsIP:
                mac = NWData[f"{networkAD}"][f"{ip}"]["mac"]
                connectedPortsMAC.append(mac)
            for ip in connectedPortsIP:
                indexIp = connectedPortsIP.index(ip)
                mac = connectedPortsMAC[indexIp]
                port = connectedports[indexIp]
                CFGData["table"][layer][port]["ipv4"] = ip
                CFGData["table"][layer][port]["mac"] = mac
            for port in notConnectedPorts:
                CFGData["table"][layer][port]["ipv4"] = ""
                CFGData["table"][layer][port]["mac"] = ""
            # print(connectedports)
            # print(notConnectedPorts)
    with open(rf"network\config\{ipv4}.json", "w+") as w:
        json.dump(CFGData, w, indent=4)

def split_list(a_list):
    half = len(a_list)//2
    return a_list[:half], a_list[half:]

def splitNetworkViaBridge(networkAD: str, ipv4: str): #Fehler: NW1 = 1-5 NW2 = 7-10 Falsche einschreibung
    with open(r"network\network.json") as f:
        NWData = json.load(f)
    with open(rf"network\config\{ipv4}.json") as r:
        CFGData = json.load(r)
    if CFGData["config"]["onlySwitchConnectable"] == True:
        CFGData["network"]["[NETWORK]:1"]["ips"] = []
        CFGData["network"]["[NETWORK]:2"]["ips"] = []

        clients = []
        for device in NWData[networkAD + ".0"]:
            try:
                if NWData[networkAD + ".0"][device]["isDHCPServer"] == True:
                    for client in NWData[networkAD + ".0"][device]["DHCP-Server"]["clients"]:
                        if NWData[networkAD + ".0"][device]["DHCP-Server"]["clients"][client]["ip"] == ipv4:
                            continue
                        else:
                            clients.append(NWData[networkAD + ".0"][device]["DHCP-Server"]["clients"][client]["ip"])
            except KeyError:
                continue

        network1, network2 = split_list(clients)

        for address in network1:
            CFGData["network"]["[NETWORK]:1"]["ips"].append(address)
        
        for address in network2:
            CFGData["network"]["[NETWORK]:2"]["ips"].append(address)

        with open(rf"network\config\{ipv4}.json", "w+") as w:
            w.write(json.dumps(CFGData, indent=4))
        """
        for layer in CFGData["table"]:
            if layer == "amount":
                continue
            else:
                with open(rf"network\config\{ipv4}.json") as r:
                    CFGData = json.load(r)
                allLayers = []
                for l in CFGData["table"]:
                    allLayers.append(l)
                # print(f"------- LAYER: {layer} -------")
                ports = []
                for port in CFGData["table"][layer]:
                    ports.append(port)
                activePorts = []
                inactivePorts = []
                for port in ports:
                    if CFGData["table"][layer][port]["ipv4"] != "":
                        activePorts.append(port)
                    else:
                        inactivePorts.append(port)
                if len(allLayers) >= 2:
                    activeIps = []
                    for port in activePorts:
                        activeIps.append(CFGData["table"][layer][port]["ipv4"])
                    ipEnds = []
                    for ip in activeIps:
                        ip = ip.split(".")[-1]
                        ipEnds.append(ip)
                    try:
                        smallestIPEnd = min(ipEnds)
                        biggestIPEnd = max(ipEnds)
                    except ValueError:
                        smallestIPEnd = "0"
                        biggestIPEnd = "0"
                    for x in range(10):
                        layer = layer.split(":")[-1]
                        try:
                            if CFGData["network"][f"[NETWORK]:{layer}"]["ips"] == []:
                                for deviceIP in NWData[f"{networkAD}.0"]:
                                    deviceIPEnding = deviceIP.split(".")[-1]
                                    if deviceIPEnding >= smallestIPEnd and deviceIPEnding <= str(biggestIPEnd):
                                        CFGData["network"][f"[NETWORK]:{layer}"]["ips"].append(str(deviceIP))
                                with open(rf"network\config\{ipv4}.json", "w+") as w:
                                    w.write(json.dumps(CFGData, indent=4))
                                break
                            else:
                                CFGData["network"][f"[NETWORK]:{layer}"]["ips"] = []
                        except KeyError:
                            CFGData["network"][f"[NETWORK]:{layer}"] = {
                                "ips": []
                            }
                            with open(rf"network\config\{ipv4}.json", "w+") as w:
                                w.write(json.dumps(CFGData, indent=4))
                else:
                    return "Nothing to split!"
        """
    else:
        pass
