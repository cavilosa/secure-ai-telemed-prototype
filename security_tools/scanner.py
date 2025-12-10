# '''
# This module is dedicated to a port scanning script that is used in cyber security for as a fundamental
# defensive network management tool and an offensive penetration testing one.
# It is crucial for discovering vulnerabilities, verifying security policies, and responding to incidents.
# The tool is build on Nmap Python library.
# '''


# '''
# Port Scanning in Cybersecurity

# Cybersecurity professionals use port scanner scripts as a fundamental tool for defensive network management and offensive penetration testing. They are crucial for discovering vulnerabilities, verifying security policies, and responding to incidents, using tools like Nmap.
# Real-Life Applications
# Vulnerability Assessment: Security analysts run port scans to identify unnecessary open ports that could serve as potential entry points for attackers. They then work to close these ports or apply necessary security patches to services running on them before malicious actors can exploit them.
# Network Inventory and Mapping: Port scanners help administrators create an up-to-date inventory of all active hosts and the services (e.g., web servers on port 80/443, SSH on port 22) running on the network. This ensures that all devices and applications comply with security policies and no unauthorized services are running.
# Firewall Rule Verification: Professionals use port scans to test the effectiveness of firewalls and security policies. By scanning from outside the perimeter, they verify that only intended ports are accessible and that unauthorized access attempts are blocked or properly filtered.
# Penetration Testing: Ethical hackers use port scanning in the initial "reconnaissance" phase of a controlled attack to understand the target's attack surface. The information gathered (open ports, operating system fingerprinting, service versions) informs subsequent, more targeted testing phases to identify misconfigurations or outdated software vulnerabilities.
# Incident Response: During a security incident, port scans can help the response team quickly assess the status of compromised systems and identify any unusual open ports or services that might be linked to the attacker's activity or malware persistence.
# Troubleshooting Connectivity Issues: Network administrators use port scanners to diagnose connectivity problems, determining whether a service is running and listening on a specific port or if communication is being blocked by a firewall or network outage.
# Common Tools and Techniques
# Cybersecurity professionals primarily use the robust and scriptable Nmap (Network Mapper) tool for these tasks, leveraging various techniques.
# SYN Scans (Half-Open): These are faster and stealthier than a full connection scan as they do not complete the TCP handshake, making them less likely to be logged by the target system.
# Service/Version Detection (-sV): Nmap scripts are used to determine the exact application and version of the service running on an open port, which helps in identifying specific, known vulnerabilities (CVEs).
# OS Detection (-O): By analyzing responses to specific packets, Nmap can often determine the operating system of the target host, which aids in tailoring further assessments.
# Scripting Engine (NSE): The Nmap Scripting Engine (NSE) allows professionals to write or use existing scripts for more advanced tasks like vulnerability detection, all integrated within the scanning process.
# By using these scripts, professionals adopt a proactive approach to find and secure network weaknesses before they can be exploited by malicious actors.
# '''

# '''
# CS network mapping and port scanning tool
# Port scanners: types, techniques, tools and how to use them
# How to prevent port scanning attacks
# Common port scanning commands and their usage
# Advanced port scanner for network security professionals
# Nmap Python library documentation: https://nmap.org/book/py-nmap-manual.html
# '''

# '''Building a security tool requires structure, reliability, and safety. Since you are building this for **Cybersecurity** (Defensive/Offensive), your code structure needs to handle **input validation** (to prevent errors or self-injection) and **profiles** (different scan types for different scenarios).

# Here is a breakdown of how to apply Python's OOP concepts specifically to a Port Scanner, along with hints on implementation.

# ### 1\. The `@classmethod`: The "Scan Profile" Factory

# In cybersecurity, you rarely just "run a scan." You run specific *types* of scans based on the Rules of Engagement (ROE) or the situation (stealth vs. noise).

# Instead of remembering complex Nmap flags (`-sS -T4 -p-` vs `-sV -O`), use `@classmethod` as **Factory Methods** to create pre-configured scanners.

#   * **Hint:** Create methods that return an instance of your class with specific arguments pre-loaded.
#   * **Use Cases:**
#       * `PortScanner.stealth()`: Returns an instance configured with SYN scan (`-sS`) and slower timing (`-T2`) to avoid firewall detection.
#       * `PortScanner.aggressive()`: Returns an instance configured with version detection, OS detection, and scripts (`-A`).
#       * `PortScanner.compliance_check()`: Returns an instance configured to only check specific ports (e.g., 22, 80, 443) required by company policy.

# ### 2\. The `@staticmethod`: The "Sanitizer" & "Helper"

# Security tools must be robust. If a user inputs a bad IP or a malformed CIDR block, your tool should catch it *before* passing it to Nmap. Since this logic doesn't depend on the scanner's state, it belongs in a static method.

