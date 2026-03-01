const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

async function main() {
  // Setup accounts
  const [deployer] = await ethers.getSigners();
  console.log("Deploying contracts with the account:", deployer.address);

  // Deploy the contract
  const identityStorage = await hre.ethers.deployContract("IdentityStorage");
  await identityStorage.waitForDeployment();
  const contractAddress = await identityStorage.getAddress();

  console.log("IdentityStorage deployed to:", contractAddress);

  // SAVE THE ADDRESS AND ABI FOR THE PYTHON CLIENT
  // This is crucial so the Python script knows where the contract is.
  const artifact = await hre.artifacts.readArtifact("IdentityStorage");
  const contractData = {
    address: contractAddress,
    abi: artifact.abi
  };

  // Save to the client folder
  fs.writeFileSync(
    path.join(__dirname, "../client/contract_data.json"),
    JSON.stringify(contractData, null, 2)
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});