import { ethers } from "hardhat";

async function main() {
  const lockedAmount = ethers.utils.parseEther("0.00000001");

  const Lock = await ethers.getContractFactory("QuestNFT");
  const lock = await Lock.deploy();

  await lock.deployed();

  console.log(`NFT Quests deployed to ${lock.address}`);
  // console.log(`Block explorer URL: https://l2scan.scroll.io/address/${lock.address}`); Uncomment here to use the pre-alpha
  console.log(
    `Block explorer URL: https://blockscout.scroll.io/address/${lock.address}`
  );
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
