from scripts.deploy_token import deploy_token_abro
from scripts.utils import get_account
from tests.utils import unit_test_restriction


def test_token_deploy():
    """To check the ABRO token deployment, and if the supply is sent to the owner"""
    unit_test_restriction()
    # Arrange
    account = get_account()
    token = deploy_token_abro()
    # Act
    minted_abro = token.totalSupply()
    account_balance_abro = token.balanceOf(account)
    # Assert
    print(f"ABRO token - minted: {minted_abro} vs account: {account_balance_abro}")
    assert minted_abro == account_balance_abro


def test_token_transfer():
    """To test transferring the ABRO token to another address."""
    unit_test_restriction()
    # Arrange
    account_from = get_account(index=0)
    account_to = get_account(index=1)
    token = deploy_token_abro()
    balance_from_before = token.balanceOf(account_from)
    # Act
    transfer_amount = 4  # ABRO token without precision
    precised_amount = transfer_amount * (10 ** token.decimals())
    transfer_tx = token.transfer(account_to, precised_amount, {"from": account_from})
    transfer_tx.wait(1)
    # Assert
    balance_to_after = token.balanceOf(account_to)
    balance_from_after = token.balanceOf(account_from)
    print(
        f"ABRO token - sent: {precised_amount} vs received: {balance_to_after}; "
        f"Sender remaining balance: {balance_from_after}"
    )
    assert precised_amount == balance_to_after
    assert balance_from_before == balance_from_after + precised_amount


def test_token_burn():
    """To test burning the ABRO token."""
    unit_test_restriction()
    # Arrange
    account = get_account()
    token = deploy_token_abro()
    init_supply = token.totalSupply()
    balance_before = token.balanceOf(account)
    # Act
    amount_to_burn = 7
    precised_amount_to_burn = amount_to_burn * (10 ** token.decimals())
    burn_tx = token.burn(precised_amount_to_burn, {"from": account})
    burn_tx.wait(1)
    balance_after = token.balanceOf(account)
    # Assert
    burned_supply = init_supply - token.totalSupply()
    print(
        f"ABRO token - burn: {precised_amount_to_burn} vs burned: {burned_supply}; "
        f"Sender remaining balance: {balance_after}"
    )
    assert precised_amount_to_burn == burned_supply
    assert balance_before == balance_after + burned_supply
