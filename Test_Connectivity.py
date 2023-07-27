import getpass
import csv
from netmiko import ConnectHandler, NetMikoAuthenticationException, NetMikoTimeoutException

def get_credentials():
    """Loop until the user defines they entered enough credentials to try and then append to a list"""
    keep_looping = True
    credentials_list = [] 
    while keep_looping:
        username = input("Enter the username to use for the connection: ")
        password = getpass.getpass("What password will be used? ")
        credentials_list.append({
            'username': username,
            'password': password,
        })
        cont = input("Want to add another? Y/N ")
        if cont == 'N' or cont =='n':
            break
    return credentials_list

def get_ipaddresses():
  """Grab the IPs in the CSV and add them to the ip_list"""
    ip_list = []
    with open('wan_routers.csv', 'r') as csvfile:
        csvreader = csv.DictReader(csvfile)
        for row in csvreader:
            ip_list.append(row['IP Address'])
    return ip_list

def test_credentials(device, credentials):
  """Loop through the credentials in the credentials list and attempt to connect to each device with a set, if the set works, move forward"""
    connection = None
    for credential in credentials:
        device.update(credential)
        try:
            connection = ConnectHandler(**device)
            return connection
        except NetMikoAuthenticationException as e:
            with open('run_log.txt', 'a') as file:
                file.write(f'Authentication failed to {device["ip"]}. \n {str(e)}')
            continue
        except NetMikoTimeoutException as e:
            with open('run_log.txt', 'a') as file:
                file.write(f'Connecting to {device["ip"]} failed. \n {str(e)}')
            continue
    return None

def test_wan(credentials, ip_list):
  """Create a reverse list of the original and then if the connection earlier succeeds, ping the ips in the reverse list."""
    ping_list = ip_list.copy()
    ping_list.reverse()
    for ip in ip_list:
        device = {
            'device_type': 'autodetect',
            'ip': ip,
            'username': '',
            'password': ''
        }
        connection = test_credentials(device, credentials)
        if connection:
            try:
                hostname = connection.find_prompt().strip('#>')
                for address in ping_list:
                    data = connection.send_command_timing(f'ping {address}', last_read=8.0)
                    with open(f'{hostname}_wan_test.txt', 'a') as file:
                        file.write(f"Pinging from {hostname} to {address}.\n {data}\n")
            except ValueError as e:
                with open('run_log.txt', 'a') as file:
                    file.write('An error occurred when attempting the test.')
            finally:
                connection.disconnect()

if __name__ == '__main__':
    credentials = get_credentials()
    ip_list = get_ipaddresses()
    test_wan(credentials, ip_list)
