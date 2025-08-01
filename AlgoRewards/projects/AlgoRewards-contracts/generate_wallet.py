#!/usr/bin/env python3
"""
Simple script to generate a new Algorand wallet for TestNet deployment
"""

from algosdk import account, mnemonic

def generate_wallet():
    """Generate a new Algorand wallet and return the address and mnemonic"""
    private_key = account.generate_account()[0]
    address = account.address_from_private_key(private_key)
    mnemonic_phrase = mnemonic.from_private_key(private_key)
    
    print("=== New Algorand Wallet Generated ===")
    print(f"Address: {address}")
    print(f"Mnemonic: {mnemonic_phrase}")
    print("\n⚠️  IMPORTANT: Save this mnemonic securely! You'll need it for deployment.")
    print("💰 You'll need to fund this address with TestNet ALGO before deploying.")
    
    return address, mnemonic_phrase

if __name__ == "__main__":
    generate_wallet() 