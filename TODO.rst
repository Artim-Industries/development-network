if defaultDhcp == True:
        ipv4 = dhcp.dhcpGenerateIpv4(networkAD)
        mac = dhcp.dhcpGenerateMac(networkAD)
        ssid = deviceName
    construction = {
        f"{ipv4}": {
            "ip": f"{ipv4}",
            "mac": f"{mac}",
            "name": f"{deviceName}",
            "type": "router",
            "description": description,
            "DHCP-enabled": defaultDhcp,
            "DHCP": {
                "DHCP-server": f"{ipv4}",
            },
            "isDHCPServer": True,
            "ssid": f"{ssid}",
            "ports": ports,
            "is-Switch": isswitch,
        }
    }
    NWData[networkAD + ".0"].update(construction)
    with open(r"network\network.json", "w+") as c:
        c.write(json.dumps(NWData, indent=4))
    f = open(f"network/config/{ipv4}.json", "x")
    f.writelines("{}")
    f.close()
    defaultConfig = {
        "WiFi": wlan,
        "WiFi-Config": {
            "SSID": f"{ssid}",
            "version": 1,
            "name": f"{ssid}",
            "control-options": {
                "connection-mode": "connect manually",
            },
            "security": {
                "authentification": "WPA2-Personal",
                "security-key": "PRESENT",
                "key-content": ""
            }
        },
        "firewall": {
            "active": True,
            "wireless-forwards": {
                "ports": {
                },
                "devices": {
                }
            }
        },
        "DNS-suffix": f"{ssid}",
        "host-name": f"{deviceName}",
        "ip-routing-enabled": False,
        "proxy-enabled": False,
        "proxy": {
            "proxy-server": ""
        },
    }
    with open(f"network/config/{ipv4}.json") as f:
        data = json.load(f)
    data["config"] = defaultConfig
    with open(f"network/config/{ipv4}.json", "w+") as f:
        f.write(json.dumps(data, indent=4))