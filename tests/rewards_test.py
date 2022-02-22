from brownie import accounts, ETHPool
import pytest

@pytest.fixture
def pool():
    return accounts[0].deploy(ETHPool)

def test_single_rewards(pool):
    balance = accounts[1].balance()

    pool.deposit({'from': accounts[1], 'value': "10 ether"})

    pool.addRewards({'from': accounts[0], 'value': "10 ether"})

    pool.withdraw({'from': accounts[1]})

    assert balance + "10 ether" == accounts[1].balance()


def test_rewards_at_the_same_time(pool):
    balanceA = accounts[1].balance()
    balanceB = accounts[2].balance()

    pool.deposit({'from': accounts[1], 'value': "15 ether"})
    pool.deposit({'from': accounts[2], 'value': "5 ether"})

    pool.addRewards({'from': accounts[0], 'value': "10 ether"})

    pool.withdraw({'from': accounts[1]})
    pool.withdraw({'from': accounts[2]})

    assert balanceA + "7.5 ether" == accounts[1].balance()
    assert balanceB + "2.5 ether" == accounts[2].balance()


def test_rewards_mixed(pool):
    balanceA = accounts[1].balance()
    balanceB = accounts[2].balance()

    pool.deposit({'from': accounts[1], 'value': "5 ether"})
    pool.addRewards({'from': accounts[0], 'value': "10 ether"})

    pool.deposit({'from': accounts[2], 'value': "5 ether"})

    pool.withdraw({'from': accounts[1]})
    pool.withdraw({'from': accounts[2]})

    assert balanceA + "10 ether" == accounts[1].balance()
    assert balanceB == accounts[2].balance()


def test_rewards_mixed_multiple_deposits(pool):
    balanceA = accounts[1].balance()
    balanceB = accounts[2].balance()

    pool.deposit({'from': accounts[1], 'value': "5 ether"})
    pool.addRewards({'from': accounts[0], 'value': "10 ether"})

    pool.deposit({'from': accounts[2], 'value': "15 ether"})
    pool.deposit({'from': accounts[1], 'value': "5 ether"})
    pool.addRewards({'from': accounts[0], 'value': "10 ether"})

    pool.withdraw({'from': accounts[1]})
    pool.withdraw({'from': accounts[2]})

    assert balanceA + "15 ether" + "7.5 ether" == accounts[1].balance()
    assert balanceB + "22.5 ether" == accounts[2].balance()

def test_multiple_add_rewards(pool):
    balanceA = accounts[1].balance()
    balanceB = accounts[2].balance()

    pool.deposit({'from': accounts[1], 'value': "5 ether"})
    pool.deposit({'from': accounts[2], 'value': "15 ether"})
    pool.addRewards({'from': accounts[0], 'value': "10 ether"})
    pool.addRewards({'from': accounts[0], 'value': "10 ether"})

    pool.withdraw({'from': accounts[1]})
    pool.withdraw({'from': accounts[2]})

    assert balanceA + "5 ether" == accounts[1].balance()
    assert balanceB + "15 ether" == accounts[2].balance()
