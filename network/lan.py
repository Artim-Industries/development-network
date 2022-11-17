import sys
import json
import os

with open(r"network\network.json") as f:
    NWData = json.load(f)


def createVConnection(networkAD: str, ipv4Device1: str, ipv4Device2: str):

    networkPathDevice1 = NWData[networkAD + ".0"][ipv4Device1]
    networkPathDevice2 = NWData[networkAD + ".0"][ipv4Device2]

    typeDevice1 = networkPathDevice1["type"]
    typeDevice2 = networkPathDevice2["type"]

    countAvailablePortsDevice1 = 0
    countAvailablePortsDevice2 = 0

    # Check if already connected
    for PortConfig in networkPathDevice1["ports"]:
        if PortConfig == "fields":
            for field in networkPathDevice1["ports"]["fields"]:
                if field == "amount":
                    continue
                elif field == "[ROUTERPORT]":
                    continue
                else:
                    for layer in networkPathDevice1["ports"]["fields"][field]["layers"]:
                        if layer == "amount":
                            continue
                        else:
                            for port in networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"]:
                                if port == "amount":
                                    continue
                                else:
                                    portPath = networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"][port]

                                    if networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"][port]["link"]["ip"] == ipv4Device2:
                                        return "DVNP-013 || Device already connected"
                                    else:
                                        if portPath["state"] == "LISTENING":
                                            countAvailablePortsDevice1 += 1
                                        continue
        elif PortConfig == "layer":
            for layer in networkPathDevice1["ports"]["layer"]:
                if layer == "amount":
                    continue
                else:
                    for port in networkPathDevice1["ports"]["layer"][layer]["LAN"]:
                        if port == "amount":
                            continue
                        else:
                            portPath = networkPathDevice1["ports"]["layer"][layer]["LAN"][port]
                            if portPath == ipv4Device2:
                                return "DVNP-013 || Device already connected"
                            else:
                                if portPath["state"] == "LISTENING":
                                    countAvailablePortsDevice1 += 1
                                continue
        elif PortConfig == "LAN":
            for port in networkPathDevice1["ports"]["LAN"]:
                if port == "amount":
                    continue
                else:
                    if networkPathDevice1["ports"]["LAN"][port]["link"]["ip"] == ipv4Device2:
                        return "DVNP-013 || Device already connected"
                    else:
                        if networkPathDevice1["ports"]["LAN"][port]["state"] == "LISTENING":
                            countAvailablePortsDevice1 += 1
                        continue
    for PortConfig in networkPathDevice2["ports"]:
        if PortConfig == "fields":
            for field in networkPathDevice2["ports"]["fields"]:
                if field == "amount":
                    continue
                elif field == "[ROUTERPORT]":
                    continue
                else:
                    for layer in networkPathDevice2["ports"]["fields"][field]["layers"]:
                        if layer == "amount":
                            continue
                        else:
                            for port in networkPathDevice2["ports"]["fields"][field]["layers"][layer]["LAN"]:
                                if port == "amount":
                                    continue
                                else:
                                    portPath = networkPathDevice2["ports"]["fields"][field]["layers"][layer]["LAN"][port]

                                    if portPath == ipv4Device1:
                                        return "DVNP-013 || Device already connected"
                                    else:
                                        if portPath["state"] == "LISTENING":
                                            countAvailablePortsDevice2 += 1
                                        continue
        elif PortConfig == "layer":
            for layer in networkPathDevice2["ports"]["layer"]:
                if layer == "amount":
                    continue
                else:
                    for port in networkPathDevice2["ports"]["layer"][layer]["LAN"]:
                        if port == "amount":
                            continue
                        else:
                            portPath = networkPathDevice2["ports"]["layer"][layer]["LAN"][port]
                            if portPath == ipv4Device1:
                                return "DVNP-013 || Device already connected"
                            else:
                                if portPath["state"] == "LISTENING":
                                    countAvailablePortsDevice2 += 1
                                continue
        elif PortConfig == "LAN":
            for port in networkPathDevice2["ports"]["LAN"]:
                if port == "amount":
                    continue
                else:
                    if networkPathDevice2["ports"]["LAN"][port]["link"]["ip"] == ipv4Device1:
                        return "DVNP-013 || Device already connected"
                    else:
                        if networkPathDevice2["ports"]["LAN"][port]["state"] == "LISTENING":
                            countAvailablePortsDevice2 += 1
                        continue

    if countAvailablePortsDevice1 > 0 and countAvailablePortsDevice2 > 0:
        # Connect from device1 to device2
        for PortConfig in networkPathDevice1["ports"]:
            if PortConfig == "fields":
                for field in networkPathDevice1["ports"]["fields"]:
                    if field == "amount":
                        continue
                    elif field == "[ROUTERPORT]":
                        continue
                    else:
                        for layer in networkPathDevice1["ports"]["fields"][field]["layers"]:
                            if layer == "amount":
                                continue
                            else:
                                for port in networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"]:
                                    if port == "amount":
                                        continue
                                    else:
                                        portPath = networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"][port]
                                        if portPath["state"] == "LISTENING":
                                            portPath["link"]["ip"] = ipv4Device2
                                            portPath["link"]["type"] = typeDevice2
                                            portPath["state"] = "ESTABLISHED"
                                            portPath["link"]["sameNetwork"] = True

                                            break
                                break
                        break
                break
            elif PortConfig == "layer":
                for layer in networkPathDevice1["ports"]["layer"]:
                    if layer == "amount":
                        continue
                    else:
                        for port in networkPathDevice1["ports"]["layer"][layer]["LAN"]:
                            if port == "amount":
                                continue
                            else:
                                portPath = networkPathDevice1["ports"]["layer"][layer]["LAN"][port]

                                if portPath["state"] == "LISTENING":
                                    portPath["link"]["ip"] = ipv4Device2
                                    portPath["link"]["type"] = typeDevice2
                                    portPath["state"] = "ESTABLISHED"
                                    portPath["link"]["sameNetwork"] = True

                                    break
                                else:
                                    continue
            elif PortConfig == "LAN":
                for port in networkPathDevice1["ports"]["LAN"]:
                    if port == "amount":
                        continue
                    else:
                        if networkPathDevice1["ports"]["LAN"][port]["state"] == "LISTENING":
                            networkPathDevice1["ports"]["LAN"][port]["link"]["ip"] = ipv4Device2
                            networkPathDevice1["ports"]["LAN"][port]["link"]["type"] = typeDevice2
                            networkPathDevice1["ports"]["LAN"][port]["state"] = "ESTABLISHED"
                            networkPathDevice1["ports"]["LAN"][port]["link"]["sameNetwork"] = True

                            break
                        else:
                            continue
                break

        # Connect from device2 to device1
        for PortConfig in networkPathDevice2["ports"]:
            if PortConfig == "fields":
                for field in networkPathDevice2["ports"]["fields"]:
                    if field == "amount":
                        continue
                    elif field == "[ROUTERPORT]":
                        continue
                    else:
                        for layer in networkPathDevice2["ports"]["fields"][field]["layers"]:
                            if layer == "amount":
                                continue
                            else:
                                for port in networkPathDevice2["ports"]["fields"][field]["layers"][layer]["LAN"]:
                                    if port == "amount":
                                        continue
                                    else:
                                        portPath = networkPathDevice2["ports"]["fields"][field]["layers"][layer]["LAN"][port]
                                        if portPath["state"] == "LISTENING":
                                            portPath["link"]["ip"] = ipv4Device1
                                            portPath["link"]["type"] = typeDevice1
                                            portPath["state"] = "ESTABLISHED"
                                            portPath["link"]["sameNetwork"] = True

                                            break
                                break
                        break
                break
            elif PortConfig == "layer":
                for layer in networkPathDevice2["ports"]["layer"]:
                    if layer == "amount":
                        continue
                    else:
                        for port in networkPathDevice2["ports"]["layer"][layer]["LAN"]:
                            if port == "amount":
                                continue
                            else:
                                portPath = networkPathDevice2["ports"]["layer"][layer]["LAN"][port]
                                if portPath["state"] == "LISTENING":
                                    portPath["link"]["ip"] = ipv4Device1
                                    portPath["link"]["type"] = typeDevice1
                                    portPath["state"] = "ESTABLISHED"
                                    portPath["link"]["sameNetwork"] = True

                                    break
                                else:
                                    continue
            elif PortConfig == "LAN":
                for port in networkPathDevice2["ports"]["LAN"]:
                    if port == "amount":
                        continue
                    else:
                        if networkPathDevice2["ports"]["LAN"][port]["state"] == "LISTENING":
                            networkPathDevice2["ports"]["LAN"][port]["link"]["ip"] = ipv4Device1
                            networkPathDevice2["ports"]["LAN"][port]["link"]["type"] = typeDevice1
                            networkPathDevice2["ports"]["LAN"][port]["state"] = "ESTABLISHED"
                            networkPathDevice2["ports"]["LAN"][port]["link"]["sameNetwork"] = True

                            break
                        else:
                            continue
                break
        with open(r"network\network.json", "w+") as c:
            c.write(json.dumps(NWData, indent=4))
    else:
        return "DVNP-014 || No Ports available"


