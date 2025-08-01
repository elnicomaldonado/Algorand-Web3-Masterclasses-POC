#!/usr/bin/env python3
"""
Real NFT Creation Script for AlgoRewards
This script demonstrates how to create real NFTs using the Algorand SDK
"""

import algokit_utils
from algosdk import account, mnemonic
from algosdk import transaction
from algosdk.v2client import algod
import json
import time


def create_real_nft():
    """Create a real NFT using the Algorand SDK"""
    
    print("🎨 Creating Real NFT with Algorand SDK")
    print("=" * 50)
    
    # Connect to Algorand
    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer = algorand.account.from_environment('DEPLOYER')
    
    print(f"📍 Your Address: {deployer.address}")
    print()
    
    # NFT parameters
    asset_name = "AlgoRewards Badge"
    asset_unit = "BADGE"
    metadata_url = "ipfs://QmYourMetadataHash"
    
    print(f"🎯 Creating NFT: {asset_name} ({asset_unit})")
    print(f"📝 Metadata URL: {metadata_url}")
    print()
    
    # Get suggested parameters
    params = algorand.algod_client.suggested_params()
    
    # Create asset creation transaction
    txn = transaction.AssetCreateTxn(
        sender=deployer.address,
        sp=params,
        total=1,
        decimals=0,
        default_frozen=True,
        manager=deployer.address,
        reserve=deployer.address,
        freeze=deployer.address,
        clawback=deployer.address,
        unit_name=asset_unit,
        asset_name=asset_name,
        url=metadata_url
    )
    
    # Sign and submit transaction
    signed_txn = txn.sign(deployer.private_key)
    tx_id = algorand.algod_client.send_transaction(signed_txn)
    
    print(f"✅ NFT Creation Transaction Submitted!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    confirmed_txn = transaction.wait_for_confirmation(algorand.algod_client, tx_id, 5)
    
    # Get asset ID
    asset_id = confirmed_txn['asset-index']
    
    print(f"🎉 NFT Created Successfully!")
    print(f"🆔 Asset ID: {asset_id}")
    print(f"🔗 Asset Explorer: https://testnet.algoexplorer.io/asset/{asset_id}")
    print()
    
    # Get asset info
    asset_info = algorand.algod_client.asset_info(asset_id)
    print("📋 Asset Information:")
    print(f"   Name: {asset_info['params']['name']}")
    print(f"   Unit: {asset_info['params']['unit-name']}")
    print(f"   URL: {asset_info['params']['url']}")
    print(f"   Total Supply: {asset_info['params']['total']}")
    print(f"   Decimals: {asset_info['params']['decimals']}")
    print(f"   Default Frozen: {asset_info['params']['default-frozen']}")
    print()
    
    return asset_id


def transfer_nft_to_recipient(asset_id, recipient_address):
    """Transfer NFT to a recipient"""
    
    print(f"🔄 Transferring NFT {asset_id} to {recipient_address}")
    print("=" * 50)
    
    # Connect to Algorand
    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer = algorand.account.from_environment('DEPLOYER')
    
    # Get suggested parameters
    params = algorand.algod.suggested_params()
    
    # Create asset transfer transaction
    txn = transaction.AssetTransferTxn(
        sender=deployer.address,
        sp=params,
        receiver=recipient_address,
        amt=1,
        index=asset_id
    )
    
    # Sign and submit transaction
    signed_txn = txn.sign(deployer.private_key)
    tx_id = algorand.algod.send_transaction(signed_txn)
    
    print(f"✅ NFT Transfer Transaction Submitted!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    confirmed_txn = transaction.wait_for_confirmation(algorand.algod, tx_id, 5)
    
    print(f"🎉 NFT Transferred Successfully!")
    print(f"👤 Recipient: {recipient_address}")
    print(f"🆔 Asset ID: {asset_id}")
    print()


def main():
    """Main function"""
    print("🚀 AlgoRewards Real NFT Creation")
    print("=" * 50)
    print()
    
    # Create the NFT
    asset_id = create_real_nft()
    
    # Ask if user wants to transfer the NFT
    transfer = input("\n🤔 Do you want to transfer this NFT to someone? (y/n): ").strip().lower()
    
    if transfer == 'y':
        recipient = input("👤 Enter recipient address: ").strip()
        if recipient:
            transfer_nft_to_recipient(asset_id, recipient)
    
    print("\n🎉 Real NFT Creation Complete!")
    print("💡 This demonstrates how to create actual NFTs on Algorand")
    print("🔗 You can now see the NFT in your wallet and on the explorer")


if __name__ == "__main__":
    main() 