#   * **Hint:** Use Python's built-in `ipaddress` library inside these methods.
#   * **Use Cases:**
#       * `validate_target(ip_string)`: Checks if the input is a valid IPv4/IPv6 address or CIDR block.
#       * `is_root()`: Nmap SYN scans (Stealth) require root/admin privileges. Use a static method to check `os.geteuid()` before the class is even instantiated for a stealth scan.
#       * `parse_nmap_xml(xml_content)`: If you need to process raw XML logs from a previous scan, this function doesn't need a live scanner instance.

# ### 3\. The `@property`: The "Data Refiner"

# Nmap returns data in complex nested dictionaries (JSON-like). Accessing `scan_result['scan']['192.168.1.1']['tcp'][80]['state']` is messy and prone to crashing if a key is missing.

# Use `@property` to create safe, clean "getters" for your data.

#   * **Hint:** Encapsulate the raw `self.scan_result` dictionary.
#   * **Use Cases:**
#       * `@property open_ports`: Returns a clean list of just the open ports, filtering out the "closed" or "filtered" ones automatically.
#       * `@property os_guess`: Safely digs through the Nmap dictionary to find the OS with the highest accuracy probability and returns just that string (e.g., "Linux 5.x").

# ### 4\. Instance Methods: The "Operator"

# These are your standard methods that do the actual work using the specific configuration of the object.

#   * **Use Cases:**
#       * `run()`: Executes the scan.
#       * `export_to_json()`: Saves the specific results of *this* scan instance to a file.
#       * `compare_with(other_scanner_instance)`: For "Diffing." Compare the results of a scan you did today vs. one you did last week to find new open ports (a critical task in Incident Response).

# -----

# ### Other Approaches to Consider

# #### A. The Context Manager (`__enter__` and `__exit__`)

# You mentioned "Defensive Network Management." If your script connects to a database to log results, or opens file handles to write large reports, you should use Context Managers. This allows you to use the `with` keyword.

#   * **Concept:**
#     ```python
#     with PortScanner('192.168.1.1') as scanner:
#         scanner.run()
#     # Cleanup (closing files/DB connections) happens automatically here
#     ```

# #### B. Asynchronous Scanning (`asyncio`)

# Nmap can be slow. If you are scanning a whole subnet (Network Inventory), doing it linearly (one by one) takes forever.

#   * **Hint:** Look into `asyncio`. While the standard `python-nmap` is synchronous, you can wrap it or use libraries that support async to trigger multiple scans at once.

# ### Recommended Resources (Hints & Documentation)

# 1.  **Input Validation:**

#       * **Library:** [Python `ipaddress` module](https://www.google.com/search?q=%5Bhttps://docs.python.org/3/library/ipaddress.html%5D\(https://docs.python.org/3/library/ipaddress.html\)) (Standard library, crucial for security tools).
#       * **Concept:** "Input Sanitization" (Preventing Command Injection).

# 2.  **The Library:**

#       * **Docs:** [python-nmap](https://pypi.org/project/python-nmap/) (The wrapper you are likely using).
#       * *Tip:* Look closely at the `PortScannerAsync` class in this library if you want speed.

# 3.  **Security Context:**

#       * **Concept:** [OS Fingerprinting techniques](https://nmap.org/book/osdetect.html) (Understanding *how* Nmap identifies OS helps you write better parsers).
#       * **Concept:** [Bypassing Firewalls](https://nmap.org/book/man-bypass-firewalls-ids.html) (Understanding fragmentation and timing options will help you build your "Stealth" `classmethod`).

# 4.  **Design Patterns:**

#       * **Pattern:** [Factory Method Pattern](https://refactoring.guru/design-patterns/factory-method) (This is the formal name for the `@classmethod` strategy discussed above).

# By using these methods, you aren't just writing a script; you are building a **framework** that can be extended safely. Good luck with the build\!'''

import nmap
import logging
import argparse
import json
import ipaddress
import os
from datetime import datetime
from pathlib import Path

