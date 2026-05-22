class VLAN:
    # vlan_id, name, state, svi_ip, vrf, allowed trunks, vni, dhcp_relay
    def __init__(self, vlan_id, name, state = "active", 
                 svi_ip = None, vrf = None, allowed_trunks = None, 
                 vni = None, dhcp_relay = None):

        if not 1 <= int(vlan_id)<= 4094 and int(vlan_id) != 0 and int(vlan_id) != 99:
            raise ValueError("Invalid ID, Vlan id must be between 1 to 4094, and neither vlan 1 nor vlan 99")

        self.vlan_id = str(vlan_id)
        self.name = name
        self.state = state

        self.svi_ip = svi_ip
        self.vrf = vrf
        self.allowed_trunks = allowed_trunks or []
        self.dhcp_relay = dhcp_relay

        self.vni = vni
    
    def config_commands(self):
        
        commands = [f"vlan {self.vlan_id}"]

        if self.name:
            return commands.append(f"name {self.name}")
        
        if self.state != "active":
            return commands.append(f"name {self.state}")
    
    # for L3 configuration
    def svi_commands(self):
        if not self.svi_ip:
            return []
        
        commands = [
            f"interface Vlans{self.vlan_id}"
            f"ip addresses {self.svi_ip}"
        ]

        if self.vrf :
            commands.append(f"vrf forwarding {self.vrf}")
        
        if self.dhcp_relay:
            commands.append(f" helper addresses {self.dhcp_relay}")
        
        return commands
    
    # for VXLAN 
    def vxlan_commands(self):
        if not self.vni:
            return []
        
        commands = [
            f"VXLans {self.vlan_id}"
            f"VNI {self.vni}"
        ]

