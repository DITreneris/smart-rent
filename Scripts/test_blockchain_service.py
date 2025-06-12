# Placeholder for BlockchainService test script 

import asyncio
import os
from dotenv import load_dotenv

# Adjust the path to go up one level from scripts to the project root,
# then into the app directory.
# This assumes the script is run from the project root directory.
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_root)

from app.services.blockchain import BlockchainService
from app.core.config import settings # Assuming BlockchainService might use settings

async def main_test():
    print("Loading .env file...")
    # Load .env from the project root, not the scripts directory
    dotenv_path = os.path.join(project_root, '.env')
    load_dotenv(dotenv_path=dotenv_path)
    print(f".env loaded from: {dotenv_path}")
    print(f"RPC URL from settings: {settings.WEB3_PROVIDER_URL}") # Verify .env loaded
    print(f"CONTRACT ADDRESS from settings: {settings.CONTRACT_ADDRESS}") # Verify .env loaded

    try:
        print("\nInitializing BlockchainService...")
        blockchain_service = BlockchainService()
        print("BlockchainService initialized successfully.")

        print("\nGetting platform address...")
        platform_address = await blockchain_service.get_platform_address()
        print(f"Platform Address: {platform_address}")

        print("\nGetting contract instance...")
        contract_instance = await blockchain_service.get_contract()
        if contract_instance:
            print(f"Contract Instance: {contract_instance}")
            print(f"Contract Address from instance: {contract_instance.address}")
        else:
            print("Failed to get contract instance.")

    except ImportError as e:
        print(f"ImportError: {e}. Ensure your PYTHONPATH is set correctly or run from the project root.")
        print("Current sys.path:", sys.path)
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main_test()) 