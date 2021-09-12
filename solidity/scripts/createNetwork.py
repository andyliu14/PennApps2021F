from brownie import *
#from brownie.network import rpc, web3, accounts
#from brownie import Vote
from web3 import Web3, EthereumTesterProvider
import json

# network.connect('development')
import time


# web3.connect('http://127.0.0.1:8545')
# print(len(accounts))
# accounts.add()
# print(len(accounts))

class ethereumClient:
    def __init__(self, connectionString):
        #self.client = network.connect(connectionString)
        #self.w3 = Web3('http://127.0.0.1:8545')
        self.w3 = Web3(EthereumTesterProvider())
        #network.gas_price(0)
        self.val = 1
    
    def addAccount(self):
        acc = accounts.add()
        return acc

    def getAccount(self, addr):
        return accounts.at(addr)

    def printContract(self):
        print("Null")
    
    def getContractInfo(self, jsonPath):
        f = open(jsonPath)
        data = json.load(f)
        f.close()
        return [data['abi'], data['bytecode']]
    
    def deployContract(self, jsonPath):
        info = self.getContractInfo(jsonPath)
        Vote = self.w3.eth.contract(abi=info[0], bytecode=info[1])
        # print(self.w3.eth.accounts())
        print(web3.eth.get_accounts())
        #self.w3.eth.default_account = web3.eth.accounts[0]
        passStr = "pass".encode('utf-8').hex()
        failStr = "reject".encode('utf-8').hex()
        tx_hash = Vote.constructor([passStr, failStr]).transact()
        # print(tx_hash)
    

client = ethereumClient("asdflkj")
# client.addAccount()
# addr0 = client.addAccount()
# addr1 = client.addAccount()
# addr2 = client.addAccount()
# print(addr2)
client.deployContract('/home/localaccount/Desktop/Pennapps/IKMR/solidity/build/contracts/Vote.json')



# def main():
#     client = ethereumClient("development")
#     client.printContract()


#     Vote.deploy([passStr, failStr], {'from': accounts[0]})
#     Vote[0].giveRightToVote(addr0, {'from': accounts[0]})
#     Vote[0].giveRightToVote(addr1, {'from': accounts[0]})
#     Vote[0].giveRightToVote(addr2, {'from': accounts[0]})

#     Vote[0].vote(0, {'from': addr0})
#     Vote[0].vote(1, {'from': addr1})
#     #print(Vote[0].winningProposal())

#     Vote[0].vote(0, {'from': addr2})
#     print(Vote[0].winningProposal())
#     time.sleep(2)
#     network.disconnect()
