#!/usr/bin/env python3
"""
Working Real NFT Creation Script for AlgoRewards
This script ACTUALLY creates real NFTs that show as Asset Creation transactions
"""

import os
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import time


def get_algod_client():
    """Get Algod client"""
    algod_address = "https://testnet-api.algonode.cloud"
    algod_token = ""
    return algod.AlgodClient(algod_token, algod_address)


def get_account_from_mnemonic():
    """Get account from mnemonic"""
    mnemonic_phrase = "salt december abuse weather dumb rookie sudden vehicle diary repeat faint unknown taxi stick suit tail file jeans brother hover arrive claw slight abstract capable"
    private_key = mnemonic.to_private_key(mnemonic_phrase)
    address = account.address_from_private_key(private_key)
    return private_key, address


def create_real_nft():
    """Create a REAL NFT that shows as Asset Creation transaction"""
    
    print("🎨 Creating REAL NFT - Asset Creation Transaction")
    print("=" * 60)
    
    # Get clients and account
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
    print(f"📍 Creator Address: {address}")
    print()
    
    # NFT parameters for a real badge
    asset_name = "AlgoRewards Real Badge"
    unit_name = "ARBADGE"
    total = 1  # NFT - only 1 copy
    decimals = 0  # NFT - no decimals
    default_frozen = True  # Non-transferable initially
    metadata_url = "https://ipfs.io/ipfs/QmYourRealMetadataHash"
    # Create a proper 32-byte hash (or set to None to skip)
    metadata_hash = None  # Skip metadata hash for now
    
    print(f"🎯 Creating Real NFT:")
    print(f"   Name: {asset_name}")
    print(f"   Unit: {unit_name}")
    print(f"   Total: {total}")
    print(f"   Decimals: {decimals}")
    print(f"   Default Frozen: {default_frozen}")
    print(f"   URL: {metadata_url}")
    print()
    
    # Get suggested parameters
    params = algod_client.suggested_params()
    
    # Create asset creation transaction
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
        url=metadata_url,
        metadata_hash=metadata_hash
    )
    
    # Sign transaction
    signed_txn = txn.sign(private_key)
    
    # Submit transaction
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"✅ REAL NFT Creation Transaction Submitted!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 5)
        print("✅ Transaction confirmed!")
        
        # Get the asset ID
        asset_id = confirmed_txn['asset-index']
        print(f"🎉 REAL NFT CREATED!")
        print(f"🆔 Asset ID: {asset_id}")
        print(f"🔗 Asset Explorer: https://testnet.algoexplorer.io/asset/{asset_id}")
        print()
        
        # Get asset info to verify
        asset_info = algod_client.asset_info(asset_id)
        print("📋 Real Asset Information:")
        print(f"   ✅ Name: {asset_info['params']['name']}")
        print(f"   ✅ Unit: {asset_info['params']['unit-name']}")
        print(f"   ✅ Total: {asset_info['params']['total']}")
        print(f"   ✅ Decimals: {asset_info['params']['decimals']}")
        print(f"   ✅ Default Frozen: {asset_info['params']['default-frozen']}")
        print(f"   ✅ Creator: {asset_info['params']['creator']}")
        print(f"   ✅ URL: {asset_info['params'].get('url', 'N/A')}")
        print()
        
        return asset_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def transfer_real_nft(asset_id, recipient_address):
    """Transfer the real NFT to a recipient"""
    
    print(f"🔄 Transferring REAL NFT {asset_id} to recipient")
    print("=" * 60)
    
    # Get clients and account
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
    print(f"📍 From: {address}")
    print(f"📍 To: {recipient_address}")
    print(f"🆔 Asset ID: {asset_id}")
    print()
    
    # Get suggested parameters
    params = algod_client.suggested_params()
    
    # Create asset transfer transaction
    txn = transaction.AssetTransferTxn(
        sender=address,
        sp=params,
        receiver=recipient_address,
        amt=1,
        index=asset_id
    )
    
    # Sign transaction
    signed_txn = txn.sign(private_key)
    
    # Submit transaction
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"✅ REAL NFT Transfer Transaction Submitted!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 5)
        print("✅ Transfer confirmed!")
        print(f"🎉 REAL NFT TRANSFERRED!")
        print(f"👤 New Owner: {recipient_address}")
        
    except Exception as e:
        print(f"❌ Transfer Error: {e}")


def main():
    """Main function"""
    print("🚀 AlgoRewards REAL NFT Creation")
    print("=" * 60)
    print("🎯 This will create ACTUAL NFTs that show as Asset Creation!")
    print()
    
    # Create the real NFT
    asset_id = create_real_nft()
    
    if asset_id:
        print("🎉 SUCCESS! You now have a REAL NFT!")
        print("🔍 Check the explorer links above to see:")
        print("   • Asset Creation transaction (not Application Call)")
        print("   • Real asset in the asset explorer")
        print("   • NFT details and metadata")
        print()
        
        # Ask about transfer
        transfer = input("🤔 Transfer this real NFT to someone? (y/n): ").strip().lower()
        if transfer == 'y':
            recipient = input("👤 Enter recipient address: ").strip()
            if recipient:
                transfer_real_nft(asset_id, recipient)
        
        print("\n🎊 REAL NFT CREATION COMPLETE!")
        print("💡 This is how you create actual NFTs on Algorand")
        print("🔗 The transaction shows as 'Asset Creation', not 'Application Call'")
        
    else:
        print("❌ NFT creation failed")


if __name__ == "__main__":
    main()