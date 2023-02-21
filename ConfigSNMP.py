from netmiko import ConnectHandler
import getpass

# Reads input from user for password
passwd = getpass.getpass('Please enter the password: ')    

devices = ['dev1', 'dev2' ]
device_list = list()

#Iterate through each device for site
for device_ip in devices:      
    device = {
        "device_type": "cisco_ios",
        "host": device_ip,
        "username": "name",   #Add username prior to running
        "password": passwd,   #Log in pass
        "secret": passwd      #Enable pass
    }
    device_list.append(device)

print(device_list)

#Iterate through device list
for each_device in device_list:       
    #Initial Connection  
    connection = ConnectHandler(**each_device)          
    commands = "snmp-server community ReadOnlyString RO"
    connection.enable()                 
    print(f'Connecting to {each_device["host"]}')
    #Send output from command to variable
    output = connection.send_config_set(commands)    
    output += connection.save_config()
    print(output)
    print(f'Closing Connection on {each_device["host"]}')
    #Close connection
    connection.disconnect()            