require("@matterlabs/hardhat-zksync-deploy");
require("@matterlabs/hardhat-zksync-solc");

module.exports = {
  zksolc: {
    version: "latest",
  },
  zkSyncDeploy: {
    zkSyncNetwork:
      process.env.NODE_ENV == "test"
        ? {
            url: "http://localhost:3050",
            ethNetwork: "http://localhost:8545",
            zksync: true,
          }
        : {
            url: "https://zksync2-testnet.zksync.dev",
            ethNetwork: "goerli",
            zksync: true,
            // contract verification endpoint
            verifyURL:
              "https://zksync2-testnet-explorer.zksync.dev/contract_verification",
          },
    ethNetwork: "goerli",
  },
  networks: {
    // To compile with zksolc, this must be the default network.
    hardhat: {
      zksync: true,
    },
  },
  solidity: {
    version: "0.8.17",
  },
};