from brownie import ABROToken, config, network
from web3 import Web3
from .utils import get_account


def deploy_token_abro():
    # init params
    account = get_account()
    init_supply = 1000  # ABRO, without precision

    # deployment
    token = ABROToken.deploy(
        account,
        Web3.toWei(init_supply, "ether"),
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )
    print(f"Successfully deploy the {token.symbol()} token on '{token.address}'")
    return token


def main():
    deploy_token_abro()
