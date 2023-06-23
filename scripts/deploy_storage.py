from brownie import ABROToken, TokenStorage, config, network
from web3 import Web3
from .deploy_token import deploy_token_abro
from .utils import get_account, LOCAL_BLOCKCHAIN_ENV


def deploy_storage_abro():
    # init params
    account = get_account()
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV and len(ABROToken) > 0:
        token = ABROToken[-1]
        print(f"Deployed contract was FOUND! Existing token contract: {token.address}")
    else:
        token = deploy_token_abro()

    # deploy the storage here
    storage = TokenStorage.deploy(
        token.address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Successfully deploy the {token.symbol()} storage on '{storage.address}'")
    return account, token, storage


def fund_storage(account, token, storage, amount):
    """
    To fund the storage with ABRO token

    Parameters
    ----------
    account: The funding account.
    token: The ERC20 token deployed contract.
    storage: The TokenStorage deployed contract.
    amount: The amount of token to be funded.
    """
    # approving the transfer managed by the storage!
    approval_tx = token.approve(storage.address, amount, {"from": account})
    # this will allow TokenStorage to call the transferFrom, thus allowing
    # storage to transfer ABRO token from funding account on funding account's behalf
    approval_tx.wait(1)
    # funding is now possible, fund the storage here
    fund_tx = storage.receiveToken(amount, {"from": account})
    fund_tx.wait(1)
    return fund_tx.events["TokensReceived"]


def main():
    deploy_storage_abro()
