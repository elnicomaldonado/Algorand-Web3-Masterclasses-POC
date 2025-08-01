#!/usr/bin/env python3
"""
Production NFT Minter for AlgoRewards
Clean, production-ready NFT creation
"""

import os
import json
import hashlib
import time
from algosdk import transaction, account, mnemonic
from algokit_utils import AlgorandClient


def create_algorewards_nft(session_name: str, recipient_address: str = None):
    """
    Create a clean AlgoRewards NFT badge
    
    Args:
        session_name: Name of the learning session
        recipient_address: Optional recipient (defaults to creator)
    """
    print(f"🎨 Creating AlgoRewards NFT Badge")
    print(f"Session: {session_name}")
    print("=" * 40)
    
    # Load environment
    try:
        algorand = AlgorandClient.from_environment()
        algod_client = algorand.algod_client
        print("✅ Connected to Algorand")
    except Exception as e:
        print(f"❌ Failed to connect: {e}")
        return None
    
    # Load deployer account
    deployer_mnemonic = os.getenv('DEPLOYER_MNEMONIC')
    if not deployer_mnemonic:
        print("❌ DEPLOYER_MNEMONIC not set in environment")
        return None
    
    try:
        private_key = mnemonic.to_private_key(deployer_mnemonic)
        address = account.address_from_private_key(private_key)
        print(f"✅ Using address: {address}")
    except Exception as e:
        print(f"❌ Invalid mnemonic: {e}")
        return None
    
    # Create metadata
    metadata = {
        "name": "AlgoRewards Badge",
        "description": f"Proof of attendance for '{session_name}' learning session.",
        "image": "https://via.placeholder.com/400x400/4F46E5/FFFFFF?text=AlgoRewards+Badge",
        "image_mimetype": "image/png",
        "background_color": "4F46E5",
        "external_url": "https://algorand.org",
        "properties": {
            "category": "Education",
            "type": "POAP", 
            "session": session_name,
            "date_issued": time.strftime("%Y-%m-%d"),
            "traits": [
                {"trait_type": "Achievement", "value": "Session Complete"},
                {"trait_type": "Session", "value": session_name},
                {"trait_type": "Date", "value": time.strftime("%Y-%m-%d")}
            ]
        }
    }
    
    # Create metadata hash
    metadata_json = json.dumps(metadata, separators=(',', ':'), sort_keys=True)
    metadata_hash = hashlib.sha256(metadata_json.encode()).digest()
    
    # NFT parameters
    asset_name = "AlgoRewards Badge"
    unit_name = "ARBADGE"
    total = 1
    decimals = 0
    default_frozen = False
    metadata_url = "https://bafkreihddthm5xr6n5fhtyg3kv4vd2wwfhewgm4j3qamynwc4f4k7tiwoa.ipfs.nftstorage.link/"
    
    try:
        # Get transaction parameters
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
        
        # Sign and send transaction
        signed_txn = txn.sign(private_key)
        txid = algod_client.send_transaction(signed_txn)
        
        # Wait for confirmation
        result = transaction.wait_for_confirmation(algod_client, txid, 5)
        asset_id = result['asset-index']
        
        print(f"🎉 NFT Badge Created Successfully!")
        print(f"   Asset ID: {asset_id}")
        print(f"   Name: {asset_name}")
        print(f"   Session: {session_name}")
        print(f"   Explorer: https://testnet.explorer.perawallet.app/asset/{asset_id}")
        
        return asset_id
        
    except Exception as e:
        print(f"❌ Error creating NFT: {e}")
        return None


if __name__ == "__main__":
    # Example usage
    asset_id = create_algorewards_nft("Algorand Smart Contracts 101")
    if asset_id:
        print(f"\n✅ Success! Check Asset ID {asset_id} in your wallet or explorer.")