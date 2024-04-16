import os
from colorama import Fore
from datetime import datetime
from napalm import get_network_driver
from napalm.base.exceptions import ConnectionException
from netmiko.exceptions import NetmikoAuthenticationException, NetmikoTimeoutException

def str_date_time():
    now = datetime.now()
    str_date = now.strftime("%Y%m%d")
    str_time = now.strftime("%H%M%S")
    return "_" + str_date + "_" + str_time
if not os.path.exists("configs"):
    os.mkdir("configs")
if not os.path.exists("configs\\device_ip.txt"):
    file = open("configs\\device_ip.txt", 'w')
    print (Fore.RED + "Please add IP Addresses to configs\\device_ip.txt" + Fore.WHITE)
    file.close()
    exit()
with open ("configs\\device_ip.txt",'r') as f:
    devices_list = f.read().splitlines()
    f.close()
for ip_address in devices_list:
    Switch = { 
            "hostname": ip_address,
            "username": "username",
            "password": "password",
            "optional_args": {"secret": "password"} 
            }
    try:
        print(Fore.WHITE + f"{'=' * 50}\nConnecting to the Device {Switch['hostname']}")
        driver = get_network_driver('ios')
        Switch_Driver = driver(**Switch)
        Switch_Driver.open()
    except (ConnectionException):
        print(Fore.RED + f"Connecting Failed on {Switch['hostname']}" + Fore.WHITE)
    except (NetmikoAuthenticationException):
        print(Fore.RED + f"Authentication failed. {Switch['hostname']}" + Fore.WHITE)
    except:
        print(Fore.RED + f"Unknown Err!. {Switch['hostname']}" + Fore.WHITE)
    else:
        output_file_name = "configs\\" + Switch['hostname'] + "_" + str_date_time() + "_cfg.txt"
        with open ( output_file_name, 'w') as f:
            print (Fore.GREEN + "Connected....")
            print(Switch_Driver.get_config()['running'], file=f)
            print(Fore.GREEN + "Pass...." + Fore.WHITE)
            f.close()
            Switch_Driver.close()