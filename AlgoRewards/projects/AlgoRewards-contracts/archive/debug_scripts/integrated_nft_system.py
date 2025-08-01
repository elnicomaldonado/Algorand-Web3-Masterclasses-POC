#!/usr/bin/env python3
"""
Integrated AlgoRewards System - Smart Contract + Real NFT Creation
This combines smart contract validation with real NFT creation
"""

import os
from algosdk.v2client import algod
from algosdk import account, mnemonic, transaction
import algokit_utils
from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import AlgoRewardsContractFactory
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


def validate_with_smart_contract(session_id, session_name, asset_name):
    """Step 1: Validate the NFT creation with smart contract"""
    
    print("🔐 Step 1: Smart Contract Validation")
    print("-" * 40)
    
    # Connect to AlgoKit
    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer = algorand.account.from_environment('DEPLOYER')
    
    # Connect to Phase 4 contract
    factory = AlgoRewardsContractFactory(
        algorand=algorand,
        default_sender=deployer.address
    )
    app_client = factory.get_app_client_by_id(app_id=743654509)
    
    print(f"✅ Connected to Contract: {app_client.app_id}")
    
    # Call smart contract to validate session
    response = app_client.send.prepare_nft_creation(args=(
        asset_name,
        "BADGE",
        "ipfs://metadata"
    ))
    
    print(f"✅ Contract Validation: {response.abi_return}")
    print(f"📄 Validation Tx: {response.tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{response.tx_id}")
    print()
    
    return True  # Validation successful


def create_real_nft_after_validation(session_id, asset_name, recipient_address):
    """Step 2: Create real NFT after contract validation"""
    
    print("🎨 Step 2: Creating Real NFT")
    print("-" * 40)
    
    # Get clients and account
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
    # NFT parameters based on session (unit name max 8 chars)
    unit_name = f"B{int(time.time()) % 1000000}"[:8]  # Max 8 chars
    total = 1
    decimals = 0
    default_frozen = True
    metadata_url = f"https://ipfs.io/ipfs/QmSession{session_id}Badge"
    
    print(f"🎯 Creating NFT for Session: {session_id}")
    print(f"   Name: {asset_name}")
    print(f"   Unit: {unit_name}")
    print(f"   Recipient: {recipient_address}")
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
        url=metadata_url
    )
    
    # Sign and submit transaction
    signed_txn = txn.sign(private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"✅ Real NFT Creation Submitted!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 5)
    asset_id = confirmed_txn['asset-index']
    
    print(f"🎉 REAL NFT CREATED!")
    print(f"🆔 Asset ID: {asset_id}")
    print(f"🔗 Asset Explorer: https://testnet.algoexplorer.io/asset/{asset_id}")
    print()
    
    return asset_id


def transfer_nft_to_recipient(asset_id, recipient_address):
    """Step 3: Transfer NFT to recipient"""
    
    print("🔄 Step 3: Transferring NFT to Recipient")
    print("-" * 40)
    
    # Get clients and account
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
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
    
    # Sign and submit transaction
    signed_txn = txn.sign(private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"✅ NFT Transfer Submitted!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 5)
    
    print(f"🎉 NFT TRANSFERRED!")
    print(f"👤 New Owner: {recipient_address}")
    print()


def integrated_badge_creation():
    """Complete integrated process: Contract validation + Real NFT creation"""
    
    print("🚀 Integrated AlgoRewards Badge Creation")
    print("=" * 60)
    print("🎯 Contract Validation + Real NFT Creation")
    print()
    
    # Session details
    session_id = f"session-{int(time.time())}"
    session_name = "Real NFT Integration Test"
    asset_name = "AlgoRewards Badge"  # Keep within 32 char limit
    recipient_address = "PA5HR7J45ONH5SA6Q73F3ZCGMWL2NWG5OZAAN7UGHAEGVQTB54SFKSZG4E"
    
    print(f"📝 Session ID: {session_id}")
    print(f"📝 Session: {session_name}")
    print(f"📝 Badge: {asset_name}")
    print(f"📝 Recipient: {recipient_address}")
    print()
    
    try:
        # Step 1: Validate with smart contract
        if validate_with_smart_contract(session_id, session_name, asset_name):
            
            # Step 2: Create real NFT
            asset_id = create_real_nft_after_validation(session_id, asset_name, recipient_address)
            
            # Step 3: Transfer to recipient
            transfer_nft_to_recipient(asset_id, recipient_address)
            
            print("🎊 INTEGRATION COMPLETE!")
            print("=" * 60)
            print("✅ Smart contract validated the request")
            print("✅ Real NFT was created (Asset Creation transaction)")
            print("✅ NFT was transferred to recipient")
            print()
            print("🔍 Check the explorer links above to see:")
            print("   • Contract validation (Application Call)")
            print("   • Asset creation (Asset Creation transaction)")
            print("   • Asset transfer (Asset Transfer transaction)")
            print()
            print("💡 This is the complete AlgoRewards process!")
            
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    integrated_badge_creation()