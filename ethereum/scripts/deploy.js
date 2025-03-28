// Script to deploy the RentalContract
const hre = require("hardhat");

async function main() {
  console.log("Deploying Smart Rent contracts...");

  // Get the Contract Factory
  const RentalContract = await hre.ethers.getContractFactory("RentalContract");
  
  // Deploy the contract
  const rentalContract = await RentalContract.deploy();
  
  // Wait for deployment to finish
  await rentalContract.waitForDeployment();
  
  // Get the deployed contract address
  const contractAddress = await rentalContract.getAddress();
  
  console.log(`RentalContract deployed to: ${contractAddress}`);
  
  // Optional: Verify on Etherscan for non-local networks
  if (network.name !== "hardhat" && network.name !== "localhost") {
    console.log("Waiting for block confirmations...");
    await rentalContract.deploymentTransaction().wait(6);
    
    console.log("Verifying contract on Etherscan...");
    await hre.run("verify:verify", {
      address: contractAddress,
      constructorArguments: [],
    });
  }
  
  return contractAddress;
}

// Execute the deployment function
main()
  .then((contractAddress) => {
    console.log("Deployment complete! Contract address:", contractAddress);
    process.exit(0);
  })
  .catch((error) => {
    console.error("Error during deployment:", error);
    process.exit(1);
  }); 