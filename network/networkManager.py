import sys
import os
import io
import json
import random
import hashlib

with open(r"network\network.json") as f:
    NWData = json.load(f)

def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return random.randint(range_start, range_end)

def createNewNetwork(networkAD):
    construction = {
        networkAD + ".0": {

        }
    }

    NWData.update(construction)
    with open(r"network\network.json", "w+") as c:
        c.write(json.dumps(NWData, indent=4))


def createWiFiNetwork(routerIP: str, ssid: str, password: str, passwordProtected: bool = True):

    splittedIP = routerIP.split(".")
    networkAD = splittedIP[0] + "." + splittedIP[1] + "." + splittedIP[2]
    deviceAD = splittedIP[3]

    if routerIP in NWData[networkAD + ".0"]:
        NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"]["amount"] += 1
        networkCount = NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"]["amount"]

        if passwordProtected == False and password:
            return "DVNP-004 || Failed to set passwort because password-protected equals false."
    
        if passwordProtected == True:
            number = random_with_N_digits(32)
            salt = str(number).encode('utf-8')
            data = password.encode('utf-8')
            hash = hashlib.sha512(salt + data).hexdigest()

            construction = {
                f"[::]:{networkCount}": {
                    "ssid": ssid,
                    "passwordProtected": passwordProtected,
                    "password": {
                        "password": str(hash),
                        "hash": "sha256",
                        "salt": str(number),
                        "status": "PRESENT"
                    },
                    "clients": []
                }
            }
        else:
            construction = {
                f"[::]:{networkCount}": {
                    "ssid": ssid,
                    "passwordProtected": passwordProtected,
                    "password": {
                        "password": "",
                        "hash": "",
                        "salt": "",
                        "status": "MISSING"
                    },
                    "clients": []
                }
            }
        
        NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"].update(construction)
        with open(r"network\network.json", "w+") as c:
            c.write(json.dumps(NWData, indent=4))

    else:
        return "DVNP-003 || Failed to resolve routers IPAdress"

def deleteWiFiNetwork(routerIP: str, ssid: str, password: str):
    splittedIP = routerIP.split(".")
    networkAD = splittedIP[0] + "." + splittedIP[1] + "." + splittedIP[2]

    done = False

    if routerIP in NWData[networkAD + ".0"]:
        for x in NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"]:
            if x == "amount":
                continue
            else:
                if NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"][x]["ssid"] == ssid:
                    DBPassword = NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"][x]["password"]["password"]
                    DBSalt = NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"][x]["password"]["salt"]

                    salt = str(DBSalt).encode('utf-8')
                    data = password.encode('utf-8')
                    hash = hashlib.sha512(salt + data).hexdigest()

                    if hash == DBPassword:
                        del NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"][x]
                        NWData[networkAD + ".0"][routerIP]["WiFi"]["networks"]["amount"] -= 1

                        with open(r"network\network.json", "w+") as c:
                            c.write(json.dumps(NWData, indent=4))

                        done = True
                        break
                    else:
                        return "DVNP-005 || Password invalid"

        if done == True:
            return "WiFi " + ssid + " has been deleted successfully."
        else:
            return "DVNP-006 || WiFi " + ssid + " cannot be found."
        
def connectToWiFi(networkAD: str, WiFiName: str, IPv4ToConnect: str, WiFipassword: str = None):
    for device in NWData[networkAD + ".0"]:
        if NWData[networkAD + ".0"][device]["network-type"] == "WiFi":
                for WiFi in NWData[networkAD + ".0"][device]["WiFi"]["networks"]:
                    if WiFi == "amount":
                        continue
                    if NWData[networkAD + ".0"][device]["WiFi"]["networks"][WiFi]["ssid"] == WiFiName:

                        if NWData[networkAD + ".0"][device]["WiFi"]["networks"][WiFi]["password"]["status"] == "PRESENT":
                            passwordHash = NWData[networkAD + ".0"][device]["WiFi"]["networks"][WiFi]["password"]["password"]
                            salt = NWData[networkAD + ".0"][device]["WiFi"]["networks"][WiFi]["password"]["salt"].encode('utf-8')

                            data = WiFipassword.encode('utf-8')
                            hash = hashlib.sha512(salt + data).hexdigest()

                            if hash == passwordHash:
                                if IPv4ToConnect not in NWData[networkAD + ".0"][device]["WiFi"]["networks"][WiFi]["clients"]:
                                    NWData[networkAD + ".0"][device]["WiFi"]["networks"][WiFi]["clients"].append(IPv4ToConnect)

                                    with open(r"network\network.json", "w+") as c:
                                        c.write(json.dumps(NWData, indent=4))
                                    return None
                        else:
                            NWData[networkAD + ".0"][device]["WiFi"]["networks"][WiFi]["clients"].append(IPv4ToConnect)
                            with open(r"network\network.json", "w+") as c:
                                c.write(json.dumps(NWData, indent=4))
                            return None
