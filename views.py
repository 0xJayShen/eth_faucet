# -*- coding: utf8 -*-
from flask import Blueprint, jsonify, request
import json
from web3 import Web3, HTTPProvider
import logging
import traceback

encoding = "UTF-8"
# handler = logging.StreamHandler()
handler = logging.FileHandler(filename='mylog.log', encoding='utf-8', )
fmt = logging.Formatter(fmt='%(asctime)s -- %(message)s -- %(filename)s -- %(lineno)d', datefmt='"%Y/%m/%d/ %H:%M:%S "')
handler.setFormatter(fmt)
log = logging.getLogger('log')
log.addHandler(handler)
log.setLevel(logging.DEBUG)

faucet = Blueprint('faucet', __name__)
eth_from_address = "0xb2Dc181F5580AF44570fC004e16f2E3E8222C2a0"
eth_from_privkey = "DDAB8C68D59D33E4943C43927679E7FB049C454B58FD2BF9C69779E5664D9C6A"
usdt_from_address = "0xDc4D5d5770fce6D8f4e0696E5EC44f025891C4e0"
usdt_from_privkey = "F378C71E699F2478711958A75925D0F916E4B010C9D66F81E4BBB44D6A82D034"
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
eth_donate_address = []
usdt_donate_address = []
chain_id = 42
url = "https://kovan.infura.io/v3/1778da334fac4d52ab04e5b305124334"
token_address = "0x8291a209a0502dc3ab9320e2e24a0e61b4909e09"


@faucet.route('/donate', methods=["POST"])
def login():
    try:
        data = json.loads(request.get_data(as_text=True))
        address = data.get("address")
        coin_name = data.get("coin_name")
        web3 = Web3(HTTPProvider(url))
        result_hash = ""
        if coin_name == "ETH":
            nonce = web3.eth.getTransactionCount(Web3.toChecksumAddress(eth_from_address), "pending")

            if address in eth_donate_address:
                return jsonify({"code": 300, "msg": "repeat to receive", "data": {}})
            eth_donate_address.append(address)
            transaction = {
                'value': Web3.toWei(0.01, 'ether'),
                'gas': 2000000,
                'gasPrice': web3.toWei('10', 'gwei'),
                'nonce': nonce,
                'chainId': chain_id,
                'to': Web3.toChecksumAddress(address),

            }
            signed = web3.eth.account.signTransaction(transaction, eth_from_privkey)
            result_hash = json.loads(web3.toJSON(web3.eth.sendRawTransaction(signed.rawTransaction)))
        if coin_name == "USDT":
            nonce = web3.eth.getTransactionCount(Web3.toChecksumAddress(usdt_from_address), "pending")

            if address in usdt_donate_address:
                return jsonify({"code": 300, "msg": "repeat to receive", "data": {}})
            usdt_donate_address.append(address)
            unicorns = web3.eth.contract(address=Web3.toChecksumAddress(token_address), abi=usdt_abi)
            unicorn_txn = unicorns.functions.transfer(
                Web3.toChecksumAddress(address),
                20000000,
            ).buildTransaction({
                'chainId': chain_id,
                'gas': 2000000,
                'gasPrice': web3.toWei('10', 'gwei'),
                'nonce': nonce,
            })
            signed_txn = web3.eth.account.signTransaction(unicorn_txn, usdt_from_privkey)
            result_hash = json.loads(web3.toJSON(web3.eth.sendRawTransaction(signed_txn.rawTransaction)))

        response = jsonify({"code": 200, "msg": "", "data": {"hash": str(result_hash)}})
    except Exception as e:
        error_traceback = traceback.format_exc()
        log.error(error_traceback)
        response = jsonify({"code": 300, "msg": "repeat to receive", "data": {}})

    return response
