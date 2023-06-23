// contracts/AbrosuaToken.sol
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";

contract ABROToken is ERC20Burnable {
    constructor(
        address owner,
        uint256 initialSupply
    ) ERC20("Abrosua Token", "ABRO") {
        _mint(owner, initialSupply);
    }
}
