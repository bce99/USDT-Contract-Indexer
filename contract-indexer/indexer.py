# Import packages
from web3 import Web3
from prometheus_client import Gauge, start_http_server
from api_key import API_KEY
import json
import time

# Connect to Ethereum Mainnet using Alchemy API
eth_url = f'https://eth-mainnet.g.alchemy.com/v2/{API_KEY}'

w3 = Web3(Web3.HTTPProvider(eth_url))

# Check connection status 
if w3.is_connected():
    print("Connected to Ethereum Mainnet")
else:
    print("Connection Failed")

usdt_contract_address = Web3.to_checksum_address('0xdac17f958d2ee523a2206206994597c13d831ec7')

# Load contract abi
with open('contract_abi.json', 'r') as abi_file:
    usdt_contract_abi = json.load(abi_file)

contract = w3.eth.contract(address=usdt_contract_address, abi=usdt_contract_abi)

# Create filters for Transfer and Approval events 
transfer_filter = contract.events.Transfer.create_filter(from_block='latest')
approval_filter = contract.events.Approval.create_filter(from_block='latest')

# Initialize Prometheus metrics
tx_per_second = Gauge('tx_per_second', 'Number of transactions per second')
token_transferred = Gauge('token_transferred_per_second', 'Amount of tokens transferred per second')
approvals_per_second = Gauge('approvals_per_second', 'Number of approvals per second')
approval_amount_metric = Gauge('approval_amount_metric', 'Total amount of tokens approved')

# Start Prometheus metrics server
start_http_server(8000)

def handle_event(event):
    if event.event == 'Transfer':
        tx_per_second.inc()  # Increment transactions per second
        token_amount = event.args.value / 1e6  # Assuming value is in smallest unit, convert to tokens
        token_transferred.inc(token_amount)  # Increment tokens transferred

    elif event.event == 'Approval':
        approvals_per_second.inc()  # Increment number of approvals per second
        approval_amount = event.args.value / 1e6  # Assuming value is in smallest unit, convert to tokens
        approval_amount_metric.inc(approval_amount) # total approval amount

# Event processing loop
while True:
    for event in transfer_filter.get_new_entries():
        handle_event(event)
    for event in approval_filter.get_new_entries():
        handle_event(event)
    time.sleep(1)  # Poll every second