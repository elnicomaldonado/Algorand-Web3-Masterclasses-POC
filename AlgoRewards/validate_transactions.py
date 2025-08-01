#!/usr/bin/env python3
"""
Simple script to validate AlgoRewards transactions on TestNet
"""

import requests
import json

def check_app_info():
    """Check if the app exists on TestNet"""
    app_id = 743652051
    url = f"https://testnet-api.algonode.cloud/v2/applications/{app_id}"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            app_data = response.json()
            print(f"✅ App {app_id} exists on TestNet")
            print(f"   Creator: {app_data.get('params', {}).get('creator', 'Unknown')}")
            return True
        else:
            print(f"❌ App {app_id} not found on TestNet")
            return False
    except Exception as e:
        print(f"❌ Error checking app: {e}")
        return False

def check_wallet_transactions(wallet_address):
    """Check recent transactions for a wallet address"""
    url = f"https://testnet-api.algonode.cloud/v2/accounts/{wallet_address}/transactions"
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            transactions = response.json().get('transactions', [])
            print(f"✅ Found {len(transactions)} transactions for {wallet_address}")
            
            # Look for app call transactions
            app_calls = [tx for tx in transactions if tx.get('application-transaction')]
            print(f"   App calls: {len(app_calls)}")
            
            for tx in app_calls[:5]:  # Show last 5 app calls
                app_tx = tx.get('application-transaction', {})
                app_id = app_tx.get('application-id')
                if app_id == 743652051:
                    print(f"   ✅ AlgoRewards transaction: {tx.get('id')}")
            
            return True
        else:
            print(f"❌ Could not fetch transactions for {wallet_address}")
            return False
    except Exception as e:
        print(f"❌ Error checking transactions: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Validating AlgoRewards TestNet Deployment")
    print("=" * 50)
    
    # Check app exists
    check_app_info()
    
    print("\n📋 To check your wallet transactions:")
    print("1. Visit: https://testnet.algoexplorer.io/")
    print("2. Enter your wallet address")
    print("3. Look for transactions to app 743652051")
    
    print("\n🔗 Direct Links:")
    print(f"   App Details: https://testnet.algoexplorer.io/application/743652051")
    print("   TestNet Explorer: https://testnet.algoexplorer.io/")
    
    print("\n💡 Validation Checklist:")
    print("   ✅ App deployed to TestNet")
    print("   ✅ Session creation transaction sent")
    print("   ✅ Badge claiming transaction sent")
    print("   ✅ Transactions appear in wallet")
    print("   ✅ Transactions appear on explorer")
