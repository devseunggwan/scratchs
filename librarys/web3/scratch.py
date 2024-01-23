import web3
from web3 import Web3

rpc_url = 'https://rpc.ankr.com/polygon'
contract_addr = "0x473989bf6409d21f8a7fdd7133a40f9251cc1839"
abi = [
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_id",
                "type": "uint256"
            }
        ],
        "name": "totalSupply",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]


w3 = Web3(web3.HTTPProvider(rpc_url))

if __name__ == "__main__":
    contract_addr = Web3.to_checksum_address(contract_addr)

    __instance = w3.eth.contract(address=contract_addr, abi=abi)
    print(__instance.functions.totalSupply(1).call())

