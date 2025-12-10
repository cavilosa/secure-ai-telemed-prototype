## Security Tools

### Network Scanner

This is a great project. Building a security tool requires structure, reliability, and safety. Since you are building this for **Cybersecurity** (Defensive/Offensive), your code structure needs to handle **input validation** (to prevent errors or self-injection) and **profiles** (different scan types for different scenarios).

Here is a breakdown of how to apply Python's OOP concepts specifically to a Port Scanner, along with hints on implementation.

### 1\. The `@classmethod`: The "Scan Profile" Factory

In cybersecurity, you rarely just "run a scan." You run specific *types* of scans based on the Rules of Engagement (ROE) or the situation (stealth vs. noise).

Instead of remembering complex Nmap flags (`-sS -T4 -p-` vs `-sV -O`), use `@classmethod` as **Factory Methods** to create pre-configured scanners.

  * **Hint:** Create methods that return an instance of your class with specific arguments pre-loaded.
  * **Use Cases:**
      * `PortScanner.stealth()`: Returns an instance configured with SYN scan (`-sS`) and slower timing (`-T2`) to avoid firewall detection.
      * `PortScanner.aggressive()`: Returns an instance configured with version detection, OS detection, and scripts (`-A`).
      * `PortScanner.compliance_check()`: Returns an instance configured to only check specific ports (e.g., 22, 80, 443) required by company policy.

### 2\. The `@staticmethod`: The "Sanitizer" & "Helper"

Security tools must be robust. If a user inputs a bad IP or a malformed CIDR block, your tool should catch it *before* passing it to Nmap. Since this logic doesn't depend on the scanner's state, it belongs in a static method.

  * **Hint:** Use Python's built-in `ipaddress` library inside these methods.
  * **Use Cases:**
      * `validate_target(ip_string)`: Checks if the input is a valid IPv4/IPv6 address or CIDR block.
      * `is_root()`: Nmap SYN scans (Stealth) require root/admin privileges. Use a static method to check `os.geteuid()` before the class is even instantiated for a stealth scan.
      * `parse_nmap_xml(xml_content)`: If you need to process raw XML logs from a previous scan, this function doesn't need a live scanner instance.

### 3\. The `@property`: The "Data Refiner"

Nmap returns data in complex nested dictionaries (JSON-like). Accessing `scan_result['scan']['192.168.1.1']['tcp'][80]['state']` is messy and prone to crashing if a key is missing.

Use `@property` to create safe, clean "getters" for your data.

  * **Hint:** Encapsulate the raw `self.scan_result` dictionary.
  * **Use Cases:**
      * `@property open_ports`: Returns a clean list of just the open ports, filtering out the "closed" or "filtered" ones automatically.
      * `@property os_guess`: Safely digs through the Nmap dictionary to find the OS with the highest accuracy probability and returns just that string (e.g., "Linux 5.x").

### 4\. Instance Methods: The "Operator"

These are your standard methods that do the actual work using the specific configuration of the object.

  * **Use Cases:**
      * `run()`: Executes the scan.
      * `export_to_json()`: Saves the specific results of *this* scan instance to a file.
      * `compare_with(other_scanner_instance)`: For "Diffing." Compare the results of a scan you did today vs. one you did last week to find new open ports (a critical task in Incident Response).

-----

### Other Approaches to Consider

#### A. The Context Manager (`__enter__` and `__exit__`)

You mentioned "Defensive Network Management." If your script connects to a database to log results, or opens file handles to write large reports, you should use Context Managers. This allows you to use the `with` keyword.

  * **Concept:**
    ```python
    with PortScanner('192.168.1.1') as scanner:
        scanner.run()
    # Cleanup (closing files/DB connections) happens automatically here
    ```

#### B. Asynchronous Scanning (`asyncio`)

Nmap can be slow. If you are scanning a whole subnet (Network Inventory), doing it linearly (one by one) takes forever.

  * **Hint:** Look into `asyncio`. While the standard `python-nmap` is synchronous, you can wrap it or use libraries that support async to trigger multiple scans at once.

### Recommended Resources (Hints & Documentation)

