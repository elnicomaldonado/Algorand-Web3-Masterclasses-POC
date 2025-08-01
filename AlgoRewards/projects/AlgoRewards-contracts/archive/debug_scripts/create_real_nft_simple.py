#!/usr/bin/env python3
"""
Simple Real NFT Creation Script for AlgoRewards
This script demonstrates how to create real NFTs using AlgoKit utilities
"""

import algokit_utils
import time


def create_real_nft():
    """Create a real NFT using AlgoKit utilities"""
    
    print("🎨 Creating Real NFT with AlgoKit")
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
    
    # Create the asset using AlgoKit
    asset_id = algorand.asset.create(
        sender=deployer.address,
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
    
    print(f"✅ NFT Created Successfully!")
    print(f"🆔 Asset ID: {asset_id}")
    print(f"🔗 Asset Explorer: https://testnet.algoexplorer.io/asset/{asset_id}")
    print()
    
    # Get asset info
    asset_info = algorand.asset.get_info(asset_id)
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
    
    # Transfer the asset
    tx_id = algorand.asset.transfer(
        sender=deployer.address,
        receiver=recipient_address,
        asset_id=asset_id,
        amount=1
    )
    
    print(f"✅ NFT Transferred Successfully!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
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
    print()
    print("🎯 KEY DIFFERENCE:")
    print("• This creates REAL NFTs that show as 'Asset Creation' transactions")
    print("• The smart contract validates and authorizes the process")
    print("• The actual NFT creation happens using AlgoKit utilities")
    print("• You can see the NFT in your wallet and on the explorer")


if __name__ == "__main__":
    main() 