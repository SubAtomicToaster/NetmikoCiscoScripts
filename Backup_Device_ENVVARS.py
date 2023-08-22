import os
from datetime import date
import csv
from netmiko import ConnectHandler, NetmikoAuthenticationException, NetMikoTimeoutException

def get_device_ip():
    selected_csv = 'network_devices.csv'
    ip_addresses = []
    try:
        with open(selected_csv, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                ip_addresses.append(row['IP'])
    except FileNotFoundError:
        print(f'The file you selected "{selected_csv}" does not exist.')
    return ip_addresses

def set_device(address_list):
    username = os.environ.get('NETMIKO_USERNAME')
    password = os.environ.get('NETMIKO_PASSWORD')
    device_list = []
    for address in address_list:
            device = {
                'use_keys': False,
                'device_type': 'autodetect',
                'ip': address,
                'username': username,
                'password': password,
            }
            device_list.append(device)
    return device_list

def send_command(device_list):
    today = date.today()
    connection = None
    for device in device_list:
        try:
            connection = ConnectHandler(**device)
            hostname = connection.find_prompt().rstrip('#').rstrip('>')
            output = connection.send_command('show run')
            with open(f'{hostname}-{today}.txt', 'w') as file:
                file.write(output)
        except NetmikoAuthenticationException as e:
            with open('run_log.txt', 'a') as runfile:
                runfile.write(f'Authentication failed to {device["ip"]}\n {str(e)}\n')
        except NetMikoTimeoutException as e:
            with open('run_log.txt', 'a') as runfile:
                runfile.write(f'Connection failed to {device["ip"]}\n {str(e)}\n')
        finally:
            if connection:
                connection.disconnect()
            
if __name__ == '__main__':
    address_list = get_device_ip()
    device_list = set_device(address_list)
    send_command(device_list)
