#!/usr/bin/env python3
"""
Opt-in to NFT - Required for NFT to show in wallet
On Algorand, you must opt-in to assets before receiving them
"""

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


def check_asset_balance(algod_client, address, asset_id):
    """Check if account has the asset"""
    try:
        account_info = algod_client.account_info(address)
        assets = account_info.get('assets', [])
        
        for asset in assets:
            if asset['asset-id'] == asset_id:
                return asset['amount']
        
        return None  # Asset not found
    
    except Exception as e:
        print(f"Error checking balance: {e}")
        return None


def opt_in_to_asset(asset_id):
    """Opt-in to the NFT asset"""
    
    print("🔗 Opting in to NFT")
    print("=" * 50)
    
    # Get client and account
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
    print(f"📍 Account: {address}")
    print(f"🆔 Asset ID: {asset_id}")
    print()
    
    # Check if already opted in
    balance = check_asset_balance(algod_client, address, asset_id)
    if balance is not None:
        print(f"✅ Already opted in! Balance: {balance}")
        print("🎉 NFT should already be visible in your wallet")
        return True
    
    print("📝 Account not opted in yet, creating opt-in transaction...")
    
    # Get suggested parameters
    params = algod_client.suggested_params()
    
    # Create opt-in transaction (AssetTransfer with amount=0 to self)
    opt_in_txn = transaction.AssetTransferTxn(
        sender=address,
        sp=params,
        receiver=address,  # Send to self
        amt=0,            # Amount = 0 for opt-in
        index=asset_id
    )
    
    # Sign transaction
    signed_txn = opt_in_txn.sign(private_key)
    
    # Submit transaction
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"✅ Opt-in Transaction Submitted!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 5)
        print("✅ Opt-in confirmed!")
        
        # Check balance after opt-in
        new_balance = check_asset_balance(algod_client, address, asset_id)
        if new_balance is not None:
            print(f"🎉 Successfully opted in! Balance: {new_balance}")
            print("💡 NFT should now appear in your wallet!")
        else:
            print("⚠️  Opt-in completed but balance check failed")
        
        return True
        
    except Exception as e:
        print(f"❌ Opt-in failed: {e}")
        return False


def transfer_nft_to_self(asset_id):
    """Transfer the NFT to your own wallet (after opt-in)"""
    
    print("🔄 Transferring NFT to Wallet")
    print("=" * 50)
    
    # Get client and account
    algod_client = get_algod_client()
    private_key, address = get_account_from_mnemonic()
    
    print(f"📍 Transferring NFT to: {address}")
    print(f"🆔 Asset ID: {asset_id}")
    print()
    
    # Get suggested parameters
    params = algod_client.suggested_params()
    
    # Create transfer transaction
    transfer_txn = transaction.AssetTransferTxn(
        sender=address,
        sp=params,
        receiver=address,  # Transfer to self
        amt=1,            # Transfer 1 NFT
        index=asset_id
    )
    
    # Sign transaction
    signed_txn = transfer_txn.sign(private_key)
    
    # Submit transaction
    tx_id = algod_client.send_transaction(signed_txn)
    
    print(f"✅ Transfer Transaction Submitted!")
    print(f"📄 Transaction ID: {tx_id}")
    print(f"🔗 Explorer: https://testnet.algoexplorer.io/tx/{tx_id}")
    print()
    
    # Wait for confirmation
    print("⏳ Waiting for confirmation...")
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 5)
        print("✅ Transfer confirmed!")
        
        # Check final balance
        final_balance = check_asset_balance(algod_client, address, asset_id)
        if final_balance == 1:
            print(f"🎉 NFT successfully in wallet! Balance: {final_balance}")
        else:
            print(f"⚠️  Unexpected balance: {final_balance}")
        
        return True
        
    except Exception as e:
        print(f"❌ Transfer failed: {e}")
        return False


def main():
    """Main function"""
    
    asset_id = 743654858  # Our TRUE NFT
    
    print("🚀 NFT Wallet Setup")
    print("=" * 60)
    print("🎯 Making NFT visible in your wallet")
    print()
    print(f"🆔 NFT Asset ID: {asset_id}")
    print(f"📱 Wallet Address: PA5HR7J45ONH5SA6Q73F3ZCGMWL2NWG5OZAAN7UGHAEGVQTB54SFKSZG4E")
    print()
    
    # Step 1: Opt-in to the asset
    print("Step 1: Opt-in to NFT")
    if opt_in_to_asset(asset_id):
        print()
        
        # Step 2: Transfer NFT to wallet (since we're the creator)
        print("Step 2: Transfer NFT to wallet")
        if transfer_nft_to_self(asset_id):
            print()
            print("🎊 SETUP COMPLETE!")
            print("=" * 60)
            print("✅ Opted in to NFT")
            print("✅ NFT transferred to wallet")
            print("✅ NFT should now be visible!")
            print()
            print("📱 Check your wallet:")
            print("   • Algorand Wallet")
            print("   • Pera Wallet") 
            print("   • MyAlgo Wallet")
            print()
            print("🔍 Or check on explorer:")
            print(f"   https://testnet.algoexplorer.io/asset/{asset_id}")
            
        else:
            print("❌ Transfer failed")
    else:
        print("❌ Opt-in failed")


if __name__ == "__main__":
    main()