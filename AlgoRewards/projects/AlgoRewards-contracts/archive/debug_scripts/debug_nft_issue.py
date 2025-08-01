#!/usr/bin/env python3
"""
Debug NFT Issue - Check what's happening with the asset
"""

from algosdk.v2client import algod, indexer
from algosdk import account, mnemonic
import requests
import json


def get_clients():
    """Get Algod and Indexer clients"""
    algod_address = "https://testnet-api.algonode.cloud"
    indexer_address = "https://testnet-idx.algonode.cloud"
    token = ""
    
    algod_client = algod.AlgodClient(token, algod_address)
    indexer_client = indexer.IndexerClient(token, indexer_address)
    
    return algod_client, indexer_client


def get_account_from_mnemonic():
    """Get account from mnemonic"""
    mnemonic_phrase = "salt december abuse weather dumb rookie sudden vehicle diary repeat faint unknown taxi stick suit tail file jeans brother hover arrive claw slight abstract capable"
    private_key = mnemonic.to_private_key(mnemonic_phrase)
    address = account.address_from_private_key(private_key)
    return private_key, address


def check_asset_via_multiple_methods(asset_id):
    """Check asset using multiple methods"""
    
    print(f"🔍 Debugging Asset ID: {asset_id}")
    print("=" * 60)
    
    algod_client, indexer_client = get_clients()
    private_key, address = get_account_from_mnemonic()
    
    print(f"📍 Account: {address}")
    print()
    
    # Method 1: Check via Algod
    print("1️⃣ Checking via Algod Client:")
    try:
        asset_info = algod_client.asset_info(asset_id)
        print("✅ Algod: Asset found!")
        print(f"   Name: {asset_info['params']['name']}")
        print(f"   Total: {asset_info['params']['total']}")
        print(f"   Creator: {asset_info['params']['creator']}")
    except Exception as e:
        print(f"❌ Algod: {e}")
    
    print()
    
    # Method 2: Check via Indexer
    print("2️⃣ Checking via Indexer Client:")
    try:
        asset_info = indexer_client.asset_info(asset_id)
        print("✅ Indexer: Asset found!")
        if 'asset' in asset_info:
            params = asset_info['asset']['params']
            print(f"   Name: {params['name']}")
            print(f"   Total: {params['total']}")
            print(f"   Creator: {params['creator']}")
    except Exception as e:
        print(f"❌ Indexer: {e}")
    
    print()
    
    # Method 3: Check via Direct HTTP
    print("3️⃣ Checking via Direct HTTP:")
    try:
        url = f"https://testnet-idx.algonode.cloud/v2/assets/{asset_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'asset' in data:
                print("✅ HTTP: Asset found!")
                params = data['asset']['params']
                print(f"   Name: {params['name']}")
                print(f"   Total: {params['total']}")
                print(f"   Creator: {params['creator']}")
            else:
                print("❌ HTTP: No asset in response")
                print(f"Response: {data}")
        else:
            print(f"❌ HTTP: Status {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ HTTP: {e}")
    
    print()
    
    # Method 4: Check account assets
    print("4️⃣ Checking Account Assets:")
    try:
        account_info = algod_client.account_info(address)
        assets = account_info.get('assets', [])
        print(f"Account has {len(assets)} assets:")
        
        target_found = False
        for asset in assets:
            asset_id_check = asset['asset-id']
            amount = asset['amount']
            print(f"   Asset {asset_id_check}: Balance {amount}")
            
            if asset_id_check == asset_id:
                target_found = True
                print(f"   ✅ Found target asset {asset_id}!")
        
        if not target_found:
            print(f"   ❌ Target asset {asset_id} not found in account")
            
    except Exception as e:
        print(f"❌ Account check: {e}")
    
    print()
    
    # Method 5: Check recent transactions
    print("5️⃣ Checking Recent Transactions:")
    try:
        # Check for asset creation transaction
        tx_id = "655Y5YT3U7CVVEQASMVKVGJNNNEYIL3F7EJXVHRN7G5K4ZCVLN7A"
        print(f"Checking transaction: {tx_id}")
        
        url = f"https://testnet-idx.algonode.cloud/v2/transactions/{tx_id}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if 'transaction' in data:
                tx = data['transaction']
                print("✅ Transaction found!")
                print(f"   Type: {tx.get('tx-type', 'unknown')}")
                print(f"   Round: {tx.get('confirmed-round', 'unknown')}")
                
                # Check for created asset
                if 'created-asset-index' in tx:
                    created_asset = tx['created-asset-index']
                    print(f"   Created Asset: {created_asset}")
                    if created_asset == asset_id:
                        print("   ✅ This matches our target asset!")
                    else:
                        print(f"   ❌ This doesn't match our target ({asset_id})")
                else:
                    print("   ❌ No created-asset-index in transaction")
            else:
                print("❌ No transaction data")
        else:
            print(f"❌ Transaction check failed: {response.status_code}")
    
    except Exception as e:
        print(f"❌ Transaction check: {e}")


def main():
    """Main debugging function"""
    
    asset_id = 743654858  # Our NFT
    
    print("🚀 NFT Asset Debugging")
    print("=" * 60)
    print("🎯 Investigating why asset is not found")
    print()
    
    check_asset_via_multiple_methods(asset_id)
    
    print()
    print("🔍 DEBUGGING COMPLETE")
    print("=" * 60)
    print("💡 If asset is not found via any method:")
    print("   • The asset creation may have failed")
    print("   • There might be a network/sync issue")
    print("   • Asset ID might be incorrect")
    print("   • TestNet data might be delayed")


if __name__ == "__main__":
    main()