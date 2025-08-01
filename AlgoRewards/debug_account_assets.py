#!/usr/bin/env python3
"""
Debug script to check what assets are in your account
"""

import json
from algosdk import mnemonic, account
from algokit_utils import AlgorandClient

def main():
    print("🔍 DEBUGGING ACCOUNT ASSETS")
    print("=" * 50)
    
    # Load environment
    try:
        algorand = AlgorandClient.from_environment()
        algod_client = algorand.algod_client
        print("✅ Connected to Algorand")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return
    
    # You need to provide your mnemonic here
    print("\n⚠️  PLEASE UPDATE THIS SCRIPT WITH YOUR MNEMONIC")
    print("Replace the mnemonic below with your actual wallet mnemonic:")
    
    # Replace this with your actual mnemonic
    mnemonic_phrase = "PUT YOUR 25-WORD MNEMONIC HERE"
    
    if "PUT YOUR" in mnemonic_phrase:
        print("❌ Please update the mnemonic in this script first!")
        return
    
    try:
        private_key = mnemonic.to_private_key(mnemonic_phrase)
        address = account.address_from_private_key(private_key)
        print(f"✅ Using address: {address}")
    except Exception as e:
        print(f"❌ Invalid mnemonic: {e}")
        return
    
    try:
        # Get account information
        account_info = algod_client.account_information(address)
        
        print(f"\n📊 ACCOUNT SUMMARY:")
        print(f"Address: {address}")
        print(f"Balance: {account_info.get('amount', 0) / 1_000_000} ALGO")
        print(f"Total Assets: {len(account_info.get('assets', []))}")
        print(f"Total Created Assets: {len(account_info.get('created-assets', []))}")
        
        # Check owned assets
        assets = account_info.get('assets', [])
        print(f"\n🏦 OWNED ASSETS ({len(assets)}):")
        if assets:
            for asset in assets:
                asset_id = asset['asset-id']
                amount = asset['amount']
                try:
                    asset_info = algod_client.get_asset_by_id(asset_id)
                    params = asset_info['params']
                    print(f"  Asset ID {asset_id}:")
                    print(f"    Name: {params.get('name', 'N/A')}")
                    print(f"    Unit: {params.get('unit-name', 'N/A')}")
                    print(f"    Amount: {amount}")
                    print(f"    Total: {params.get('total', 'N/A')}")
                    print(f"    Decimals: {params.get('decimals', 'N/A')}")
                    print(f"    Creator: {params.get('creator', 'N/A')}")
                    print(f"    Is NFT: {params.get('total') == 1 and params.get('decimals') == 0}")
                    print()
                except Exception as e:
                    print(f"    ❌ Error fetching asset {asset_id}: {e}")
        else:
            print("  No owned assets found")
        
        # Check created assets
        created_assets = account_info.get('created-assets', [])
        print(f"\n🎨 CREATED ASSETS ({len(created_assets)}):")
        if created_assets:
            for asset in created_assets:
                asset_id = asset['index']
                params = asset['params']
                print(f"  Asset ID {asset_id}:")
                print(f"    Name: {params.get('name', 'N/A')}")
                print(f"    Unit: {params.get('unit-name', 'N/A')}")
                print(f"    Total: {params.get('total', 'N/A')}")
                print(f"    Decimals: {params.get('decimals', 'N/A')}")
                print(f"    Creator: {params.get('creator', 'N/A')}")
                print(f"    Is NFT: {params.get('total') == 1 and params.get('decimals') == 0}")
                print(f"    URL: {params.get('url', 'N/A')}")
                print(f"    Metadata Hash: {'Present' if params.get('metadata-hash') else 'None'}")
                print()
        else:
            print("  No created assets found")
        
        # Find NFTs specifically
        all_nfts = []
        
        # From owned assets
        for asset in assets:
            if asset['amount'] > 0:
                try:
                    asset_info = algod_client.get_asset_by_id(asset['asset-id'])
                    params = asset_info['params']
                    if params.get('total') == 1 and params.get('decimals') == 0:
                        all_nfts.append({
                            'id': asset['asset-id'],
                            'name': params.get('name', 'Unnamed'),
                            'source': 'owned'
                        })
                except:
                    pass
        
        # From created assets
        for asset in created_assets:
            params = asset['params']
            if params.get('total') == 1 and params.get('decimals') == 0:
                all_nfts.append({
                    'id': asset['index'],
                    'name': params.get('name', 'Unnamed'),
                    'source': 'created'
                })
        
        print(f"\n🎯 SUMMARY - NFTs FOUND ({len(all_nfts)}):")
        if all_nfts:
            for nft in all_nfts:
                print(f"  ✅ {nft['name']} (ID: {nft['id']}) - {nft['source']}")
                print(f"     Explorer: https://testnet.explorer.perawallet.app/asset/{nft['id']}")
        else:
            print("  ❌ No NFTs found!")
            print("\nPossible reasons:")
            print("  - NFT was created but not yet confirmed")
            print("  - Wrong account/mnemonic")
            print("  - Asset is not actually an NFT (total≠1 or decimals≠0)")
        
    except Exception as e:
        print(f"❌ Error checking account: {e}")

if __name__ == "__main__":
    main()