def deleteVConnection(networkAD: str, ipv4Device1: str, ipv4Device2: str):
    networkPathDevice1 = NWData[networkAD + ".0"][ipv4Device1]
    networkPathDevice2 = NWData[networkAD + ".0"][ipv4Device2]

    typeDevice1 = networkPathDevice1["type"]
    typeDevice2 = networkPathDevice2["type"]

    success = False
    initDevice1 = False
    initDevice2 = False

    # init connection 1
    for PortConfig in networkPathDevice1["ports"]:
        if PortConfig == "fields":
            for field in networkPathDevice1["ports"]["fields"]:
                if field == "amount":
                    continue
                elif field == "[ROUTERPORT]":
                    continue
                else:
                    for layer in networkPathDevice1["ports"]["fields"][field]["layers"]:
                        if layer == "amount":
                            continue
                        else:
                            for port in networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"]:
                                if port == "amount":
                                    continue
                                else:
                                    portPath = networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"][port]
                                    if portPath["state"] == "ESTABLISHED" and portPath["link"]["ip"] == ipv4Device2:
                                        initDevice1 = True

                                        break
                            break
                    break
            break
        elif PortConfig == "layer":
            for layer in networkPathDevice1["ports"]["layer"]:
                if layer == "amount":
                    continue
                else:
                    for port in networkPathDevice1["ports"]["layer"][layer]["LAN"]:
                        if port == "amount":
                            continue
                        else:
                            portPath = networkPathDevice1["ports"]["layer"][layer]["LAN"][port]
                            if portPath["state"] == "ESTABLISHED" and portPath["link"]["ip"] == ipv4Device2:
                                initDevice1 = True

                                break
                    break
            break
        elif PortConfig == "LAN":
            for port in networkPathDevice1["ports"]["LAN"]:
                if port == "amount":
                    continue
                else:
                    if networkPathDevice1["ports"]["LAN"][port]["state"] == "ESTABLISHED" and networkPathDevice1["ports"]["LAN"][port]["link"]["ip"] == ipv4Device2:
                        initDevice1 = True

                        break
                    else:
                        continue
            break

    # init connection 2
    for PortConfig in networkPathDevice2["ports"]:
        if PortConfig == "fields":
            for field in networkPathDevice2["ports"]["fields"]:
                if field == "amount":
                    continue
                elif field == "[ROUTERPORT]":
                    continue
                else:
                    for layer in networkPathDevice2["ports"]["fields"][field]["layers"]:
                        if layer == "amount":
                            continue
                        else:
                            for port in networkPathDevice2["ports"]["fields"][field]["layers"][layer]["LAN"]:
                                if port == "amount":
                                    continue
                                else:
                                    portPath = networkPathDevice2["ports"]["fields"][field]["layers"][layer]["LAN"][port]
                                    if portPath["state"] == "ESTABLISHED" and portPath["link"]["ip"] == ipv4Device1:
                                        initDevice2 = True

                                        break
                            break
                    break
            break
        elif PortConfig == "layer":
            for layer in networkPathDevice2["ports"]["layer"]:
                if layer == "amount":
                    continue
                else:
                    for port in networkPathDevice2["ports"]["layer"][layer]["LAN"]:
                        if port == "amount":
                            continue
                        else:
                            portPath = networkPathDevice2["ports"]["layer"][layer]["LAN"][port]
                            if portPath["state"] == "ESTABLISHED" and portPath["link"]["ip"] == ipv4Device1:
                                initDevice2 = True

                                break
                    break
            break
        elif PortConfig == "LAN":
            for port in networkPathDevice2["ports"]["LAN"]:
                if port == "amount":
                    continue
                else:
                    if networkPathDevice2["ports"]["LAN"][port]["state"] == "ESTABLISHED" and networkPathDevice2["ports"]["LAN"][port]["link"]["ip"] == ipv4Device1:
                        initDevice2 = True

                        break
                    else:
                        continue
            break

    if initDevice1 == True and initDevice2 == True:
        # remove connection from device1 to device2
        for PortConfig in networkPathDevice1["ports"]:
            if PortConfig == "fields":
                for field in networkPathDevice1["ports"]["fields"]:
                    if field == "amount":
                        continue
                    elif field == "[ROUTERPORT]":
                        continue
                    else:
                        for layer in networkPathDevice1["ports"]["fields"][field]["layers"]:
                            if layer == "amount":
                                continue
                            else:
                                for port in networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"]:
                                    if port == "amount":
                                        continue
                                    else:
                                        portPath = networkPathDevice1["ports"]["fields"][field]["layers"][layer]["LAN"][port]
                                        if portPath["state"] == "ESTABLISHED" and portPath["link"]["ip"] == ipv4Device2:
                                            portPath["link"]["ip"] = ""
                                            portPath["link"]["type"] = ""
                                            portPath["state"] = "LISTENING"
                                            portPath["link"]["sameNetwork"] = True
                                            success = True

                                            break
                                break
                        break
                break
            elif PortConfig == "layer":
                for layer in networkPathDevice1["ports"]["layer"]:
                    if layer == "amount":
                        continue
                    else:
                        for port in networkPathDevice1["ports"]["layer"][layer]["LAN"]:
                            if port == "amount":
                                continue
                            else:
                                portPath = networkPathDevice1["ports"]["layer"][layer]["LAN"][port]
                                if portPath["state"] == "ESTABLISHED" and portPath["link"]["ip"] == ipv4Device2:
                                    portPath["link"]["ip"] = ""
                                    portPath["link"]["type"] = ""
                                    portPath["state"] = "LISTENING"
                                    portPath["link"]["sameNetwork"] = True
                                    success = True

                                    break
                        break
                break
            elif PortConfig == "LAN":
                for port in networkPathDevice1["ports"]["LAN"]:
                    if port == "amount":
                        continue
                    else:
                        if networkPathDevice1["ports"]["LAN"][port]["state"] == "ESTABLISHED" and networkPathDevice1["ports"]["LAN"][port]["link"]["ip"] == ipv4Device2:
                            networkPathDevice1["ports"]["LAN"][port]["link"]["ip"] = ""
                            networkPathDevice1["ports"]["LAN"][port]["link"]["type"] = ""
                            networkPathDevice1["ports"]["LAN"][port]["state"] = "LISTENING"
                            networkPathDevice1["ports"]["LAN"][port]["link"]["sameNetwork"] = True
                            success = True

                            break
                        else:
                            continue
                break

        # remove connection from device2 to device1
        for PortConfig in networkPathDevice2["ports"]:
            if PortConfig == "fields":
                for field in networkPathDevice2["ports"]["fields"]:
                    if field == "amount":
                        continue
                    elif field == "[ROUTERPORT]":
                        continue
                    else:
                        for layer in networkPathDevice2["ports"]["fields"][field]["layers"]:
                            if layer == "amount":
                                continue
                            else:
                                for port in networkPathDevice2["ports"]["fields"][field]["layers"][layer]["LAN"]:
                                    if port == "amount":
                                        continue
                                    else:
                                        portPath = networkPathDevice2["ports"]["fields"][field]["layers"][layer]["LAN"][port]
                                        if portPath["state"] == "ESTABLISHED" and portPath["link"]["ip"] == ipv4Device1:
                                            portPath["link"]["ip"] = ""
                                            portPath["link"]["type"] = ""
                                            portPath["state"] = "LISTENING"
                                            portPath["link"]["sameNetwork"] = True
                                            success = True

                                            break
                                break
                        break
                break
            elif PortConfig == "layer":
                for layer in networkPathDevice2["ports"]["layer"]:
                    if layer == "amount":
                        continue
                    else:
                        for port in networkPathDevice2["ports"]["layer"][layer]["LAN"]:
                            if port == "amount":
                                continue
                            else:
                                portPath = networkPathDevice2["ports"]["layer"][layer]["LAN"][port]
                                if portPath["state"] == "ESTABLISHED" and portPath["link"]["ip"] == ipv4Device1:
                                    portPath["link"]["ip"] = ""
                                    portPath["link"]["type"] = ""
                                    portPath["state"] = "LISTENING"
                                    portPath["link"]["sameNetwork"] = True
                                    success = True

                                    break
                        break
                break
            elif PortConfig == "LAN":
                for port in networkPathDevice2["ports"]["LAN"]:
                    if port == "amount":
                        continue
                    else:
                        if networkPathDevice2["ports"]["LAN"][port]["state"] == "ESTABLISHED" and networkPathDevice2["ports"]["LAN"][port]["link"]["ip"] == ipv4Device1:
                            networkPathDevice2["ports"]["LAN"][port]["link"]["ip"] = ""
                            networkPathDevice2["ports"]["LAN"][port]["link"]["type"] = ""
                            networkPathDevice2["ports"]["LAN"][port]["state"] = "LISTENING"
                            networkPathDevice2["ports"]["LAN"][port]["link"]["sameNetwork"] = True
                            success = True

                            break
                        else:
                            continue
                break
    else:
        return "DNNP-015 || Connection not found (if you're trying to remove the connection from a switch to a router, use deleteRouterConnection)"
    if success == True:
        with open(r"network\network.json", "w+") as c:
            c.write(json.dumps(NWData, indent=4))
    else:
        return "DVNP-015 || Connection not found"