class NetworkScanner:
    def __init__(self, target, arguments):
        self.target = target
        self.arguments = arguments
        try:
            self.scanner = nmap.PortScanner()
        except nmap.PortScannerError:
            logging.error("Nmap not found, please install it")
            print("Nmap not found, please install it")
            raise Exception("Nmap not found")
        self.scan_result = {}      

    def run(self):
        """Instance method to run the scan"""
        logging.info(f"Running scan on {self.target}")
        self.scan_result = self.scanner.scan(self.target, arguments=self.arguments)
        logging.info(f"Scan completed on {self.target} with the results: {self.scan_result}")

    def export_to_json(self, filename, scan_type='manual'):
        """Instance method to export scan results to JSON"""
        directory = f'logs/{scan_type}'
        # Define the path for the directory and the JSON file
        output_dir = Path(directory)
        output_file_path = output_dir / filename
        # Create the directory if it doesn't exist
        output_dir.mkdir(parents=True, exist_ok=True)
        with open(output_file_path, "w") as f:
            json.dump(self.scan_result, f, indent=4)
        logging.info(f"Scan results exported to {filename}")

    def compare_with(self):
        """Instance method to compare scan results with another scanner instance"""
        # approved_baseline.json - to check for server drift from approved state
        try:
            return {
                "new_open_ports": self._new_open_ports,
                "new_closed_ports": self._new_closed_ports,
                "service_versions_changed": self._service_versions_changed,
                "os_changes": self._os_changes
            }
        except Exception as e: 
            logging.error(f"Error comparing scan results: {e}")
            raise e
    
    def _new_open_ports(self):
        """Property to get a list of newly opened ports compared to a baseline scan"""
        # Placeholder for actual implementation
        return []
    
    def _new_closed_ports(self):
        """Property to get a list of newly closed ports compared to a baseline scan"""
        # Placeholder for actual implementation
        return []
    
    def _service_versions_changed(self):
        """Property to get a list of services with changed versions compared to a baseline scan"""
        # Placeholder for actual implementation
        return []
    
    def _os_changes(self):
        """Property to get a list of OS changes compared to a baseline scan"""
        # Placeholder for actual implementation
        return []
     

    @classmethod
    def deep_audit(cls, target):
        # -sV: Get versions
        # -O: Get OS
        # -p-: Check EVERY port (takes longer)
        # --open: Clean output
        arguments = "-sV -O -p- --open"
        return cls(target, arguments)

    @classmethod
    def stealth(cls, target):
        """Factory method for stealth scan profile"""
        logging.info(f"Creating stealth scan profile for {target}")
        if cls.is_root(): # Check for root/admin privileges required for stealth scan
            return cls(target, arguments="-sS -T2")
        else:
            logging.error("Root privileges are required for stealth scan profile.")
            raise PermissionError("Root privileges are required for stealth scan profile.")            

    @classmethod
    def agressive(cls, target):
        """Factory method for aggressive scan profile"""
        logging.info(f"Creating aggressive scan profile for {target}")
        return cls(target, arguments="-A -T4")

    @staticmethod
    def validate_target(ip_string):
        """Static method to validate IP address or CIDR block"""
        try:
            ipaddress.ip_network(ip_string, strict=False)
            return True
        except ValueError:
            logging.error(f"Invalid IP address or CIDR block: {ip_string}")
            raise ValueError(f"Invalid IP address or CIDR block: {ip_string}")

    @staticmethod
    def parse_nmap_xml(xml_content):
        """Static method to parse Nmap XML output"""
        scanner = nmap.PortScanner()
        scanner.analyse_nmap_xml_scan(xml_content)
        return scanner.scaninfo()

    @staticmethod
    def is_root():
        """Static method to check for root/admin privileges"""
        import ctypes
        # Try to check both Windows and Unix-like systems for admin rights priovielges
        # Windows admin check = ctypes.windll.shell32.IsUserAnAdmin() != 0
        # Unix-like admin check = os.geteuid() == 0
        admin = False
        if os.name == 'nt' and ctypes.windll.shell32.IsUserAnAdmin() != 0:
            admin = True
        if os.name != 'nt' and os.geteuid() == 0:
            admin = True
        if not admin:
            return False
        return admin

    @property
    def open_ports(self):
        """Property to get a list of open ports"""
        open_ports = []
        for host in self.scan_result.get("scan", {}):
            host_data = self.scan_result["scan"].get(host, {})
            all_protocols = host_data.keys()
            protocols = [proto for proto in all_protocols if proto in ["tcp", "udp", "icmp"]]
            for proto in protocols:
                for port in self.scan_result["scan"][host][proto]:
                    if self.scan_result["scan"][host][proto][port]["state"] == "open":
                        open_ports.append((host, port, proto))
            
        return open_ports


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    parser = argparse.ArgumentParser(description="Network Scanner Tool")

    parser.add_argument("target", help="Target IP address or CIDR block to scan")

    parser.add_argument(
        "--profile",
        choices=["stealth", "aggressive"],
        default="stealth",
        help="Scan profile to use",
    )

    now = datetime.now().strftime("%Y%m%d_%H%M%S")
    parser.add_argument(
        "--output", default=f"scan_{now}.json", help="Output file for scan results"
    )

    parser.add_argument("--diff", help="Compare with previous scan result")

    parser.add_argument("--test_mode", action="store_true", help="Run in test mode with mock data")

    args = parser.parse_args()

    if not NetworkScanner.validate_target(args.target):
        print("Invalid target IP address or CIDR block.")
        raise ValueError("Invalid target IP address or CIDR block.")
    
    if args.test_mode:
        scanner = NetworkScanner(target=args.target, arguments="-sT")

    if args.profile == "stealth":
        try:
            scanner = NetworkScanner.stealth(args.target)
        except PermissionError:
            logging.error("Exiting due to insufficient privileges for stealth scan.")
            print("Stealth scan requires root/admin privileges. Please run the script with elevated permissions.")
        except Exception:
            print("Error: That doesn't look like a valid IP address.")
    else:
        scanner = NetworkScanner.agressive(args.target)

    scanner.run()
    scanner.export_to_json(args.output)
