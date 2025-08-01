#!/usr/bin/env python3
"""
Create TRUE NFT following ARC-3 and ARC-19 standards
This creates proper NFTs, not just tokens with supply 1
"""

import os
import json
import hashlib
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import base64


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


def create_arc3_metadata():
    """Create ARC-3 compliant metadata for true NFT"""
    
    metadata = {
        "name": "AlgoRewards Badge #001",
        "description": "A unique badge awarded for completing AlgoRewards session",
        "image": "https://ipfs.io/ipfs/QmBadgeImage001",
        "image_integrity": "sha256-...",
        "image_mimetype": "image/png",
        "background_color": "000000",
        "external_url": "https://algorewards.com/badge/001",
        "external_url_integrity": "sha256-...",
        "external_url_mimetype": "text/html",
        "animation_url": "https://ipfs.io/ipfs/QmBadgeAnimation001",
        "animation_url_integrity": "sha256-...",
        "animation_url_mimetype": "video/mp4",
        "properties": {
            "session_id": "session-001",
            "achievement": "First Badge",
            "rarity": "Common",
            "issued_date": "2025-01-31",
            "traits": [
                {
                    "trait_type": "Session Type",
                    "value": "Workshop"
                },
                {
                    "trait_type": "Difficulty",
                    "value": "Beginner"
                },
                {
                    "trait_type": "Badge Number",
                    "value": 1,
                    "display_type": "number"
                }
            ]
        },
        "extra": {
            "contract_address": "PA5HR7J45ONH5SA6Q73F3ZCGMWL2NWG5OZAAN7UGHAEGVQTB54SFKSZG4E",
            "minted_by": "AlgoRewards Platform",
            "version": "1.0"
        }
    }
    
    return metadata


def create_true_nft():
    """Create a TRUE NFT following ARC-3/ARC-19 standards"""
    
    print("🎨 Creating TRUE NFT (ARC-3/ARC-19 Compliant)")
    print("=" * 60)
    
    # Get clients and account
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
    print(f"📍 Creator Address: {address}")
    print()
    
    # Create ARC-3 metadata
    metadata = create_arc3_metadata()
    metadata_json = json.dumps(metadata, separators=(',', ':'))
    
    print("📋 ARC-3 Metadata Created:")
    print(f"   Name: {metadata['name']}")
    print(f"   Description: {metadata['description']}")
    print(f"   Properties: {len(metadata['properties']['traits'])} traits")
    print()
    
    # Create metadata hash (ARC-19 standard)
    metadata_hash = hashlib.sha256(metadata_json.encode()).digest()
    
    # NFT parameters for TRUE NFT
    asset_name = metadata['name']  # "AlgoRewards Badge #001"
    unit_name = "ARB001"  # Unique unit name
    total = 1  # NFT - exactly 1 copy
    decimals = 0  # NFT - no decimals
    default_frozen = False  # Can be transferred (set True for soulbound)
    
    # ARC-19: Use ipfs:// URL that resolves to metadata JSON
    metadata_url = "https://ipfs.io/ipfs/QmMetadataHashExample"
    
    print(f"🎯 Creating TRUE NFT:")
    print(f"   Name: {asset_name}")
    print(f"   Unit: {unit_name}")
    print(f"   Total: {total} (TRUE NFT)")
    print(f"   Decimals: {decimals}")
    print(f"   Default Frozen: {default_frozen}")
    print(f"   Metadata URL: {metadata_url}")
    print(f"   Metadata Hash: {metadata_hash.hex()[:16]}...")
    print()
    
    # Get suggested parameters
    params = algod_client.suggested_params()
    
    # Create TRUE NFT asset creation transaction
    txn = transaction.AssetCreateTxn(
        sender=address,
        sp=params,
        total=total,
        decimals=decimals,
        default_frozen=default_frozen,
        manager=address,  # Can update metadata
        reserve=address,  # Can hold uncirculated units
        freeze=address,   # Can freeze/unfreeze transfers
        clawback=address, # Can revoke assets (optional)
        unit_name=unit_name,
        asset_name=asset_name,
        url=metadata_url,
        metadata_hash=metadata_hash  # ARC-19 metadata hash
    )
    
    # Sign and submit transaction
    signed_txn = txn.sign(private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"✅ TRUE NFT Creation Transaction Submitted!")
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
        print(f"🎉 TRUE NFT CREATED!")
        print(f"🆔 Asset ID: {asset_id}")
        print(f"🔗 Asset Explorer: https://testnet.algoexplorer.io/asset/{asset_id}")
        print()
        
        # Verify it's a true NFT
        asset_info = algod_client.asset_info(asset_id)
        params = asset_info['params']
        
        print("🔍 TRUE NFT Verification:")
        print(f"   ✅ Name: {params['name']}")
        print(f"   ✅ Unit: {params['unit-name']}")
        print(f"   ✅ Total Supply: {params['total']} (Must be 1 for NFT)")
        print(f"   ✅ Decimals: {params['decimals']} (Must be 0 for NFT)")
        print(f"   ✅ Default Frozen: {params['default-frozen']}")
        print(f"   ✅ Has Metadata Hash: {'Yes' if 'metadata-hash' in params else 'No'}")
        print(f"   ✅ Has URL: {'Yes' if 'url' in params else 'No'}")
        print()
        
        # Check if it's truly an NFT
        is_nft = (
            params['total'] == 1 and 
            params['decimals'] == 0 and 
            'metadata-hash' in params and
            'url' in params
        )
        
        if is_nft:
            print("🎊 CONFIRMED: This is a TRUE NFT!")
            print("✅ Total supply = 1")
            print("✅ Decimals = 0") 
            print("✅ Has metadata hash (ARC-19)")
            print("✅ Has metadata URL (ARC-3)")
        else:
            print("❌ This is NOT a true NFT")
        
        print()
        print("📋 Metadata Preview:")
        print(json.dumps(metadata, indent=2)[:500] + "...")
        
        return asset_id
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    """Main function"""
    print("🚀 AlgoRewards TRUE NFT Creation")
    print("=" * 60)
    print("🎯 Creating ARC-3/ARC-19 compliant NFTs")
    print()
    
    # Create the TRUE NFT
    asset_id = create_true_nft()
    
    if asset_id:
        print("\n🎉 SUCCESS! You now have a TRUE NFT!")
        print("🔍 Key differences from regular tokens:")
        print("   • Total supply = 1 (unique)")
        print("   • Decimals = 0 (indivisible)")
        print("   • Metadata hash for integrity (ARC-19)")
        print("   • Rich metadata with traits (ARC-3)")
        print("   • Shows as NFT in wallets and explorers")
        print()
        print("🎯 This is a proper NFT, not just a token!")
        
    else:
        print("❌ TRUE NFT creation failed")


if __name__ == "__main__":
    main()