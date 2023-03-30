# Python HTTP(s) proxy checker coded by zxcr9999
import argparse
import requests
import threading

alive_proxies = []

def check_proxy(ip, port):
    try:
        proxy = f'http://{ip}:{port}'
        response = requests.get('https://www.google.com', proxies={'http': proxy, 'https': proxy}, timeout=5)
        if response.status_code == 200:
            print(f'[ALIVE] {ip}:{port}')
            with open('alive_proxies.txt', 'a') as f:
                f.write(f'{ip}:{port}\n')
    except:
        print(f'[DEAD] {ip}:{port}')
parser = argparse.ArgumentParser(description='HTTP(s) Proxy checker')
parser.add_argument('proxy_file', help='Proxy file for checking')
parser.add_argument('--threads', type=int, default=10, help='Number threads using for checking proxy')
args = parser.parse_args()
with open(args.proxy_file, 'r') as f:
    proxies = [line.strip().split(':') for line in f]

num_threads = args.threads
proxy_parts = [proxies[i:i + len(proxies) // num_threads] for i in range(0, len(proxies), len(proxies) // num_threads)]

threads = []
for i in range(num_threads):
    thread = threading.Thread(target=lambda proxies: [check_proxy(ip, port) for ip, port in proxies], args=(proxy_parts[i],))
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()