1.  **Input Validation:**

      * **Library:** [Python `ipaddress` module](https://www.google.com/search?q=%5Bhttps://docs.python.org/3/library/ipaddress.html%5D\(https://docs.python.org/3/library/ipaddress.html\)) (Standard library, crucial for security tools).
      * **Concept:** "Input Sanitization" (Preventing Command Injection).

2.  **The Library:**

      * **Docs:** [python-nmap](https://pypi.org/project/python-nmap/) (The wrapper you are likely using).
      * *Tip:* Look closely at the `PortScannerAsync` class in this library if you want speed.

3.  **Security Context:**

      * **Concept:** [OS Fingerprinting techniques](https://nmap.org/book/osdetect.html) (Understanding *how* Nmap identifies OS helps you write better parsers).
      * **Concept:** [Bypassing Firewalls](https://nmap.org/book/man-bypass-firewalls-ids.html) (Understanding fragmentation and timing options will help you build your "Stealth" `classmethod`).

4.  **Design Patterns:**

      * **Pattern:** [Factory Method Pattern](https://refactoring.guru/design-patterns/factory-method) (This is the formal name for the `@classmethod` strategy discussed above).

By using these methods, you aren't just writing a script; you are building a **framework** that can be extended safely. Good luck with the build\!

That is the million-dollar question. Writing the script is Step 1. Integrating it into a workflow is Step 2 (and that is where the real value is).

In the professional world (especially in places like Grande Prairie or Fort St. John where teams are small), these scripts are used in **two distinct ways**.

### 1\. Manual Mode: "The Troubleshooter / Pentester"

*Who uses it:* You, the SysAdmin, or the Penetration Tester.
*When:* Ad-hoc. When something breaks, or when you are auditing a specific new server.

**Scenario:** A developer tells you, "I just deployed the new patient database."
**Action:** You open your terminal and run your script manually to verify they didn't accidentally open dangerous ports.

```bash
# You run this in your CLI
python scanner.py 192.168.1.50 --profile aggressive
```

**Why script it instead of just using Nmap?**
Because you don't want to remember the complex Nmap flags every time. Your script enforces **Consistency**. It ensures every scan is done exactly the same way, with the same safety checks.

-----

### 2\. Automated Mode: "The Watchdog" (This is your goal)

*Who uses it:* The Server (Cron / CI Pipeline / SOAR).
*When:* Every night at 3:00 AM, or every time code is committed.

This is where your **JSON output** becomes critical. Computers don't read console text; they read JSON.

**Scenario:** You want to know if anyone secretly plugs in a rogue server or opens a firewall port without asking.

**The Workflow:**

1.  **Schedule:** A `cron` job (Linux scheduler) runs your script every night.
2.  **Output:** The script saves `scan_results_2025-12-09.json`.
3.  **Diffing (The "Blue Team" Magic):** Another tiny script compares `today.json` vs `yesterday.json`.
4.  **Alerting:** If there is a difference (e.g., Port 22 was closed yesterday, but open today), it sends a Slack message or email.

### Practical Example: Setting up the "Watchdog"

You can simulate this "Enterprise Automation" right now on your machine (WSL or Linux).

**Step 1: The Wrapper Script (`nightly_scan.sh`)**
You create a simple shell script that runs your Python tool.

```bash
#!/bin/bash
# automated_scan.sh

DATE=$(date +%Y-%m-%d)
TARGET="192.168.1.1"
OUTPUT_DIR="./logs"

# 1. Run your Python tool
python3 security_tools/scanner_oop.py --target $TARGET --save "$OUTPUT_DIR/scan_$DATE.json"

# 2. (Optional) Simple "Diff" Check
# Compare today's output with yesterday's to see if anything changed
diff "$OUTPUT_DIR/scan_$DATE.json" "$OUTPUT_DIR/scan_yesterday.json" > "$OUTPUT_DIR/changes.txt"

# 3. If changes found, alert (Simulated with echo)
if [ -s "$OUTPUT_DIR/changes.txt" ]; then
    echo "ALERT: Network changes detected!"
    # In real life: python send_email.py "Alert"
fi
```

**Step 2: The Schedule (Cron)**
You add this to the Linux scheduler.

```bash
# Open crontab
crontab -e

# Add this line to run every day at 3:00 AM
0 3 * * * /home/user/projects/secure-ai/automated_scan.sh
```

### Why this impresses employers in Grande Prairie:

If you tell an employer: *"I write scripts that run manually,"* they think **"Junior."**
If you tell them: *"I write scripts that run automatically every night, compare the logs, and email me if a firewall port accidentally opens,"* they think **"Senior / Automation Engineer."**

This approach turns your project from a "tool" into a **"System."**

