import sys
import json
import os
from network import dhcp, router
import network
import datetime


defaultPorts = {
    "fields": {
        "amount": 2,
        "[::]:1": {
            "type": "PoE",
            "layers": {
                "amount": 2,
                "[::]:1": {
                    "LAN": {
                        "amount": 5,
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
                        },
                        "[::]:3": {
                            "protocol": "TCP",
                                        "link": {
                                            "ip": "",
                                            "type": "",
                                            "sameNetwork": True
                                        },
                            "state": "LISTENING"
                        },
                        "[::]:4": {
                            "protocol": "TCP",
                                        "link": {
                                            "ip": "",
                                            "type": "",
                                            "sameNetwork": True
                                        },
                            "state": "LISTENING"
                        },
                        "[::]:5": {
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
                "[::]:2": {
                    "LAN": {
                        "amount": 5,
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
                        },
                        "[::]:3": {
                            "protocol": "TCP",
                                        "link": {
                                            "ip": "",
                                            "type": "",
                                            "sameNetwork": True
                                        },
                            "state": "LISTENING"
                        },
                        "[::]:4": {
                            "protocol": "TCP",
                                        "link": {
                                            "ip": "",
                                            "type": "",
                                            "sameNetwork": True
                                        },
                            "state": "LISTENING"
                        },
                        "[::]:5": {
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
        },
        "[::]:2": {
            "type": "PoE",
            "layers": {
                "amount": 2,
                "[::]:1": {
                    "LAN": {
                        "amount": 5,
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
                        },
                        "[::]:3": {
                            "protocol": "TCP",
                                        "link": {
                                            "ip": "",
                                            "type": "",
                                            "sameNetwork": True
                                        },
                            "state": "LISTENING"
                        },
                        "[::]:4": {
                            "protocol": "TCP",
                                        "link": {
                                            "ip": "",
                                            "type": "",
                                            "sameNetwork": True
                                        },
                            "state": "LISTENING"
                        },
                        "[::]:5": {
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
                "[::]:2": {
                    "LAN": {
                        "amount": 5,
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
                        },
                        "[::]:3": {
                            "protocol": "TCP",
                                        "link": {
                                            "ip": "",
                                            "type": "",
                                            "sameNetwork": True
                                        },
                            "state": "LISTENING"
                        },
                        "[::]:4": {
                            "protocol": "TCP",
                                        "link": {
                                            "ip": "",
                                            "type": "",
                                            "sameNetwork": True
                                        },
                            "state": "LISTENING"
                        },
                        "[::]:5": {
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
        },
        "[ROUTERPORT]": {
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


def createVSwitch(routerIpv4: str, networkAD: str, deviceName: str = "Virtuelles Switch", description: str = None, defaultDHCP: bool = True, ipv4: str = None, mac: str = None, ports: dict = defaultPorts, DHCP: str = None):
    with open(r"network\network.json") as f:
        NWData = json.load(f)
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

    construction = {
        f"{ipv4}": {
            "ip": f"{ipv4}",
            "mac": f"{mac}",
            "name": f"{deviceName}",
            "type": "switch",
            "description": description,
            "DHCP-enabled": True,
            "DHCP": {
                "DHCP-server": f"{DHCPServer}",
            },
            "ports": ports,
        }
    }
    
    routerport = construction[ipv4]["ports"]["fields"]["[ROUTERPORT]"]
    Router = NWData[networkAD + ".0"][routerIpv4]["ports"]["LAN"]
    for port in Router:
        if port == "amount":
            continue
        else:
            if Router[port]["state"] == "LISTENING":
                Router[port]["link"]["ip"] = ipv4
                Router[port]["link"]["type"] = "switch"
                Router[port]["state"] = "ESTABLISHED"

                routerport["link"]["ip"] = routerIpv4
                routerport["link"]["type"] = "router"
                routerport["link"]["sameNetwork"] = True
                routerport["state"] = "ESTABLISHED"

                break
            else:
                continue

    NWData[networkAD + ".0"].update(construction)
    f = open(f"network/config/{ipv4}.json", "x")
    f.writelines('{"table": {}}')
    f.close()
    with open(r"network\network.json", "w+") as c:
        c.write(json.dumps(NWData, indent=4))

    with open(rf"network\config\{ipv4}.json") as f:
        CFGData = json.load(f)

    for FIELD in NWData[networkAD + ".0"][ipv4]["ports"]["fields"]:
        if FIELD == "amount":
            continue
        elif FIELD == "[ROUTERPORT]":
            continue
        else:
            TempFieldConfig = {
                f"{FIELD}": {}
            }
            for layer in NWData[networkAD + ".0"][ipv4]["ports"]["fields"][f"{FIELD}"]["layers"]:
                if layer == "amount":
                    continue
                else:
                    TempLayerConfig = {
                        f"{layer}": {}
                    }
                    for port in NWData[networkAD + ".0"][ipv4]["ports"]["fields"][f"{FIELD}"]["layers"][layer]["LAN"]:
                        if port == "amount":
                            continue
                        else:
                            TempPortConfig = {
                                f"{port}": {
                                    "MAC": ""
                                }
                            }
                            TempLayerConfig[f"{layer}"].update(TempPortConfig)
                    TempFieldConfig[f"{FIELD}"].update(TempLayerConfig)
            CFGData["table"].update(TempFieldConfig)

            with open(rf"network\config\{DHCPServer}.json") as f:
                DHCPConfig = json.load(f)
            const = {
                "config": {
                        "firewall": {
                            "active": False,
                            "portForwarding": {}
                        },
                        "DNS-suffix": DHCPConfig["config"]["DNS-suffix"],
                        "host-name": deviceName,
                        "proxy-enabled": False,
                        "proxy": {
                            "proxy-server": ""
                        }
                }
            }
            CFGData.update(const)
            with open(rf"network\config\{ipv4}.json", "w+") as w:
                w.write(json.dumps(CFGData, indent=4))

def deleteVSwitch(networkAD: str, ipv4: str):
    with open(r"network\network.json") as f:
        NWData = json.load(f)
    networkAD = networkAD + ".0"
    try:
        if NWData[networkAD][ipv4]["type"] == "switch":
            for FIELD in NWData[networkAD][ipv4]["ports"]["fields"]:
                if FIELD == "amount":
                    continue
                elif FIELD == "[ROUTERPORT]":
                    continue
                else:
                    for layer in NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"]:
                        if layer == "amount":
                            continue
                        else:
                            for port in NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"]:
                                if port == "amount":
                                    continue
                                else:
                                    if NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"][port]["state"] == "ESTABLISHED":
                                        connectedIP = NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"][port]["link"]["ip"]

                                        for device in NWData[networkAD]:
                                            if device == connectedIP:
                                                if NWData[networkAD][device]["type"] == "switch":
                                                    for F in NWData[networkAD][device]["ports"]["fields"]:
                                                        if F == "amount":
                                                            continue
                                                        if F == "[ROUTERPORT]":
                                                            continue
                                                        else:
                                                            for L in NWData[networkAD][device]["ports"]["fields"][F]["layers"]:
                                                                if L == "amount":
                                                                    continue
                                                                else:
                                                                    for P in NWData[networkAD][device]["ports"]["fields"][F]["layers"][L]["LAN"]:
                                                                        if NWData[networkAD][device]["ports"]["fields"][F]["layers"][L]["LAN"][P]["link"]["ip"] == ipv4 and NWData[networkAD][device]["ports"]["fields"][F]["layers"][L]["LAN"][P]["state"] == "ESTABLISHED":
                                                                            NWData[networkAD][device]["ports"]["fields"][F]["layers"][L]["LAN"][P]["link"]["ip"] = ""
                                                                            NWData[networkAD][device]["ports"]["fields"][F]["layers"][L]["LAN"][P]["link"]["type"] = ""
                                                                            NWData[networkAD][device]["ports"]["fields"][F]["layers"][L]["LAN"][P]["state"] = "LISTENING"
                                                                            NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"][port]["link"]["ip"] = ""
                                                                            NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"][port]["link"]["type"] = ""
                                                                            NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"][port]["state"] = "LISTENING"
                                                elif NWData[networkAD][device]["type"] == "pc":
                                                    for port in NWData[networkAD][device]["ports"]["LAN"]:
                                                        if port == "amount":
                                                            continue
                                                        else:
                                                            if NWData[networkAD][device]["ports"]["LAN"][port]["state"] == "ESTABLISHED" and NWData[networkAD][device]["ports"]["LAN"][port]["link"]["ip"] == ipv4:
                                                                NWData[networkAD][device]["ports"]["LAN"][port]["link"]["ip"] = ""
                                                                NWData[networkAD][device]["ports"]["LAN"][port]["link"]["type"] = ""
                                                                NWData[networkAD][device]["ports"]["LAN"][port]["state"] = "LISTENING"
                                                                NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"][port]["link"]["ip"] = ""
                                                                NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"][port]["link"]["type"] = ""
                                                                NWData[networkAD][ipv4]["ports"]["fields"][FIELD]["layers"][layer]["LAN"][port]["state"] = "LISTENING"
                                                #elif NWData[networkAD][device]["type"] == "YOUR TYPE":

            routerIP = NWData[networkAD][ipv4]["ports"]["fields"]["[ROUTERPORT]"]["link"]["ip"]
            for port in NWData[networkAD][routerIP]["ports"]["LAN"]:
                if port == "amount":
                    continue
                else:
                    if NWData[networkAD][routerIP]["ports"]["LAN"][port]["link"]["ip"] == ipv4 and NWData[networkAD][routerIP]["ports"]["LAN"][port]["state"] == "ESTABLISHED":
                        NWData[networkAD][routerIP]["ports"]["LAN"][port]["link"]["ip"] = ""
                        NWData[networkAD][routerIP]["ports"]["LAN"][port]["link"]["type"] = ""
                        NWData[networkAD][routerIP]["ports"]["LAN"][port]["state"] = "LISTENING"
            del NWData[networkAD][ipv4]

            os.remove(f"network/config/{ipv4}.json")
            with open(r"network\network.json", "w+") as c:
                c.write(json.dumps(NWData, indent=4))
            return "No Error"
        else:
            return "This device is not a switch"
    except KeyError:
        return "Ipv4 doesn't exists"


def initSwitch(networkAD: str, ipv4: str):
    with open(r"network\network.json") as f:
        NWData = json.load(f)
    networkAD = networkAD + ".0"
    with open(rf"network\config\{ipv4}.json") as r:
        CFGData = json.load(r)

    for field in NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["fields"]:
        if field == "amount":
            continue
        elif field == "[ROUTERPORT]":
            continue
        else:
            for layer in NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["fields"][field]["layers"]:
                if layer == "amount":
                    continue
                else:
                    for port in NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["fields"][field]["layers"][layer]["LAN"]:
                        if port == "amount":
                            continue
                        else:
                            if NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["fields"][field]["layers"][layer]["LAN"][port]["state"] == "ESTABLISHED":
                                IPv4 = NWData[f"{networkAD}"][f"{ipv4}"]["ports"]["fields"][field]["layers"][layer]["LAN"][port]["link"]["ip"]

                                for device in NWData[networkAD]:
                                    if device == IPv4:
                                        MAC = NWData[networkAD][device]["mac"]

                                        CFGData["table"][field][layer][port]["MAC"] = MAC
                            else:
                                CFGData["table"][field][layer][port]["MAC"] = ""
    with open(rf"network\config\{ipv4}.json", "w+") as w:
        json.dump(CFGData, w, indent=4)
