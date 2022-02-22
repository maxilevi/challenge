from brownie import accounts, ETHPool
import pytest

@pytest.fixture
def pool():
    return accounts[0].deploy(ETHPool)

def test_depositing_to_pool(pool):
    balance = accounts[1].balance()
    pool.deposit({'from': accounts[1], 'value': "0.1 ether"})

    assert balance - "0.1 ether" == accounts[1].balance()
    assert pool.totalDeposits() == "0.1 ether"


def test_multiple_deposits_add_up(pool):
    balanceA = accounts[1].balance()
    balanceB = accounts[2].balance()
    pool.deposit({'from': accounts[1], 'value': "0.5 ether"})
    pool.deposit({'from': accounts[2], 'value': "0.1 ether"})
    pool.deposit({'from': accounts[2], 'value': "0.1 ether"})

    assert balanceA - "0.5 ether" == accounts[1].balance()
    assert balanceB - "0.2 ether" == accounts[2].balance()
    assert pool.totalDeposits() == "0.7 ether"