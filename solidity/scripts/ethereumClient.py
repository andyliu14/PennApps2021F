import sys
import time
import pprint

from web3.providers.eth_tester import EthereumTesterProvider
from web3 import Web3
from eth_tester import PyEVMBackend
from solcx import compile_source
from eth_account import Account
import secrets



class ethereumClient:
    def __init__(self, connectionString):
        self.w3 = Web3(connectionString)

    def compile_source_file(self, file_path):
        with open(file_path, 'r') as f:
            source = f.read()

        return compile_source(source)


    def deploy_contract(self, w3, contract_interface):
        passStr = "pass".encode('utf-8').hex()
        failStr = "reject".encode('utf-8').hex()
        w3.eth.default_account = w3.eth.accounts[0]
        tx_hash = w3.eth.contract(
            abi=contract_interface['abi'],
            bytecode=contract_interface['bin']).constructor([passStr, failStr]).transact()

        address = w3.eth.get_transaction_receipt(tx_hash)['contractAddress']
        return address
    
    def add_account(self):
        priv = secrets.token_hex(32)
        private_key = "0x" + priv
        acct = Account.from_key(private_key)

        return acct

    def deploy_voting_contract(self):
        contract_source_path = '/home/localaccount/Desktop/Pennapps/IKMR/solidity/contracts/vote.sol'
        compiled_sol = self.compile_source_file(contract_source_path)
        contract_id, contract_interface = compiled_sol.popitem()
        address = self.deploy_contract(self.w3, contract_interface)
        return address, contract_interface['abi']

    def getContractByAddress(self, contractAddress, abi):
        vote_contract = self.w3.eth.contract(address=contractAddress, abi=abi)
        return vote_contract
    
    def authorize_voter(self, contract, voterAddr, adminAddr):
        contract.functions.giveRightToVote(voterAddr).transact({'from': adminAddr})

    def vote(self, contract, voterAddr, voterKey, isYesVote):
        builtTransaction = None
        nonce = client.w3.eth.get_transaction_count(voterAddr)
        if isYesVote:
            builtTransaction = contract.functions.vote(0).buildTransaction({'gasPrice': 0, 'nonce': nonce})
        else:
            builtTransaction = contract.functions.vote(1).buildTransaction({'gasPrice': 0, 'nonce': nonce})
        
        signed_tx = self.w3.eth.account.sign_transaction(builtTransaction, private_key = voterKey)
        out = self.w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        return out

    def viewResult(self, contract):
        try:
            if contract.functions.winningProposal().call() == 0:
                return True
            else:
                return False
        except:
            return None





w3 = Web3(EthereumTesterProvider(PyEVMBackend()))
client = ethereumClient(EthereumTesterProvider(PyEVMBackend()))

# contract_source_path = '/home/localaccount/Desktop/Pennapps/IKMR/solidity/contracts/vote.sol'
# compiled_sol = client.compile_source_file(contract_source_path)

# contract_id, contract_interface = compiled_sol.popitem()

# address = client.deploy_contract(w3, contract_interface)
# print(f'Deployed {contract_id} to: {address}\n')

addr, abi = client.deploy_voting_contract()
acct = client.add_account()
acct1 = client.add_account()
acct2 = client.add_account()

vote_contract = client.getContractByAddress(addr, abi)

client.authorize_voter(vote_contract, acct.address, w3.eth.accounts[0])
client.authorize_voter(vote_contract, acct1.address, w3.eth.accounts[0])
print(len(client.w3.eth.accounts))
print(client.vote(vote_contract, acct.address, acct.privateKey, True))
#print(client.vote(vote_contract, acct1.address, acct1.privateKey, False))
print(client.vote(vote_contract, acct2.address, acct2.privateKey, False))
print(vote_contract.functions.winningProposal().call())



# gas_estimate = vote_contract.functions..estimateGas()

# print(vote_contract.functions.giveRightToVote(client.add_account()).transact({'from': w3.eth.accounts[0]}))


