from typing import Optional
from brownie import (
    accounts,
    config,
    network,
)
from web3 import Web3


# chain required for Mocking
LOCAL_BLOCKCHAIN_ENV = [
    "development",  # run using ganache-cli
    "ganache-local",  # ganache UI for mock contract deployment!
]
# chain required for Forking
FORKED_LOCAL_ENV = [
    "mainnet-fork",  # Ganache CLI, ethereum mainnet forked
]
BURN_ADDRESS = "0x0000000000000000000000000000000000000000"


def get_account(index=None, id=None):
    if index is not None:
        # automatically use stored account via indexing
        return accounts[index]
    if id is not None:
        # get from the stored account in brownie
        return accounts.load(id)

    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENV
        or network.show_active() in FORKED_LOCAL_ENV
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["key_playground"])
