const { expect } = require('chai');
const { ethers } = require('hardhat');

describe('SmartRent Contract', function () {
  let SmartRent;
  let smartRent;
  let owner;
  let landlord;
  let tenant;
  let addrs;

  // Sample property data
  const metadataURI = "ipfs://QmX7DFZ8FwTJ3xdAgznRJXBr5LNRyUH7DFZ8USFiHtXLU5";
  const pricePerMonth = ethers.utils.parseEther('0.5'); // 0.5 ETH per month
  const securityDeposit = ethers.utils.parseEther('1'); // 1 ETH security deposit
  const rentalDuration = 3; // 3 months

  beforeEach(async function () {
    // Get contract factory and signers
    SmartRent = await ethers.getContractFactory('SmartRent');
    [owner, landlord, tenant, ...addrs] = await ethers.getSigners();

    // Deploy the contract
    smartRent = await SmartRent.deploy();
    await smartRent.deployed();
  });

  describe('Deployment', function () {
    it('Should set the right owner', async function () {
      expect(await smartRent.owner()).to.equal(owner.address);
    });

    it('Should start with zero properties', async function () {
      expect(await smartRent.getPropertyCount()).to.equal(0);
    });
  });

  describe('Property Listing', function () {
    it('Should allow listing a property', async function () {
      // List a property as the landlord
      await smartRent.connect(landlord).listProperty(
        metadataURI,
        pricePerMonth,
        securityDeposit
      );

      // Check property count
      expect(await smartRent.getPropertyCount()).to.equal(1);

      // Get the property info
      const property = await smartRent.properties(0);
      expect(property.owner).to.equal(landlord.address);
      expect(property.pricePerMonth).to.equal(pricePerMonth);
      expect(property.securityDeposit).to.equal(securityDeposit);
      expect(property.metadataURI).to.equal(metadataURI);
      expect(property.isRented).to.equal(false);
    });

    it('Should emit PropertyListed event when listing a property', async function () {
      await expect(
        smartRent.connect(landlord).listProperty(
          metadataURI,
          pricePerMonth,
          securityDeposit
        )
      )
        .to.emit(smartRent, 'PropertyListed')
        .withArgs(0, landlord.address, pricePerMonth, metadataURI);
    });

    it('Should not allow listing a property with zero price', async function () {
      await expect(
        smartRent.connect(landlord).listProperty(
          metadataURI,
          0,
          securityDeposit
        )
      ).to.be.revertedWith('Price must be greater than zero');
    });
  });

  describe('Property Rental', function () {
    beforeEach(async function () {
      // List a property first
      await smartRent.connect(landlord).listProperty(
        metadataURI,
        pricePerMonth,
        securityDeposit
      );
    });

    it('Should allow renting a property', async function () {
      const totalAmount = pricePerMonth.mul(rentalDuration).add(securityDeposit);

      // Rent the property as the tenant
      await smartRent.connect(tenant).rentProperty(0, rentalDuration, {
        value: totalAmount
      });

      // Check property status
      const property = await smartRent.properties(0);
      expect(property.isRented).to.equal(true);

      // Check rental details
      const rental = await smartRent.getRental(0);
      expect(rental.tenant).to.equal(tenant.address);
      expect(rental.startTime).to.not.equal(0);
      expect(rental.duration).to.equal(rentalDuration);
    });

    it('Should emit PropertyRented event when renting a property', async function () {
      const totalAmount = pricePerMonth.mul(rentalDuration).add(securityDeposit);

      await expect(
        smartRent.connect(tenant).rentProperty(0, rentalDuration, {
          value: totalAmount
        })
      ).to.emit(smartRent, 'PropertyRented');
    });

    it('Should not allow renting with insufficient funds', async function () {
      const insufficientAmount = pricePerMonth.mul(rentalDuration); // Missing security deposit

      await expect(
        smartRent.connect(tenant).rentProperty(0, rentalDuration, {
          value: insufficientAmount
        })
      ).to.be.revertedWith('Insufficient payment amount');
    });

    it('Should not allow renting an already rented property', async function () {
      const totalAmount = pricePerMonth.mul(rentalDuration).add(securityDeposit);

      // First tenant rents the property
      await smartRent.connect(tenant).rentProperty(0, rentalDuration, {
        value: totalAmount
      });

      // Second tenant tries to rent the same property
      await expect(
        smartRent.connect(addrs[0]).rentProperty(0, rentalDuration, {
          value: totalAmount
        })
      ).to.be.revertedWith('Property is already rented');
    });
  });

  describe('Rental Completion', function () {
    beforeEach(async function () {
      // List a property
      await smartRent.connect(landlord).listProperty(
        metadataURI,
        pricePerMonth,
        securityDeposit
      );

      // Rent the property
      const totalAmount = pricePerMonth.mul(rentalDuration).add(securityDeposit);
      await smartRent.connect(tenant).rentProperty(0, rentalDuration, {
        value: totalAmount
      });
    });

    it('Should allow landlord to complete a rental', async function () {
      // Move time forward to after rental period
      await ethers.provider.send('evm_increaseTime', [rentalDuration * 30 * 24 * 60 * 60]);
      await ethers.provider.send('evm_mine');

      // Complete the rental
      await smartRent.connect(landlord).completeRental(0);

      // Check property status
      const property = await smartRent.properties(0);
      expect(property.isRented).to.equal(false);
    });

    it('Should emit RentalCompleted event when completing a rental', async function () {
      // Move time forward
      await ethers.provider.send('evm_increaseTime', [rentalDuration * 30 * 24 * 60 * 60]);
      await ethers.provider.send('evm_mine');

      await expect(
        smartRent.connect(landlord).completeRental(0)
      ).to.emit(smartRent, 'RentalCompleted').withArgs(0);
    });

    it('Should not allow non-owner to complete a rental', async function () {
      await expect(
        smartRent.connect(tenant).completeRental(0)
      ).to.be.revertedWith('Only the property owner can complete a rental');
    });

    it('Should return security deposit to tenant on completion', async function () {
      // Get tenant balance before
      const balanceBefore = await ethers.provider.getBalance(tenant.address);

      // Move time forward
      await ethers.provider.send('evm_increaseTime', [rentalDuration * 30 * 24 * 60 * 60]);
      await ethers.provider.send('evm_mine');

      // Complete rental
      await smartRent.connect(landlord).completeRental(0);

      // Get tenant balance after
      const balanceAfter = await ethers.provider.getBalance(tenant.address);

      // Check that tenant received security deposit back
      expect(balanceAfter.sub(balanceBefore)).to.be.closeTo(
        securityDeposit,
        ethers.utils.parseEther('0.01') // Allow for small differences due to gas costs
      );
    });
  });

  describe('Funds Withdrawal', function () {
    beforeEach(async function () {
      // List a property
      await smartRent.connect(landlord).listProperty(
        metadataURI,
        pricePerMonth,
        securityDeposit
      );

      // Rent the property
      const totalAmount = pricePerMonth.mul(rentalDuration).add(securityDeposit);
      await smartRent.connect(tenant).rentProperty(0, rentalDuration, {
        value: totalAmount
      });
    });

    it('Should allow landlord to withdraw rental funds', async function () {
      // Get landlord balance before
      const balanceBefore = await ethers.provider.getBalance(landlord.address);

      // Withdraw funds
      const tx = await smartRent.connect(landlord).withdrawFunds();
      const receipt = await tx.wait();
      const gasCost = receipt.gasUsed.mul(receipt.effectiveGasPrice);

      // Get landlord balance after
      const balanceAfter = await ethers.provider.getBalance(landlord.address);

      // Calculate expected amount (rental payment without security deposit)
      const expectedAmount = pricePerMonth.mul(rentalDuration);

      // Check that landlord received rental payment
      // Balance difference should be expected amount minus gas costs
      expect(balanceAfter.add(gasCost).sub(balanceBefore)).to.equal(expectedAmount);
    });

    it('Should emit PaymentReceived event when withdrawing funds', async function () {
      await expect(
        smartRent.connect(landlord).withdrawFunds()
      ).to.emit(smartRent, 'PaymentReceived');
    });

    it('Should not allow withdrawal if no funds are available', async function () {
      // Withdraw funds first time
      await smartRent.connect(landlord).withdrawFunds();

      // Try to withdraw again
      await expect(
        smartRent.connect(landlord).withdrawFunds()
      ).to.be.revertedWith('No funds available for withdrawal');
    });
  });

  describe('Emergency Functions', function () {
    it('Should allow owner to trigger emergency stop', async function () {
      await smartRent.connect(owner).triggerEmergencyStop("Security vulnerability detected");
      
      // Try to list a property after emergency stop
      await expect(
        smartRent.connect(landlord).listProperty(
          metadataURI,
          pricePerMonth,
          securityDeposit
        )
      ).to.be.revertedWith('Contract is in emergency stop mode');
    });

    it('Should emit ContractEmergency event when emergency stop is triggered', async function () {
      const reason = "Security vulnerability detected";
      await expect(
        smartRent.connect(owner).triggerEmergencyStop(reason)
      ).to.emit(smartRent, 'ContractEmergency').withArgs(reason);
    });

    it('Should not allow non-owner to trigger emergency stop', async function () {
      await expect(
        smartRent.connect(landlord).triggerEmergencyStop("Unauthorized attempt")
      ).to.be.revertedWith('Ownable: caller is not the owner');
    });

    it('Should allow owner to resume from emergency stop', async function () {
      // Trigger emergency stop
      await smartRent.connect(owner).triggerEmergencyStop("Test emergency");
      
      // Resume operations
      await smartRent.connect(owner).resumeFromEmergencyStop();
      
      // Should be able to list a property now
      await smartRent.connect(landlord).listProperty(
        metadataURI,
        pricePerMonth,
        securityDeposit
      );
      
      expect(await smartRent.getPropertyCount()).to.equal(1);
    });
  });
}); 