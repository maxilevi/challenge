pragma solidity ^0.8.7;

contract ETHPool {

    mapping(address => uint256) public deposits;
    mapping(address => uint256) public unclaimedRewards;
    mapping(address => uint256) public rewardsWhenDeposited;
    mapping(uint256 => uint256) public totalBalanceWhenAddedRewards;
    uint256 public totalDeposits;
    uint256 public lifetimeRewards;

    function deposit() public payable {
        require(msg.value > 0, "Cannot deposit 0");
        uint256 depositValue = msg.value;

        if (deposits[msg.sender] != 0)
        {
            (uint256 principal, uint256 rewards) = doWithdraw(msg.sender);
            unclaimedRewards[msg.sender] += rewards;
            depositValue += principal;
        }

        deposits[msg.sender] += depositValue;
        rewardsWhenDeposited[msg.sender] = lifetimeRewards;
        totalDeposits += depositValue;
    }

    function doWithdraw(address from) private returns (uint256, uint256)
    {
        uint256 principal = deposits[from];
        require(principal > 0, "Cannot withdraw without depositing first");

        uint256 owedRewardsPool = (lifetimeRewards - rewardsWhenDeposited[from]);
        uint256 totalDepositsAtTheRewardMoment = totalBalanceWhenAddedRewards[lifetimeRewards] - totalBalanceWhenAddedRewards[rewardsWhenDeposited[from]];
        uint256 rewards = 0;
        if (totalDepositsAtTheRewardMoment > 0)
            rewards = owedRewardsPool * principal / totalDepositsAtTheRewardMoment + unclaimedRewards[from];

        totalDeposits -= principal;
        unclaimedRewards[from] = 0;
        deposits[from] = 0;

        return (principal, rewards);
    }

    function withdraw() public {
        (uint256 principal, uint256 rewards) = doWithdraw(msg.sender);
        uint256 amount = principal + rewards;

        (bool success, ) = msg.sender.call{value: amount}('');
        require(success, "Withdraw transfer failed");
    }

    function addRewards() public payable {
        require(msg.value > 0, "Cannot add no rewards");

        lifetimeRewards += msg.value;
        totalBalanceWhenAddedRewards[lifetimeRewards] = totalDeposits;
    }
}
