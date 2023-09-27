import os
import json
from dotenv import load_dotenv
from web3 import Web3

# Connect to Infura
load_dotenv()
infura_provider = Web3.HTTPProvider("https://optimism-mainnet.infura.io/v3/5422ebc991684c9ebc64ff6a1c5938dc")
w3 = Web3(infura_provider)

# Initialize contract
contract_address = "0xb27308f9F90D607463bb33eA1BeBb41C27CE5AB6"

with open('/Users/flora/PycharmProjects/pythonProject/Quoter.json', 'r') as quoter_abi_file:
    quoter_abi = json.load(quoter_abi_file)

contract = w3.eth.contract(address=contract_address, abi=quoter_abi)

# Encode the path for Uniswap v3
def encode_path(tokens, fee):
    path = tokens[0][2:]  # start with the first token, stripping off the "0x"
    for token in tokens[1:]:
        path += format(fee, '04x') + token[2:]
    return "0x" + path

WETH_ADDRESS = "0x4200000000000000000000000000000000000006"
wstETH_ADDRESS = "0x1F32b1c2345538c0c6f582fCB022739c4A194Ebb" 
FEE = 500  # for 0.05%

path_data = encode_path([WETH_ADDRESS, wstETH_ADDRESS], FEE)
print(f"Encoded Path: {path_data}")


def quoteExactInput(path, amountIn):
    print(f"Quoting Exact Input: path={path}, amountIn={amountIn}")
    # Encode the function call
    function_params = contract.encodeABI(
        fn_name="quoteExactInput",
        args=[path, amountIn]
    )

    print(f"Encoded function parameters: {function_params}")

    # Define the transaction parameters
    transaction = {
        "to": contract_address,
        "data": function_params,
    }
    print(f"Transaction parameters: {transaction}")

    # Use eth_call to retrieve the price
    price = w3.eth.call(transaction)

    # Decode the result to get the price
    price = contract.decode_function_result("quoteExactInput(bytes,uint256)", price)
    print(f"Decoded price result: {price}")

    # Print the price
    print(f"Price for {amountIn} Wei of WETH to wstETH: {price[1]} Wei of wstETH")

amount_in_data = 1000000000000000000

# Run the simulation
quoteExactInput(path_data, amount_in_data)
