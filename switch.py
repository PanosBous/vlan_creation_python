from netmiko import ConnectHandler

device_type = ["arista_eos", "cisco_ios"]

class Switch:
    def __init__(self, host, username, password, secret, device_type):
        self.host = host
        self.username = username
        self.password = password
        self.secret = secret
        # i want to do it and for the cisco devices 
        self.device_type = device_type
    
    # function to connect
    def connect(self):
        
        print(f"\n Connecting to {self.host}")

        self.Connection = ConnectHandler(
            device_type = self.device_type,
            host = self.host,
            username = self.username,
            password = self.password,
            secret = self.secret
        )
        self.Connection.enable()

    # function to dissconnect
    def disconnect(self):
        if self.connect:
            print("Disconnecting from {self.host}")
            self.Connection.disconnect()

    def get_vlans(self):

        output = self.Connection.send_command(
            "Show vlans",
            use_textfsm= True
        )

        vlan_dict = {}

        for vlan in output:
            vlan_dict[vlan['vlan id']] = vlan['name']
        
        return vlan_dict

    def configure_vlans(self, VLAN):
        commands = VLAN.config_commands()
        output = self.Connection.send_config_set(commands)
        return(output)
    
    # L3 and VXLAN
    def apply_vlans(self, vlan):
        commands = []

        commands += vlan.svi_commands()
        commands += vlan.vxlan_commands()
        