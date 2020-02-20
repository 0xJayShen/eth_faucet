# -*- coding: utf8 -*-
from flask import Blueprint, jsonify, request
import json
from web3 import Web3, HTTPProvider

faucet = Blueprint('faucet', __name__)
from_address = "0x9Ba9Ae032a2709efb6eB5651b78058F19f01A38C"
from_privkey = "6979024FF24828859CF98B5BA61E73827CFBC0BC2F01DCF7F170F23172639A62"
usdt_abi = [
    {"constant": True, "inputs": [], "name": "name", "outputs": [{"name": "", "type": "string"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"name": "_upgradedAddress", "type": "address"}], "name": "deprecate", "outputs": [],
     "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"name": "_spender", "type": "address"}, {"name": "_value", "type": "uint256"}],
     "name": "approve", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [], "name": "deprecated", "outputs": [{"name": "", "type": "bool"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"name": "_evilUser", "type": "address"}], "name": "addBlackList", "outputs": [],
     "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [], "name": "totalSupply", "outputs": [{"name": "", "type": "uint256"}],
     "payable": False, "stateMutability": "view", "type": "function"}, {"constant": False,
                                                                        "inputs": [{"name": "_from", "type": "address"},
                                                                                   {"name": "_to", "type": "address"},
                                                                                   {"name": "_value",
                                                                                    "type": "uint256"}],
                                                                        "name": "transferFrom", "outputs": [],
                                                                        "payable": False,
                                                                        "stateMutability": "nonpayable",
                                                                        "type": "function"},
    {"constant": True, "inputs": [], "name": "upgradedAddress", "outputs": [{"name": "", "type": "address"}],
     "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [{"name": "", "type": "address"}], "name": "balances",
     "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint256"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "maximumFee", "outputs": [{"name": "", "type": "uint256"}],
     "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "_totalSupply", "outputs": [{"name": "", "type": "uint256"}],
     "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [], "name": "unpause", "outputs": [], "payable": False,
     "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [{"name": "_maker", "type": "address"}], "name": "getBlackListStatus",
     "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [{"name": "", "type": "address"}, {"name": "", "type": "address"}], "name": "allowed",
     "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "paused", "outputs": [{"name": "", "type": "bool"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [{"name": "who", "type": "address"}], "name": "balanceOf",
     "outputs": [{"name": "", "type": "uint256"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [], "name": "pause", "outputs": [], "payable": False, "stateMutability": "nonpayable",
     "type": "function"},
    {"constant": True, "inputs": [], "name": "getOwner", "outputs": [{"name": "", "type": "address"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "owner", "outputs": [{"name": "", "type": "address"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "symbol", "outputs": [{"name": "", "type": "string"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"name": "_to", "type": "address"}, {"name": "_value", "type": "uint256"}],
     "name": "transfer", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False,
     "inputs": [{"name": "newBasisPoints", "type": "uint256"}, {"name": "newMaxFee", "type": "uint256"}],
     "name": "setParams", "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"name": "amount", "type": "uint256"}], "name": "issue", "outputs": [],
     "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"name": "amount", "type": "uint256"}], "name": "redeem", "outputs": [],
     "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [{"name": "_owner", "type": "address"}, {"name": "_spender", "type": "address"}],
     "name": "allowance", "outputs": [{"name": "remaining", "type": "uint256"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [], "name": "basisPointsRate", "outputs": [{"name": "", "type": "uint256"}],
     "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": True, "inputs": [{"name": "", "type": "address"}], "name": "isBlackListed",
     "outputs": [{"name": "", "type": "bool"}], "payable": False, "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"name": "_clearedUser", "type": "address"}], "name": "removeBlackList",
     "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": True, "inputs": [], "name": "MAX_UINT", "outputs": [{"name": "", "type": "uint256"}], "payable": False,
     "stateMutability": "view", "type": "function"},
    {"constant": False, "inputs": [{"name": "newOwner", "type": "address"}], "name": "transferOwnership", "outputs": [],
     "payable": False, "stateMutability": "nonpayable", "type": "function"},
    {"constant": False, "inputs": [{"name": "_blackListedUser", "type": "address"}], "name": "destroyBlackFunds",
     "outputs": [], "payable": False, "stateMutability": "nonpayable", "type": "function"}, {
        "inputs": [{"name": "_initialSupply", "type": "uint256"}, {"name": "_name", "type": "string"},
                   {"name": "_symbol", "type": "string"}, {"name": "_decimals", "type": "uint256"}], "payable": False,
        "stateMutability": "nonpayable", "type": "constructor"},
    {"anonymous": False, "inputs": [{"indexed": False, "name": "amount", "type": "uint256"}], "name": "Issue",
     "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "name": "amount", "type": "uint256"}], "name": "Redeem",
     "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "name": "newAddress", "type": "address"}], "name": "Deprecate",
     "type": "event"}, {"anonymous": False, "inputs": [{"indexed": False, "name": "feeBasisPoints", "type": "uint256"},
                                                       {"indexed": False, "name": "maxFee", "type": "uint256"}],
                        "name": "Params", "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": False, "name": "_blackListedUser", "type": "address"},
        {"indexed": False, "name": "_balance", "type": "uint256"}], "name": "DestroyedBlackFunds", "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "name": "_user", "type": "address"}], "name": "AddedBlackList",
     "type": "event"},
    {"anonymous": False, "inputs": [{"indexed": False, "name": "_user", "type": "address"}], "name": "RemovedBlackList",
     "type": "event"}, {"anonymous": False, "inputs": [{"indexed": True, "name": "owner", "type": "address"},
                                                       {"indexed": True, "name": "spender", "type": "address"},
                                                       {"indexed": False, "name": "value", "type": "uint256"}],
                        "name": "Approval", "type": "event"}, {"anonymous": False, "inputs": [
        {"indexed": True, "name": "from", "type": "address"}, {"indexed": True, "name": "to", "type": "address"},
        {"indexed": False, "name": "value", "type": "uint256"}], "name": "Transfer", "type": "event"},
    {"anonymous": False, "inputs": [], "name": "Pause", "type": "event"},
    {"anonymous": False, "inputs": [], "name": "Unpause", "type": "event"}]
eth_donate_IP = []
usdt_donate_IP = []
chain_id = 42
url = "https://kovan.infura.io/v3/1778da334fac4d52ab04e5b305124334"
token_address = "0x8291a209a0502dc3ab9320e2e24a0e61b4909e09"
@faucet.route('/donate', methods=["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    address = data.get("address")
    coin_name = data.get("coin_name")
    IP = request.remote_addr
    web3 = Web3(HTTPProvider(url))
    nonce = web3.eth.getTransactionCount(Web3.toChecksumAddress(from_address), "pending")
    result_hash = ""

    if coin_name == "ETH":
        if IP in eth_donate_IP:
            return jsonify({"code": 300, "msg": "repeat to receive", "data": {}})
        eth_donate_IP.append(IP)
        transaction = {
            'value': Web3.toWei(0.01, 'ether'),
            'gas': 2000000,
            'gasPrice': web3.toWei('10', 'gwei'),
            'nonce': nonce,
            'chainId': chain_id,
            'to': Web3.toChecksumAddress(address),

        }
        signed = web3.eth.account.signTransaction(transaction, from_privkey)
        result_hash = json.loads(web3.toJSON(web3.eth.sendRawTransaction(signed.rawTransaction)))
    if coin_name == "USDT":
        if IP in usdt_donate_IP:
            return jsonify({"code": 300, "msg": "repeat to receive", "data": {}})
        usdt_donate_IP.append(IP)
        unicorns = web3.eth.contract(address=Web3.toChecksumAddress(token_address),abi=usdt_abi)
        unicorn_txn = unicorns.functions.transfer(
            Web3.toChecksumAddress(address),
            20000000,
        ).buildTransaction({
            'chainId': chain_id,
            'gas': 2000000,
            'gasPrice': web3.toWei('10', 'gwei'),
            'nonce': nonce,
        })
        signed_txn = web3.eth.account.signTransaction(unicorn_txn, from_privkey)
        result_hash = json.loads(web3.toJSON(web3.eth.sendRawTransaction(signed_txn.rawTransaction)))

    response = jsonify({"code": 200, "msg": "", "data": {"hash": str(result_hash)}})

    return response
