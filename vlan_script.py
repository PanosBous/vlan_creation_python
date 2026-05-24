import json
import yaml

from vlan import VLAN
from switch import Switch
    
def main():
    #VLANS which i create
    # vlans = {
    #     VLAN(2, "management"),
    #     VLAN(3, "data"),
    #     VLAN(4, "active_directory"),
    #     VLAN(5, "administrators"),
    #     #infrastructure
    #     VLAN(10, "servers"),
    #     VLAN(11, "storage"),
    #     VLAN(12, "back-up"),
    #     VLAN(13, "monitoring"),
    #     #user access
    #     VLAN(20, "users"),
    #     VLAN(21, "engineering"),
    #     VLAN(22, "finance"),
    #     VLAN(23, "hr"),
    #     VLAN(24, "sales"),
    #     # voice wireless
    #     VLAN(30, "voice"),
    #     VLAN(31, "guest_wifi"),
    #     VLAN(32, "wireless"),
    #     VLAN(33, "iot"),
    #     #security
    #     VLAN(40, "access control"),
    #     VLAN(41, "security cameras"),
    #     VLAN(42, "printers"),
    #     #network service
    #     VLAN(70, "DNS"),
    #     VLAN(71, "DHCP"),
    #     VLAN(72, "NTP"),
    #     VLAN(90, "parking_lot", "suspend")
    # }

    # or uncomment the upper vlans !!!!
    vlans = get_vlans_from_user()

    # There are 5 predefined arista switches in a json file
    # open switches file
    with open('switches.json') as f:
        data = json.load(f)

    # build the objects
    switches = []
    for sw in data["switches"]:
        switches.append(
            Switch(
                host = sw["host"],
                username = sw["username"],
                password = sw["password"],
                secret = sw["secret"],
                device_type = sw["device_type"]
            )
        )
    

    # alternative way with Switches in YAML file
    # def load_switches():
    #     with open('switches.yaml', "r") as s:
    #         data = yaml.safe_load(s)
    
    #     switches = []
    #     for sw in data["Switches"]:
    #         switches.append(Switch(**sw))

    #     return switches

    # in case you want to store switches in a yaml file
    # uncomment the line 
    # switches = load_switches()


    # connect to switches
    for switch in switches:

        #try to connect
        try:
            switch.connect()
            current_vlans = switch.get_vlans()

            for vlan in vlans:
                
                vlan_exists = vlan.vlan_id in current_vlans

                vlan_name_matches = (
                    vlan_exists and
                    current_vlans[vlan.vlan_id] == vlan.name
                )

                if not vlan_exists or not vlan_name_matches:

                    print(f"Configuring vlan {vlan.vlan_id}")

                    output = switch.configure_vlans(vlan)
                    print(output)

                else:
                    # vlan does not exist
                    print(f"Vlan {vlan.vlan_id} already configured")
            
            print(f"Disconnecting from {switch['host']}")
            switch.disconnect()
                
        except Exception as e:
            print(f"Failed to connect to {switch['host']}")
            print(e)

# or uncomment the hardcoded Vlans from above
def get_vlans_from_user():
    vlans = []

    # here creates a loop
    while True:
        vlan_id = input("Enter Vlan id or q to quit: ")
        
        if (1 <= int(vlan_id)<= 4094 and int(vlan_id) != 0 and int(vlan_id) != 99):
            vlan_id = input("Please enter a valid Vlan between 1 - 4094 and not 0 or 99")
        
            if vlan_id.lower() == 'q':
                break

        vlan_name = input("Enter a vlan name: ")

        vlan_state = input("Enter the state of vlan: active or passive ? ")

        if vlan_state == "active":
            vlan_state = "active"
        else:
            vlan_state = "passive"        
        
        vlans.append(VLAN(vlan_id, vlan_name, vlan_state))

    
    return vlans


if __name__ == "__main__":
    main()
