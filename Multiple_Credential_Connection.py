import csv
import getpass
from netmiko import ConnectHandler, NetmikoTimeoutException, NetmikoAuthenticationException

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
        if cont == 'N' or 'n':
            break
    return credentials_list

def get_ipaddresses(selected_site): 
    """Create a list of ip addresses from a CSV file that the user selects"""   
    ip_addresses = []
    with open(f"{selected_site}_devices.csv", "r") as csvfile:
        csv_reader = csv.DictReader(csvfile)
        for row in csv_reader:
            ip_addresses.append(row["IP Address"])
    return ip_addresses

def test_credential_connection(device, credentials_list):
    """Test the credentials from the list against the device and return the connection if the credential succeeds"""
    connection = None
    for credential in credentials_list:
        device.update(credential)
        try:
            connection = ConnectHandler(**device)
            return connection
        except NetmikoAuthenticationException as e:
            with open('run_log.txt', 'a') as runfile:
                runfile.write(f"The credentials entered failed to connect to {device['ip']} \n {str(e)}")
            continue
        except NetmikoTimeoutException as e:
            with open('run_log.txt' 'a') as runfile:
                runfile.write(f"The device at {device['ip']} is either offline or was unable to be reached \n {str(e)}")
            continue
    return None

def perform_work(ip_list, credentials_list):
    """Loop through the IP list and then create the device, define the connection and send commands on"""
    for ip in ip_list:
        device = {
            "device_type": "autodetect",
            "ip": ip,
            "username": "",
            "password": "",
        }
        connection = test_credential_connection(device, credentials_list)
        if connection:
            print(f"Connected to {device['ip']}")
            try:
                output = connection.send_command("sh ip int br")
                with open("success_log.txt", "a") as runfile:
                    runfile.write(f"{output} \n")
            except ValueError as e:
                print(f"Failed to enter configuration mode on {ip}: {str(e)}")
            finally:
                connection.disconnect()

if __name__ == '__main__':
    selected_csv = input("What site are you attempting to connect to? ")
    ip_list = get_ipaddresses(selected_csv)
    credential_list = get_credentials()
    perform_work(ip_list, credential_list)
