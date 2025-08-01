#!/usr/bin/env python3
"""
Production deployment script for AlgoRewards smart contract
"""

import os
from algokit_utils import AlgorandClient
from algosdk import mnemonic, account


def deploy_algorewards_contract():
    """Deploy the production AlgoRewards contract"""
    
    print("🚀 Deploying AlgoRewards Production Contract")
    print("=" * 50)
    
    # Load environment
    try:
        algorand = AlgorandClient.from_environment()
        print("✅ Connected to Algorand network")
    except Exception as e:
        print(f"❌ Failed to connect to Algorand: {e}")
        return None
    
    # Load deployer account
    deployer_mnemonic = os.getenv('DEPLOYER_MNEMONIC')
    if not deployer_mnemonic:
        print("❌ DEPLOYER_MNEMONIC not set in environment")
        return None
    
    try:
        private_key = mnemonic.to_private_key(deployer_mnemonic)
        deployer_address = account.address_from_private_key(private_key)
        print(f"✅ Using deployer address: {deployer_address}")
    except Exception as e:
        print(f"❌ Invalid deployer mnemonic: {e}")
        return None
    
    print("\n📝 Instructions:")
    print("1. Update smart_contracts/algo_rewards_contract/contract.py with production code")
    print("2. Run: algokit project deploy")
    print("3. Update frontend with new App ID")
    
    return True


if __name__ == "__main__":
    deploy_algorewards_contract()