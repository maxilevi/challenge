from brownie import accounts, ETHPool
import pytest

@pytest.fixture
def pool():
    return accounts[0].deploy(ETHPool)

def test_withdrawing(pool):
    balance = accounts[1].balance()

    pool.deposit({'from': accounts[1], 'value': "10 ether"})
    pool.deposit({'from': accounts[1], 'value': "10 ether"})

    pool.withdraw({'from': accounts[1]})

    assert balance == accounts[1].balance()
    assert pool.totalDeposits() == 0


def test_multiple_withdrawals(pool):
    balanceA = accounts[1].balance()
    balanceB = accounts[2].balance()
    pool.deposit({'from': accounts[1], 'value': "0.5 ether"})
    pool.deposit({'from': accounts[2], 'value': "10.0 ether"})
    pool.deposit({'from': accounts[1], 'value': "0.5 ether"})

    pool.withdraw({'from': accounts[1]})
    pool.withdraw({'from': accounts[2]})

    pool.deposit({'from': accounts[2], 'value': "10.0 ether"})
    pool.withdraw({'from': accounts[2]})


    assert balanceA == accounts[1].balance()
    assert balanceB == accounts[2].balance()
    assert pool.totalDeposits() == 0