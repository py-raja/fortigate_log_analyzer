# Fortinet Debug Logs Retrieval Tool

This script is designed to resolve DNS queries using a specified DNS server and retrieve debug logs from a Fortinet firewall device. It continuously monitors and fetches logs for a specified hostname and its resolved IP addresses.

---

## Features

- Resolves hostnames using a custom DNS server.
- Connects to a Fortinet firewall device to retrieve debug logs.
- Filters logs based on destination IP and specific criteria (e.g., action `deny`).
- Provides detailed error handling for DNS resolution and firewall connection issues.
- Runs in an infinite loop until interrupted.

---

## Prerequisites

1. **Python Environment:** Ensure you have Python 3.x installed.
2. **Required Libraries:** Install the following Python libraries:
   - `netmiko`
   - `dnspython`
3. **Firewall Access:** Valid credentials and IP address for the Fortinet firewall.
4. **DNS Server:** Accessible DNS server for hostname resolution.
5. **Credentials File:** A file named `credentials.txt` containing the firewall username and password, each on a separate line.

---

## Setup and Usage

### 1. Clone the Repository
```bash
git clone https://github.com/py-raja/fortigate_log_analyzer.git
cd fortinet-debug-logs
```

### 2. Install Required Libraries
```bash
pip install netmiko dnspython
```

### 3. Create a Credentials File
Create a file named `credentials.txt` in the same directory as the script. Add the username and password for the Fortinet firewall, each on a new line:

```
<firewall-username>
<firewall-password>
```

### 4. Update Script Variables
Edit the script to configure the following variables:
- `firewall_ip`: IP address of the Fortinet firewall.
- `hostname`: The hostname to resolve (e.g., `meet.google.com`).
- `dns_server`: The DNS server to use for hostname resolution.

### 5. Run the Script
```bash
python script_name.py
```

### 6. Interrupt the Script
To stop the script, press `Ctrl+C`.

---

## Script Details

### Functions

1. **`resolve_dns(hostname, dns_server)`**
   Resolves a hostname using the specified DNS server.

2. **`debuglogs(hostname, ipaddress, device_ip, username, password)`**
   Connects to the Fortinet firewall and retrieves debug logs based on the specified criteria.

3. **`read_credentials(file_path)`**
   Reads the username and password from a specified file.

### Workflow

1. Resolves the IP addresses of the hostname using the specified DNS server.
2. Iterates through the resolved IPs and retrieves relevant logs from the Fortinet firewall.
3. Prints the logs or error messages as appropriate.
4. Repeats the process at regular intervals until interrupted.

---

## Error Handling

- **DNS Resolution Errors:**
  - Handles `NXDOMAIN`, timeouts, and invalid DNS server addresses.

- **Firewall Connection Errors:**
  - Catches `NetmikoBaseException` for device connection issues.

- **General Exceptions:**
  - Logs unexpected errors with stack traces for debugging.

---

## Notes

- Adjust the sleep time (`time.sleep(10)`) as needed to balance monitoring frequency and system load.
- Ensure the Fortinet firewall's SSH access is enabled and reachable from the system running the script.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

---

## Contributing

Contributions are welcome! Feel free to fork this repository, make changes, and submit a pull request.

---


