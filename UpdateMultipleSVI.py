from netmiko import ConnectHandler
import getpass

# Reads input from user for password
passwd = getpass.getpass('Please enter the password: ') 


# Define the device connection parameters
devices_list = ['dev1']
device_list = list()


for device_ip in devices_list:      #Iterate through each device for site
    device = {
        "device_type": "cisco_ios",
        "host": device_ip,
        "username": "name",   #Add username prior to running
        "password": passwd,   #Log in pass
        "secret": passwd      #Enable pass
    }
    device_list.append(device)

print(device_list)


# Connect to the device
for each_device in device_list:
    with ConnectHandler(**each_device) as conn:
        conn.enable()
        # Define the IP helper address
        ip_helper = "IP_AddressOfDHCPSrv"
        # Define the list of SVIs to update
        svis = ["Vlan101", "Vlan102", "Vlan103", "Vlan104", "Vlan105", "Vlan106", "Vlan107", "Vlan108", "Vlan109", "Vlan110", "Vlan111", "Vlan112", "Vlan113", "Vlan114", "Vlan115", "Vlan116", "Vlan117", "Vlan118", "Vlan119", "Vlan120", "Vlan134", "Vlan135", "Vlan136", "Vlan137", "Vlan138", "Vlan139", "Vlan140", "Vlan141", "Vlan142", "Vlan143", "Vlan144", "Vlan145", "Vlan146", "Vlan147", "Vlan148", "Vlan149", "Vlan150", "Vlan151", "Vlan152", "Vlan153", "Vlan154", "Vlan155"]
        # Loop through the list of SVIs and update the IP helper address
        for svi in svis:
            cmd = [f"interface {svi}",
                   f"ip helper-address {ip_helper}"]
            output = conn.send_config_set(cmd)
            print(output)
        conn.save_config()
        conn.disconnect()