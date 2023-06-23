// contracts/TokenStorage.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "./IERC20Burnable.sol";

error ZeroBalance();

/*
This storage should be able received ERC-20 token and record the current balance
*/
contract TokenStorage is Ownable {
    // event
    event TokensSent(address to, address token, uint256 amount);
    event TokensReceived(address from, address token, uint256 amount);
    event TokensWithdrew(address token, uint256 amount);
    event TokensBurnt(address token, uint256 amount);

    IERC20Burnable private _token;
    string public tokenName;
    string public tokenSymbol;

    constructor(address token) {
        _token = IERC20Burnable(token);
        tokenName = _token.name();
        tokenSymbol = _token.symbol();
    }

    function getTotalSupply() public view returns (uint256) {
        return _token.totalSupply();
    }

    /*
     * To send tokens from the storage to the specific address.
     */
    function transferToken(address to, uint256 amount) public onlyOwner {
        if (currentStorage() == 0) revert ZeroBalance();
        _token.transfer(to, amount);
        _token.approve(address(this), amount);
        emit TokensSent(to, address(_token), amount);
    }

    /*
     * To send tokens from the caller to the storage.
     */
    function receiveToken(uint256 amount) external {
        require(amount > 0, "Amount must be greater than zero");
        // check the allowance
        uint256 allowance = _token.allowance(msg.sender, address(this));
        require(allowance >= amount, "Insufficient allowance! Check it again");
        // perform the token transfer from sender to storage
        _token.transferFrom(msg.sender, address(this), amount);
        emit TokensReceived(msg.sender, address(_token), amount);
    }

    /*
     * To send the tokens to the owner address.
     */
    function withdrawToken(uint256 amount) public onlyOwner {
        if (currentStorage() == 0) revert ZeroBalance();
        _token.transfer(owner(), amount);
        _token.approve(address(this), amount);
        emit TokensWithdrew(address(_token), amount);
    }

    /*
     * To burn the tokens in storage, will burn all the available balance
     * if the amount exceeds the storage balance.
     */
    function burnToken(uint256 amount) public onlyOwner {
        if (currentStorage() == 0) revert ZeroBalance();
        uint256 amountBurnt;
        // handle the amount of token to be burnt
        if (amount > currentStorage()) {
            amountBurnt = currentStorage();
        } else {
            amountBurnt = amount;
        }
        // burn the token
        _token.burn(amountBurnt);
        _token.approve(address(this), amount);
        emit TokensBurnt(address(_token), amountBurnt);
    }

    function currentStorage() public view returns (uint256) {
        return _token.balanceOf(address(this));
    }
}
