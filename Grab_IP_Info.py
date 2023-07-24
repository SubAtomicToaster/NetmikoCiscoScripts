import getpass
from pathlib import Path
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException

def get_device_info():
    """Grab user input and set device information for the connection"""
    username = input('Username: ')
    password = getpass.getpass() 
    devices = []
    try:
        #Try to open the file and grab the ip addresses in each line and create the specifc device to add to the empty list
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
    except FileNotFoundError as e:
        print(f"The file {file} was not found. Did you select the correct one?\n {str(e)}")
    return devices
            
def run_commands(devices):
    """Set the log file for the session and run commands against devices"""
    path = Path('run_log.txt')
    #Loop through the devices in the devices list
    for device in devices:
        #Set the connection to none so we can check later if it exists before attempting to disconnect
        connection = None
        try:
            #Begin the connection and write the hostname and output from the commands ran to the log file
            connection = ConnectHandler(**device)
            output = connection.send_command('sh ip int br')
            with path.open('a') as f:
                f.write(connection.find_prompt().rstrip("#").rstrip(">") + ' was succesfully queried\n')
                f.write(f"{output}\n")
        except NetMikoTimeoutException as e:
            #Append to the log file if the connection tp the current device times out
            with path.open('a') as f:
                f.write(f"Failed to connect to {device['ip']}: {str(e)}")
        except NetMikoAuthenticationException as e:
            #Append to the log file if authentication fails to the current device
            with path.open('a') as f:
                f.write(f"Failed to authenticate to {device['ip']}: {str(e)}")
        finally:
            #Test if the connection exists before disconnecting
            if connection:
                connection.disconnect()
        
if __name__ == '__main__':
    devices = get_device_info()
    run_commands(devices)
