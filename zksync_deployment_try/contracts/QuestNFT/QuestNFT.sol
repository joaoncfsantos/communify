// SPDX-License-Identifier: MIT
pragma solidity ^0.8.9;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";

contract QuestNFT is ERC721, Ownable {
    using Strings for uint256;

    uint public constant MAX_TOKENS = 10000;
    uint public constant MAX_TOKEN_PER_WALLET = 1;
    uint private constant TOKENS_RESERVED = 5;
    uint public price = 0;

    bool public isSaleActive;
    uint256 public totalSupply;
    mapping(address => uint256) private mintedPerWallet;

    string public baseUri;
    string public baseExtension = ".json";

    constructor() ERC721("QuestNFT", "QUEST") {
        baseUri = "ipfs://xxxxxxxxxxxxxxxxxxxxxxxxxxxxx/";
        for(uint256 i = 1; i <= TOKENS_RESERVED; ++i) {
            _safeMint(msg.sender, i);
        }
        totalSupply = TOKENS_RESERVED;
    }

    // Public Functions
    function mint() external payable {
        require(isSaleActive, "The sale is paused.");
        require(mintedPerWallet[msg.sender] < MAX_TOKEN_PER_WALLET, "You already have this quest token");
        uint256 curTotalSupply = totalSupply;
        require(curTotalSupply + 1 <= MAX_TOKENS, "Exceeds total supply.");
        require(price <= msg.value, "Insufficient funds.");

        _safeMint(msg.sender, curTotalSupply+1);
        mintedPerWallet[msg.sender]++;
        totalSupply++;
    }

    // Owner-only functions

    function launch_quest() external onlyOwner {
        isSaleActive = true;
    }

    function close_quest() external onlyOwner {
        isSaleActive = false;
    }

    function setBaseUri(string memory _baseUri) external onlyOwner {
        baseUri = _baseUri;
    }

    function setPrice(uint256 _price) external onlyOwner {
        price = _price;
    }

    function withdrawAll() external payable onlyOwner {
        uint256 balance = address(this).balance;
        uint256 balanceOne = balance * 70 / 100;
        uint256 balanceTwo = balance * 30 / 100;
        ( bool transferOne, ) = payable(0x7ceB3cAf7cA83D837F9d04c59f41a92c1dC71C7d).call{value: balanceOne}("");
        ( bool transferTwo, ) = payable(0x7ceB3cAf7cA83D837F9d04c59f41a92c1dC71C7d).call{value: balanceTwo}("");
        require(transferOne && transferTwo, "Transfer failed.");
    }

    function tokenURI(uint256 tokenId) public view virtual override returns (string memory) {
        require(_exists(tokenId), "ERC721Metadata: URI query for nonexistent token");
 
        string memory currentBaseURI = _baseURI();
        return bytes(currentBaseURI).length > 0
            ? string(abi.encodePacked(currentBaseURI, tokenId.toString(), baseExtension))
            : "";
    }
 
    function _baseURI() internal view virtual override returns (string memory) {
        return baseUri;
    }
}