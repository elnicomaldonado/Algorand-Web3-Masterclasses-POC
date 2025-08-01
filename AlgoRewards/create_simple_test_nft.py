#!/usr/bin/env python3
"""
Create the simplest possible NFT to test detection
"""

import os
from algosdk import transaction, account, mnemonic
from algokit_utils import AlgorandClient

def main():
    print("🧪 Creating SIMPLE TEST NFT")
    print("=" * 40)
    
    # Load environment
    try:
        algorand = AlgorandClient.from_environment()
        algod_client = algorand.algod_client
        print("✅ Connected to Algorand")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return
    
    # Get deployer account from environment
    deployer_mnemonic = os.getenv('DEPLOYER_MNEMONIC')
    if not deployer_mnemonic:
        print("❌ DEPLOYER_MNEMONIC not set in environment")
        return
    
    try:
        private_key = mnemonic.to_private_key(deployer_mnemonic)
        address = account.address_from_private_key(private_key)
        print(f"✅ Using address: {address}")
    except Exception as e:
        print(f"❌ Invalid mnemonic: {e}")
        return
    
    # Super simple NFT parameters
    asset_name = "Test NFT"
    unit_name = "TESTNFT"
    total = 1
    decimals = 0
    default_frozen = False
    
    try:
        # Get transaction parameters
        params = algod_client.suggested_params()
        
        # Create the simplest possible NFT
        txn = transaction.AssetCreateTxn(
            sender=address,
            sp=params,
            total=total,
            decimals=decimals,
            default_frozen=default_frozen,
            manager=address,
            reserve=address,
            freeze=address,
            clawback=address,
            unit_name=unit_name,
            asset_name=asset_name,
            # No URL, no metadata hash
        )
        
        # Sign transaction
        signed_txn = txn.sign(private_key)
        
        # Send transaction
        txid = algod_client.send_transaction(signed_txn)
        print(f"🚀 Simple NFT Transaction: {txid}")
        
        # Wait for confirmation
        result = transaction.wait_for_confirmation(algod_client, txid, 5)
        asset_id = result['asset-index']
        
        print(f"🎉 Simple NFT Created!")
        print(f"   Asset ID: {asset_id}")
        print(f"   Name: {asset_name}")
        print(f"   Unit: {unit_name}")
        print(f"   Explorer: https://testnet.explorer.perawallet.app/asset/{asset_id}")
        
        # Now check the account to see the created asset
        print(f"\n🔍 Checking account...")
        account_info = algod_client.account_information(address)
        created_assets = account_info.get('created-assets', [])
        print(f"Total created assets: {len(created_assets)}")
        
        for asset in created_assets:
            if asset['index'] == asset_id:
                print(f"✅ Found our NFT in created assets!")
                print(f"   Asset ID: {asset['index']}")
                print(f"   Params: {asset['params']}")
                break
        else:
            print(f"❌ NFT not found in created assets")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()