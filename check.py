from web3 import Web3
import threading

bsc_url = "https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc_url))

contract_address = "0x26f5f3b28ecbbbfe64167df7c7a3590f90c90af9"
contract_abi = [
    {
        "inputs": [
            {"internalType": "contract IERC20", "name": "_token", "type": "address"},
            {"internalType": "address payable", "name": "_initialOwner", "type": "address"},
        ],
        "stateMutability": "nonpayable",
        "type": "constructor",
    },
    {"inputs": [{"internalType": "address", "name": "target", "type": "address"}], "name": "AddressEmptyCode", "type": "error"},
    {"inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "AddressInsufficientBalance", "type": "error"},
    {"inputs": [], "name": "EnforcedPause", "type": "error"},
    {"inputs": [], "name": "ExpectedPause", "type": "error"},
    {"inputs": [], "name": "FailedInnerCall", "type": "error"},
    {"inputs": [{"internalType": "address", "name": "owner", "type": "address"}], "name": "OwnableInvalidOwner", "type": "error"},
    {"inputs": [{"internalType": "address", "name": "account", "type": "address"}], "name": "OwnableUnauthorizedAccount", "type": "error"},
    {"inputs": [{"internalType": "address", "name": "token", "type": "address"}], "name": "SafeERC20FailedOperation", "type": "error"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "recipient", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "CanClaim", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "recipient", "type": "address"}, {"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "HasClaimed", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": True, "internalType": "address", "name": "previousOwner", "type": "address"}, {"indexed": True, "internalType": "address", "name": "newOwner", "type": "address"}], "name": "OwnershipTransferred", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "address", "name": "account", "type": "address"}], "name": "Paused", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "uint256", "name": "amount", "type": "uint256"}], "name": "Swept", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "internalType": "address", "name": "account", "type": "address"}], "name": "Unpaused", "type": "event"},
    {"inputs": [], "name": "claim", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "", "type": "address"}], "name": "claimableTokens", "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "owner", "outputs": [{"internalType": "address", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "pause", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "paused", "outputs": [{"internalType": "bool", "name": "", "type": "bool"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "renounceOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [{"internalType": "address[]", "name": "_recipients", "type": "address[]"}, {"internalType": "uint256[]", "name": "_claimableAmount", "type": "uint256[]"}], "name": "setRecipients", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "sweep", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "sweepReceiver", "outputs": [{"internalType": "address payable", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [], "name": "token", "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}], "stateMutability": "view", "type": "function"},
    {"inputs": [{"internalType": "address", "name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [], "stateMutability": "nonpayable", "type": "function"},
    {"inputs": [], "name": "unpause", "outputs": [], "stateMutability": "nonpayable", "type": "function"}
]

contract = web3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=contract_abi)

def get_claimable_tokens(wallet):
    try:
        result = contract.functions.claimableTokens(web3.to_checksum_address(wallet)).call()
        if result != 0:
            print(f"{wallet}: {result/10**18}")
    except Exception as e:
        print("Error calling claimableTokens:", e)

list_address = []
with open("list_address.txt", 'r', encoding='UTF-8') as f:
    for line in f:
        if line.rstrip() != '':
            list_address.append(line.rstrip())
            
threads = []

for i in list_address:
    t = threading.Thread(target=get_claimable_tokens, args=(i,))
    threads.append(t)
    t.start()
    
for thread in threads:
    thread.join()
