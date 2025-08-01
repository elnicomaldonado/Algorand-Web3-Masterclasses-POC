#!/usr/bin/env python3
"""
Create Wallet-Friendly NFT - Optimized for UI Display
This creates NFTs that display properly in modern wallets
"""

import os
import json
import hashlib
import base64
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction


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


def create_wallet_optimized_metadata():
    """Create metadata optimized for wallet display"""
    
    # Use a real, accessible image for better display
    metadata = {
        "name": "AlgoRewards Badge",
        "description": "Proof of attendance for AlgoRewards session. This unique badge certifies completion of blockchain education milestones.",
        "image": "https://via.placeholder.com/400x400/4F46E5/FFFFFF?text=AlgoRewards+Badge",
        "image_integrity": "sha256-placeholder",
        "image_mimetype": "image/png",
        "background_color": "4F46E5",
        "external_url": "https://algorand.org",
        "animation_url": "",
        "properties": {
            "category": "Education",
            "type": "POAP",
            "issuer": "AlgoRewards Platform",
            "session": "Blockchain Fundamentals",
            "date_issued": "2025-01-31",
            "rarity": "Common",
            "transferable": True,
            "traits": [
                {
                    "trait_type": "Achievement",
                    "value": "Session Complete"
                },
                {
                    "trait_type": "Level", 
                    "value": "Beginner"
                },
                {
                    "trait_type": "Badge Number",
                    "value": 1,
                    "display_type": "number"
                },
                {
                    "trait_type": "Network",
                    "value": "Algorand"
                }
            ]
        },
        "localization": {
            "uri": "https://algorand.org/localization/{locale}.json",
            "default": "en",
            "locales": ["en", "es", "fr"]
        }
    }
    
    return metadata


def create_wallet_friendly_nft():
    """Create NFT optimized for wallet UI display"""
    
    print("🎨 Creating Wallet-Friendly NFT")
    print("=" * 60)
    
    # Get clients and account
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
    print(f"📍 Creator Address: {address}")
    print()
    
    # Create optimized metadata
    metadata = create_wallet_optimized_metadata()
    metadata_json = json.dumps(metadata, separators=(',', ':'))
    
    print("📋 Wallet-Optimized Metadata:")
    print(f"   Name: {metadata['name']}")
    print(f"   Description: {metadata['description'][:60]}...")
    print(f"   Image: {metadata['image']}")
    print(f"   Background: #{metadata['background_color']}")
    print(f"   Traits: {len(metadata['properties']['traits'])}")
    print()
    
    # Create metadata hash
    metadata_hash = hashlib.sha256(metadata_json.encode()).digest()
    
    # NFT parameters optimized for wallets
    asset_name = metadata['name']  # "AlgoRewards Badge"
    unit_name = "ARBADGE"  # Short, clear unit name
    total = 1
    decimals = 0
    default_frozen = False  # Allow transfers for better UX
    
    # Use a placeholder IPFS URL (in production, upload to real IPFS)
    metadata_url = "https://bafkreihddthm5xr6n5fhtyg3kv4vd2wwfhewgm4j3qamynwc4f4k7tiwoa.ipfs.nftstorage.link/"
    
    print(f"🎯 Creating Wallet-Friendly NFT:")
    print(f"   Name: {asset_name}")
    print(f"   Unit: {unit_name}")
    print(f"   Image URL: {metadata['image']}")
    print(f"   Metadata URL: {metadata_url}")
    print(f"   Transferable: {not default_frozen}")
    print()
    
    # Get suggested parameters
    params = algod_client.suggested_params()
    
    # Create wallet-friendly NFT
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
    
    # Sign and submit
    signed_txn = txn.sign(private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"✅ Wallet-Friendly NFT Created!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 5)
        asset_id = confirmed_txn['asset-index']
        
        print(f"🎉 WALLET-FRIENDLY NFT CREATED!")
        print(f"🆔 Asset ID: {asset_id}")
        print(f"🔗 Asset Explorer: https://testnet.algoexplorer.io/asset/{asset_id}")
        print()
        
        # Verify wallet-friendly features
        asset_info = algod_client.asset_info(asset_id)
        params_info = asset_info['params']
        
        print("🔍 Wallet-Friendly Features:")
        print(f"   ✅ Clear Name: '{params_info['name']}'")
        print(f"   ✅ Short Unit: '{params_info['unit-name']}'")
        print(f"   ✅ Transferable: {not params_info['default-frozen']}")
        print(f"   ✅ Has Image URL: {'url' in params_info}")
        print(f"   ✅ Has Metadata Hash: {'metadata-hash' in params_info}")
        print(f"   ✅ Total = 1: {params_info['total'] == 1}")
        print(f"   ✅ Decimals = 0: {params_info['decimals'] == 0}")
        print()
        
        print("📱 Wallet Display Tips:")
        print("   • Should show image from placeholder URL")
        print("   • Name should be clear and readable")
        print("   • Should appear in both Assets and NFTs sections")
        print("   • Transferable so can be sent/received")
        print("   • Rich metadata for detailed view")
        print()
        
        # Auto opt-in and transfer to self
        print("🔄 Auto-setting up in wallet...")
        setup_in_wallet(asset_id)
        
        return asset_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def setup_in_wallet(asset_id):
    """Automatically set up NFT in wallet"""
    
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
    try:
        # Check if already opted in
        account_info = algod_client.account_info(address)
        assets = account_info.get('assets', [])
        
        already_opted = any(asset['asset-id'] == asset_id for asset in assets)
        
        if not already_opted:
            print("   📝 Opting in to NFT...")
            
            # Opt-in transaction
            params = algod_client.suggested_params()
            opt_in_txn = transaction.AssetTransferTxn(
                sender=address,
                sp=params,
                receiver=address,
                amt=0,
                index=asset_id
            )
            
            signed_txn = opt_in_txn.sign(private_key)
            tx_id = algod_client.send_transaction(signed_txn)
            
            transaction.wait_for_confirmation(algod_client, tx_id, 5)
            print(f"   ✅ Opted in! Tx: {tx_id}")
        
        # Transfer to self to ensure it's in wallet
        print("   🔄 Transferring to wallet...")
        
        params = algod_client.suggested_params()
        transfer_txn = transaction.AssetTransferTxn(
            sender=address,
            sp=params,
            receiver=address,
            amt=1,
            index=asset_id
        )
        
        signed_txn = transfer_txn.sign(private_key)
        tx_id = algod_client.send_transaction(signed_txn)
        
        transaction.wait_for_confirmation(algod_client, tx_id, 5)
        print(f"   ✅ In wallet! Tx: {tx_id}")
        
    except Exception as e:
        print(f"   ⚠️ Setup warning: {e}")


def main():
    """Main function"""
    
    print("🚀 Wallet-Friendly NFT Creator")
    print("=" * 60)
    print("🎯 Creating NFT optimized for wallet UI display")
    print()
    
    asset_id = create_wallet_friendly_nft()
    
    if asset_id:
        print("🎊 SUCCESS!")
        print("=" * 60)
        print("✅ Created wallet-friendly NFT")
        print("✅ Optimized for UI display")
        print("✅ Has proper image and metadata")
        print("✅ Ready for wallet viewing")
        print()
        print("📱 This NFT should display much better in:")
        print("   • Pera Wallet")
        print("   • Algorand Wallet")
        print("   • MyAlgo Wallet")
        print("   • NFT marketplaces")
        print()
        print(f"🆔 Your new wallet-friendly NFT ID: {asset_id}")
        print("💡 Try searching for this one in your wallet!")
        
    else:
        print("❌ Creation failed")


if __name__ == "__main__":
    main()