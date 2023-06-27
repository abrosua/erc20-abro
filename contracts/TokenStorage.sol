// contracts/TokenStorage.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import {IERC20BurnPermit} from "./IERC20BurnPermit.sol";

error ZeroBalance();

/*
This storage should be able received ERC-20 token and record the current balance
*/
contract TokenStorage is Ownable {
    using SafeERC20 for IERC20;

    // event
    event TokensSent(address to, address token, uint256 amount);
    event TokensReceived(address from, address token, uint256 amount);
    event TokensWithdrew(address token, uint256 amount);
    event TokensBurnt(address token, uint256 amount);

    IERC20BurnPermit private _token;
    IERC20 private _tokenSafe;
    string public tokenName;
    string public tokenSymbol;

    constructor(address token) {
        _token = IERC20BurnPermit(token);
        _tokenSafe = IERC20(token);
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
     * To send tokens from the caller to the storage with permit signature!
     */
    function receiveTokenPermit(
        uint256 amount,
        uint256 deadline,
        uint8 permitV,
        bytes32 permitR,
        bytes32 permitS
    ) external {
        require(amount > 0, "Amount must be greater than zero");
        // handle ERC20 permit signature
        {
            _token.permit(
                msg.sender,
                address(this),
                amount,
                deadline,
                permitV,
                permitR,
                permitS
            );
        }
        // perform the token transfer from sender to storage
        _tokenSafe.safeTransferFrom(msg.sender, address(this), amount);
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
