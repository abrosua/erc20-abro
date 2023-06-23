import pytest
from brownie import network
from scripts.utils import LOCAL_BLOCKCHAIN_ENV


def unit_test_restriction():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENV:
        pytest.skip("Unit test is for LOCAL testing only!")
