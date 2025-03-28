@echo off
echo Starting Local Ethereum Node...

cd ethereum

echo Installing dependencies...
call npm install

echo Starting Hardhat node...
call npx hardhat node

echo Ethereum node shutdown. 