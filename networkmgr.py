import sys
import network
import json

cmd = "python networkmgr.py --create --arguments '{\"type\": \"network\", \"networkAD\": \"77.77.77.77\"}'"

routerPortConfig = {
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

def checkIfKeyExists(dictorary: dict, key: str):
    try:
        if dictorary[key]:
            return dictorary[key]
        else:
            return None
    except:
        return None

try:
    if sys.argv[1]:
        mode = sys.argv[1]

        if mode == "--create":
            if sys.argv[2] == "--arguments":
                obj = u'' + sys.argv[3] + ''
                arguments = json.loads(obj)

                creationType = arguments['type']

                if creationType == "network":
                    networkAD = arguments["networkAD"]
                    print(f"Create Network with {networkAD}")

                elif creationType == "router":
                    networkAD = arguments["networkAD"]
                    deviceName = arguments["deviceName"]
                    deviceDescription = checkIfKeyExists(arguments, "deviceDescription")
                    networkType = checkIfKeyExists(arguments, "networkType")
                    if (networkType == None):
                        networkType = "WiFi"
                    DHCPEnabled = checkIfKeyExists(arguments, "DHCPEnabled")
                    if (DHCPEnabled == None):
                        DHCPEnabled = True
                    isDHCPServer = checkIfKeyExists(arguments, "isDHCPServer")
                    if (isDHCPServer == None):
                        isDHCPServer = True
                    DHCPServer = checkIfKeyExists(arguments, "DHCPServer")
                    if (DHCPServer == None):
                        DHCPServer = "localhost"
                    portConfig = checkIfKeyExists(arguments, "portConfig")
                    if (portConfig == None):
                        portConfig = routerPortConfig
                    startIP = checkIfKeyExists(arguments, "startIP")
                    if (startIP == None):
                        startIP = ".1"
                    endIP = checkIfKeyExists(arguments, "endIP")
                    if (endIP == None):
                        endIP = ".255"
                    overwrite = checkIfKeyExists(arguments, "overwrite")
                    if (overwrite == None):
                        overwrite = False
                    print(f"Create Router " + deviceName)

                print(arguments)
        

    else:
        print("HELP")
except Exception as e:
    print(e)