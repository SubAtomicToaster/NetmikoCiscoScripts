import getpass
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException

devices = []
username = input('Username: ')
password = getpass.getpass()

with open('switches.txt') as file:
    for line in file:
        ip = line.strip()
        device = {
            'device_type': 'cisco_ios',
            'ip': ip,
            'username': username,
            'password': password,
        }
        devices.append(device)
        
for device in devices:
    try:
        connection = ConnectHandler(**device)
        output = connection.send_command('sh ip int br')
        print(output)
    except NetMikoTimeoutException as e:
        print('Failed to connect to ', device['ip'], ': ', str(e))
    except NetMikoAuthenticationException as e:
        print('Failed to authenticate to:', device['ip'], ': ', str(e))
    finally:
        connection.disconnect()
