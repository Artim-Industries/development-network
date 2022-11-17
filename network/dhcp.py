import sys
import os
import io
import json
import random
import datetime


conversion_table = {0: '0', 1: '1', 2: '2', 3: '3', 4: '4',
                    5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: 'A', 11: 'B', 12: 'C',
                    13: 'D', 14: 'E', 15: 'F'}


def decimalToHexadecimal(decimal):
    hexadecimal = ''
    while(decimal > 0):
        remainder = decimal % 16
        hexadecimal = conversion_table[remainder] + hexadecimal
        decimal = decimal // 16

    return hexadecimal


with open(r"network\network.json") as f:
    data = json.load(f)


def dhcpGenerateIpv4(networkAddress, expireDays: int = 10):
    NWAddressOld = networkAddress
    networkAddress = networkAddress + ".0"
    if data[networkAddress] != None:
        DHCP = ""

        for x in data[networkAddress]:
            if data[networkAddress][x]["isDHCPServer"] == True:
                DHCP = x
                DHCPServer = x
                startIP = data[networkAddress][DHCPServer]["DHCP-Server"]["IPRange"]["startIP"]
                endIP = data[networkAddress][DHCPServer]["DHCP-Server"]["IPRange"]["endIP"]

                startIPRange = int(startIP.split(".")[-1])
                endIPRange = int(endIP.split(".")[-1])

                IPAdressToCheck = random.randint(startIPRange, endIPRange)
                usedAdresses = []

                for y in data[networkAddress][DHCPServer]["DHCP-Server"]["clients"]:
                    usedAdresses.append(
                        data[networkAddress][DHCPServer]["DHCP-Server"]["clients"][y]["ip"])

                checkedIPAdress = str(NWAddressOld) + "." + str(IPAdressToCheck)
                if checkedIPAdress not in usedAdresses:
                    countClients = len(
                        data[networkAddress][DHCPServer]["DHCP-Server"]["clients"])
                    thisClient = countClients + 1

                    today = datetime.datetime.strptime(
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                    expireDate = today + datetime.timedelta(days=expireDays)

                    construction = {
                        f"[::]:{thisClient}": {
                            "ip": f"{checkedIPAdress}",
                            "expiring": str(expireDate)
                        }
                    }

                    data[networkAddress][DHCPServer]["DHCP-Server"]["clients"].update(
                        construction)
                    with open(r"network\network.json", "w+") as c:
                        c.write(json.dumps(data, indent=4))
                    return checkedIPAdress
                    
        for x in data[networkAddress][DHCP]["DHCP-Server"]["clients"]:
            expireDate = datetime.datetime.strptime(
                data[networkAddress][DHCP]["DHCP-Server"]["clients"][x]["expiring"], "%Y-%m-%d %H:%M:%S")
            safeDate = expireDate + datetime.timedelta(days=1)

            now = datetime.datetime.strptime(
                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
            if now > safeDate:
                IPAdress = data[networkAddress][DHCP]["DHCP-Server"]["clients"][x]["ip"]

                if IPAdress != DHCP:
                    del data[networkAddress][DHCP]["DHCP-Server"]["clients"][x]

                    countClients = len(
                        data[networkAddress][DHCPServer]["DHCP-Server"]["clients"])
                    thisClient = countClients + 1

                    today = datetime.datetime.strptime(
                        str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                    expireDate = today + datetime.timedelta(days=expireDays)

                    construction = {
                        f"[::]:{thisClient}": {
                            "ip": f"{IPAdress}",
                            "expiring": str(expireDate)
                        }
                    }

                    data[networkAddress][DHCPServer]["DHCP-Server"]["clients"].update(
                        construction)
                    with open(r"network\network.json", "w+") as c:
                        c.write(json.dumps(data, indent=4))

                    return IPAdress


def getDHCPServer(networkAdress):
    networkAddress = networkAdress + ".0"
    for x in data[networkAddress]:
        if data[networkAddress][x]["isDHCPServer"] == True:
            return x


def getIPv4FromExternalDHCPServer(networkAdress: str, DHCPServer: str, expireDays: int = 10):
    NWAddressOld = networkAddress
    networkAddress = networkAdress + ".0"
    if networkAddress in data:
        if data[networkAddress][DHCPServer]["isDHCPServer"] == True:
            startIP = data[networkAddress][DHCPServer]["DHCP-Server"]["IPRange"]["startIP"]
            endIP = data[networkAddress][DHCPServer]["DHCP-Server"]["IPRange"]["endIP"]

            startIPRange = int(startIP.split(".")[-1])
            endIPRange = int(endIP.split(".")[-1])

            IPAdressToCheck = random.randint(startIPRange, endIPRange)
            usedAdresses = []

            for y in data[networkAddress][DHCPServer]["DHCP-Server"]["clients"]:
                usedAdresses.append(data[networkAddress][DHCPServer]["DHCP-Server"]["clients"][y]["ip"])

            checkedIPAdress = str(NWAddressOld) + "." + str(IPAdressToCheck)
            if checkedIPAdress not in usedAdresses:
                countClients = len(data[networkAddress][DHCPServer]["DHCP-Server"]["clients"])
                thisClient = countClients + 1

                today = datetime.datetime.strptime(
                    str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                expireDate = today + datetime.timedelta(days=expireDays)

                constt = {
                    f"[::]:{thisClient}": {
                        "ip": f"{checkedIPAdress}",
                        "expiring": str(expireDate)
                    }
                }

                data[networkAddress][DHCPServer]["DHCP-Server"]["clients"].update(constt)
                with open(r"network\network.json", "w+") as c:
                    c.write(json.dumps(data, indent=4))
                return checkedIPAdress
            else:
                for x in data[networkAddress][DHCPServer]["DHCP-Server"]["clients"]:
                    expireDate = datetime.datetime.strptime(data[networkAddress][DHCPServer]["DHCP-Server"]["clients"][x]["expiring"], "%Y-%m-%d %H:%M:%S")
                    safeDate = expireDate + datetime.timedelta(days=1)

                    now = datetime.datetime.strptime(str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                    if now > safeDate:
                        IPAdress = data[networkAddress][DHCPServer]["DHCP-Server"]["clients"][x]["ip"]

                        if IPAdress != DHCPServer:
                            del data[networkAddress][DHCPServer]["DHCP-Server"]["clients"][x]

                            countClients = len(
                                data[networkAddress][DHCPServer]["DHCP-Server"]["clients"])
                            thisClient = countClients + 1

                            today = datetime.datetime.strptime(
                                str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "%Y-%m-%d %H:%M:%S")
                            expireDate = today + datetime.timedelta(days=expireDays)

                            construction = {
                                f"[::]:{thisClient}": {
                                    "ip": f"{IPAdress}",
                                    "expiring": str(expireDate)
                                }
                            }

                            data[networkAddress][DHCPServer]["DHCP-Server"]["clients"].update(construction)
                            with open(r"network\network.json", "w+") as c:
                                c.write(json.dumps(data, indent=4))

                            return IPAdress
        else:
            return f"DVNP-012 || {DHCPServer} is not a DHCP-Server."
    else:
        return "DVNP-002 || Cannot resolve Network-Adress."


def dhcpGenerateMac(networkAddress):
    NWAddressOld = networkAddress
    networkAddress = networkAddress + ".0"
    NAOne = int(networkAddress.split(".")[0])
    MacOne = decimalToHexadecimal(NAOne)
    NATwo = int(networkAddress.split(".")[1])
    MacTwo = decimalToHexadecimal(NATwo)
    NAThree = int(networkAddress.split(".")[2])
    MacThree = decimalToHexadecimal(NAThree)
    NWAmountDevices = 0
    for x in data[networkAddress]:
        NWAmountDevices += 1
    if NWAmountDevices == 0:
        MacFour = 0
    else:
        MacFour = decimalToHexadecimal(NWAmountDevices)
    try:
        if int(MacFour) < 9:
            MacFour = "0" + str(MacFour)
    except ValueError:
        if len(MacFour) == 1:
            MacFour = MacFour + "0"
    MacFive = decimalToHexadecimal(random.randint(0, 99))
    try:
        if int(MacFive) < 9:
            MacFive = "0" + MacFive
    except ValueError:
        if len(MacFive) == 1:
            MacFive = MacFive + "0"
    MacSix = decimalToHexadecimal(random.randint(0, 99))
    try:
        if int(MacSix) < 9:
            MacSix = "0" + MacSix
    except ValueError:
        if len(MacSix) == 1:
            MacSix = MacSix + "0"
    Mac = MacOne + "-" + MacTwo + "-" + MacThree + \
        "-" + MacFour + "-" + MacFive + "-" + MacSix
    macs = []
    for x in data[networkAddress]:
        mac = data[networkAddress][x]["mac"]
        macs.append(mac)
    if Mac in macs:
        dhcpGenerateMac(NWAddressOld)
    else:
        return Mac
