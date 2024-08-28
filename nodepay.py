import asyncio
import requests
import json
import time
import uuid
from loguru import logger
import os
import sys
from itertools import cycle, islice

# Get the directory where the script is located
script_dir = os.path.dirname(os.path.abspath(__file__))

# Function to read a single line from a file
def read_single_line_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return f.read().strip()
    return None

# Function to read multiple lines from a file
def read_lines_file(file_path):
    with open(file_path, 'r') as f:
        return f.read().splitlines()

# Function to filter out empty lines
def filter_non_empty_lines(lines):
    return [line for line in lines if line.strip()]

# Read configuration values from files
NP_TOKEN = read_single_line_file(os.path.join(script_dir, 'token.txt'))
PROXY_LIST = filter_non_empty_lines(read_lines_file(os.path.join(script_dir, 'proxies.txt')))
ACCOUNTS_LIST = filter_non_empty_lines(read_lines_file(os.path.join(script_dir, 'accounts.txt')))

# Constants
HTTPS_URL = "https://nw3.nodepay.org/api/auth/session"
RETRY_INTERVAL = 60  # Retry interval for failed proxies (in seconds)
EXTENSION_VERSION = "2.2.3"

# Proxy pool with cyclic iteration
proxy_pool = cycle(PROXY_LIST)

# Get N proxies for an account
def get_proxies_for_account(num_proxies):
    return list(islice(proxy_pool, num_proxies))

async def call_api_info(token, proxy=None):
    logger.info("Fetching UserID")
    headers = {'Content-Type': 'application/json'}
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    proxies = {
        'http': proxy,
        'https': proxy
    } if proxy else None
    
    response = requests.post(
        "https://api.nodepay.ai/api/auth/session",
        headers=headers,
        json={},
        proxies=proxies
    )
    response.raise_for_status()
    return response.json()

async def send_ping(user_id, token, proxy=None):
    logger.info(f"Sending ping with proxy {proxy}")
    browser_id = str(uuid.uuid3(uuid.NAMESPACE_DNS, user_id))
    logger.info(browser_id)
    while True:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
                'Content-Type': 'application/json'
            }
            headers['Authorization'] = f'Bearer {token}'
            payload = {
                "user_id": user_id,
                "browser_id": browser_id,
                "timestamp": int(time.time()),
                "version": EXTENSION_VERSION
            }
            
            proxies = {
                'http': proxy,
                'https': proxy
            } if proxy else None
            
            response = requests.post(HTTPS_URL, headers=headers, json=payload, proxies=proxies)
            response.raise_for_status()
            logger.debug(response.json())
            await asyncio.sleep(10)  # Wait before the next action
        except Exception as e:
            logger.error(e)
            await asyncio.sleep(RETRY_INTERVAL)

async def process_account(account, proxies):
    tasks = []
    for proxy in proxies:
        tasks.append(send_ping(account['user_id'], NP_TOKEN, proxy=proxy))
    
    await asyncio.gather(*tasks)

async def main():
    if NP_TOKEN != "":
        # If the number of proxies is greater than the number of accounts, distribute proxies evenly among accounts
        proxies_per_account = max(1, len(PROXY_LIST) // len(ACCOUNTS_LIST))
        
        # Create tasks for all accounts
        tasks = []
        for account in ACCOUNTS_LIST:
            proxies = get_proxies_for_account(proxies_per_account)
            user_data = await call_api_info(NP_TOKEN, proxy=proxies[0])  # Get user_id using one of the proxies
            tasks.append(process_account(user_data, proxies))
        
        await asyncio.gather(*tasks)
    else:
        logger.error("NP_TOKEN must be specified in token.txt.")

if __name__ == '__main__':
    asyncio.run(main())
