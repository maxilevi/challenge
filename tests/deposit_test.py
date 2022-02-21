from brownie import accounts, ETHPool
import pytest

@pytest.fixture
def pool():
    return accounts[0].deploy(ETHPool)

def test_depositing_to_pool(pool):
    balance = accounts[1].balance()
    pool.deposit()
    accounts[1].transfer(accounts[1], "10 ether", gas_price=0)

    assert balance - "10 ether" == accounts[0].balance()