def deleteRouterConnection(networkAD: str, routerIPv4: str, deviceWithRouterPortIPv4: str):
    if networkAD + ".0" not in NWData:
        return "DVNP-002 || Cannot resolve Network-Adress."

    try:
        routerPath = NWData[networkAD + ".0"][routerIPv4]
        DevicePath = NWData[networkAD + ".0"][deviceWithRouterPortIPv4]
    except KeyError:
        return "DVNP-008 || Failed to resolve IP-Adress"

    for port in routerPath["ports"]["LAN"]:
        if port == "amount":
            continue
        else:
            portPath = routerPath["ports"]["LAN"][port]

            if portPath["link"]["ip"] == deviceWithRouterPortIPv4 and portPath["state"] == "ESTABLISHED":
                portPath["link"]["ip"] = ""
                portPath["link"]["type"] = ""
                portPath["state"] = "LISTENING"

    routerportPath = DevicePath["ports"]["fields"]["[ROUTERPORT]"]
    if routerportPath["link"]["ip"] == routerIPv4 and routerportPath["state"] == "ESTABLISHED":
        routerportPath["link"]["ip"] = ""
        routerportPath["link"]["type"] = ""
        routerportPath["state"] = "LISTENING"

    else:
        return "DVNP-015 || Connection not found"

    with open(r"network\network.json", "w+") as c:
        c.write(json.dumps(NWData, indent=4))
