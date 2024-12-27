import netmiko
import re
import traceback
import dns.resolver
import socket
from ipaddress import ip_network, IPv4Network
import time

def resolve_dns(hostname, dns_server):
    """
    Resolves a hostname using a custom DNS server.
    """
    try:
        resolver = dns.resolver.Resolver()
        resolver.nameservers = [dns_server]

        answers = resolver.resolve(hostname)
        ip_addresses = [ip.address for ip in answers]
        return ip_addresses

    except dns.resolver.NXDOMAIN:
        print(f"Error: Hostname '{hostname}' not found on DNS server {dns_server}.")
        return None
    except dns.resolver.Timeout:
        print(f"Error: DNS query timed out to server {dns_server}.")
        return None
    except socket.gaierror as e:
        print(f"Error: Invalid DNS server address: {dns_server}. {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None


def debuglogs(hostname, ipaddress, device_ip, username, password):
    """
    Connects to a Fortinet device and retrieves debug logs.
    """
    date = "date"
    try:
        device = netmiko.ConnectHandler(
            device_type='fortinet',
            ip=device_ip,
            username=username,
            password=password
        )

        # Send commands to the device
        device.send_command("execute log filter reset")
        device.send_command("execute log filter device 0")
        device.send_command("execute log filter category 0")
        device.send_command(f"execute log filter field dstip {ipaddress}")
        device.send_command("execute log filter field action deny")
        output = device.send_command("execute log display")
        print(output)
        if date in output:
            firewall_dns = device.send_command(f"diagnose firewall fqdn get-ip {hostname}")
            firewall_dns_ip = re.search(r"\bip: (\d+\.\d+\.\d+\.\d+)\b",firewall_dns)
            print(f"DNS resolution ip for {hostname} in firewall is {firewall_dns_ip.group(1)}")
            print(f"DNS resolution ip for {hostname} in the DNS server {dns_server} is {ip}")
            
        else:
            print(f"No logs found for IP: {ipaddress}")

        return output

    except netmiko.NetmikoBaseException as e:
        print(f"Error connecting to device {device_ip}: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()
    finally:
        try:
            device.disconnect()
        except Exception:
            pass

    return None


def read_credentials(file_path):
    """
    Reads username and password from a file.
    """
    try:
        with open(file_path, 'r') as file:
            username = file.readline().strip()
            password = file.readline().strip()
        return username, password
    except FileNotFoundError:
        print(f"Error: Credentials file '{file_path}' not found.")
        raise
    except Exception as e:
        print(f"Unexpected error reading credentials: {e}")
        raise


# Main script logic
firewall_ip = "192.168.1.1" # We need to modify the Fortinet firewall IP here
credentials_file = "credentials.txt"

# Read credentials
try:
    username, password = read_credentials(credentials_file)
except Exception:
    exit(1)

hostname = "meet.google.com" # We can modify the destination URL domain or FQDN here
dns_server = "8.8.8.8" # We can modify the DNS server ip here



# Loop indefinitely until interrupted
try:
    while True:
        print("\nResolving DNS and fetching logs...")

        resolved_ips = resolve_dns(hostname, dns_server)

        if resolved_ips:
            for ip in resolved_ips:
                print(f"Processing IP: {ip}")
                dns_debug = debuglogs(hostname, ip, firewall_ip, username, password)
        else:
            print("No IP addresses resolved.")

        # Wait for a while before the next iteration
        time.sleep(10)  # Adjust sleep time as needed (e.g., 5 seconds)

except KeyboardInterrupt:
    print("\nProcess interrupted by user. Exiting...")

