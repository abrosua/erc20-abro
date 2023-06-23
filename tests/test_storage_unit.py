import pytest
from brownie import exceptions
from scripts.deploy_storage import deploy_storage_abro, fund_storage
from scripts.utils import get_account
from tests.utils import unit_test_restriction


def test_storage_can_receive():
    """To test the storage can receive some ABRO tokens."""
    unit_test_restriction()
    # Arrange
    account, token, storage = deploy_storage_abro()
    amount = 6 * (10 ** token.decimals())
    balance_before = token.balanceOf(account)
    # Act
    received_event = fund_storage(account, token, storage, amount)
    received = received_event["amount"]
    from_address = received_event["from"]
    storage_balance = storage.currentStorage()
    # Assert
    balance_after = token.balanceOf(account)
    print(
        f"Receiving token --- amount: {received}, storage balance: {storage_balance} "
        f"and remaining sender balance: {balance_after}"
    )
    assert from_address == account
    assert amount == received and amount == storage.currentStorage()
    assert balance_before == balance_after + amount
    print(f"Passed the RECEIVE unit test!")


def test_storage_can_transfer():
    """To test the storage can transfer some ABRO tokens (owner only)."""
    unit_test_restriction()
    # Arrange
    account_admin, token, storage = deploy_storage_abro()
    amount = 6 * (10 ** token.decimals())
    fund_storage(account_admin, token, storage, amount)
    account_to = get_account(index=1)
    storage_before = storage.currentStorage()
    # Act
    transfer_tx = storage.transferToken(account_to, amount, {"from": account_admin})
    transfer_tx.wait(1)
    sent_amount = transfer_tx.events["TokensSent"]["amount"]
    sent_to = transfer_tx.events["TokensSent"]["to"]
    # Assert
    print(
        f"Sent token --- amount: {sent_amount}, storage balance: {storage.currentStorage()} "
        f"and the target balance: {token.balanceOf(account_to)}"
    )
    assert account_to == sent_to
    assert amount == sent_amount and amount == token.balanceOf(account_to)
    assert storage_before == amount + storage.currentStorage()
    # Act & Assert: Zero balance test
    with pytest.raises(exceptions.VirtualMachineError) as e:
        storage.transferToken(account_to, amount, {"from": account_admin})
    assert "ZeroBalance()" in str(e.value)


def test_storage_can_withdraw():
    """To test the storage can withdraw some ABRO tokens (owner only)."""
    unit_test_restriction()
    # Arrange
    account_admin, token, storage = deploy_storage_abro()
    amount = 5 * (10 ** token.decimals())
    fund_storage(account_admin, token, storage, amount)
    storage_before = storage.currentStorage()
    admin_before = token.balanceOf(account_admin)
    # Act
    withdraw_tx = storage.withdrawToken(amount, {"from": account_admin})
    withdraw_tx.wait(1)
    withdraw_amount = withdraw_tx.events["TokensWithdrew"]["amount"]
    # Assert
    print(
        f"Withdrew token --- amount: {withdraw_amount}, storage balance: "
        f"{storage.currentStorage()} and the admin: {token.balanceOf(account_admin)}"
    )
    assert amount == withdraw_amount
    assert amount == token.balanceOf(account_admin) - admin_before
    assert storage_before == amount + storage.currentStorage()
    # Act & Assert: Zero balance test
    with pytest.raises(exceptions.VirtualMachineError) as e:
        storage.withdrawToken(amount, {"from": account_admin})
    assert "ZeroBalance()" in str(e.value)


def test_storage_can_burn():
    """
    To test the storage can burn some ABRO tokens (owner only).
    Also test requesting to burn tokens more than the storage balance.
    """
    unit_test_restriction()
    # Arrange
    account_admin, token, storage = deploy_storage_abro()
    amount = 7 * (10 ** token.decimals())
    fund_storage(account_admin, token, storage, amount)
    storage_before = storage.currentStorage()
    init_supply = token.totalSupply()
    # Act
    burn_tx = storage.burnToken(amount, {"from": account_admin})
    burn_tx.wait(1)
    burn_amount = burn_tx.events["TokensBurnt"]["amount"]
    # Assert
    print(
        f"Burn token --- amount: {burn_amount}, storage balance: "
        f"{storage.currentStorage()} and the total supply: {token.totalSupply()}"
    )
    assert amount == burn_amount
    assert storage_before - amount == storage.currentStorage()
    assert init_supply - amount == token.totalSupply()
    # Act & Assert: Zero balance test
    with pytest.raises(exceptions.VirtualMachineError) as e:
        storage.burnToken(amount, {"from": account_admin})
    assert "ZeroBalance()" in str(e.value)
