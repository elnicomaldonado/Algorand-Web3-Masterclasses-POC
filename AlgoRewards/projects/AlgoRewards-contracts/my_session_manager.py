#!/usr/bin/env python3
"""
Personal AlgoRewards Session Manager
Easy tool for creating sessions and minting badges
"""

import algokit_utils
from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import AlgoRewardsContractFactory
import time
import sys

def get_app_client():
    """Get connected app client"""
    algorand = algokit_utils.AlgorandClient.from_environment()
    deployer = algorand.account.from_environment('DEPLOYER')
    
    factory = AlgoRewardsContractFactory(
        algorand=algorand,
        default_sender=deployer.address
    )
    
    return factory.get_app_client_by_id(app_id=743654314), deployer.address

def create_session(session_name, description, custom_id=None):
    """Create a new session"""
    app_client, your_address = get_app_client()
    
    # Generate session ID if not provided
    if custom_id:
        session_id = custom_id
    else:
        session_id = f"session-{int(time.time())}"
    
    metadata_url = f"ipfs://QmMetadata{session_id}Hash"
    
    print(f"🎯 Creating Session: {session_name}")
    print(f"📝 Session ID: {session_id}")
    print(f"📝 Description: {description}")
    print()
    
    # Create session
    response = app_client.send.create_session(args=(
        session_id,
        session_name,
        description,
        metadata_url
    ))
    
    print("✅ SESSION CREATED!")
    print(f"📄 Transaction: https://testnet.algoexplorer.io/tx/{response.tx_id}")
    print(f"💡 Use this Session ID to claim badges: {session_id}")
    print()
    
    return session_id

def claim_badge(session_id, badge_name=None, recipient=None):
    """Claim a badge for a session"""
    app_client, your_address = get_app_client()
    
    if not badge_name:
        badge_name = f"Badge for {session_id}"
    
    if not recipient:
        recipient = your_address
    
    asset_unit = f"BADGE{int(time.time()) % 10000}"
    metadata_url = f"ipfs://QmBadgeMetadata{session_id}Hash"
    
    print(f"🏆 Claiming Badge: {badge_name}")
    print(f"🎫 Session ID: {session_id}")
    print(f"👤 Recipient: {recipient}")
    print()
    
    # Claim badge
    response = app_client.send.claim_badge(args=(
        session_id,
        recipient,
        badge_name,
        asset_unit,
        metadata_url
    ))
    
    print("✅ BADGE CLAIMED!")
    print(f"📄 Transaction: https://testnet.algoexplorer.io/tx/{response.tx_id}")
    print(f"🎉 Response: {response.abi_return}")
    print()

def interactive_mode():
    """Interactive session manager"""
    print("🎮 AlgoRewards Interactive Session Manager")
    print("=" * 50)
    
    while True:
        print("\nWhat would you like to do?")
        print("1. Create a new session")
        print("2. Claim a badge")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            print("\n📝 Creating New Session")
            print("-" * 30)
            session_name = input("Session name: ").strip()
            description = input("Description: ").strip()
            custom_id = input("Custom session ID (press Enter for auto): ").strip()
            
            if custom_id == "":
                custom_id = None
                
            session_id = create_session(session_name, description, custom_id)
            
        elif choice == "2":
            print("\n🏆 Claiming Badge")
            print("-" * 20)
            session_id = input("Session ID: ").strip()
            badge_name = input("Badge name (optional): ").strip()
            
            if badge_name == "":
                badge_name = None
                
            claim_badge(session_id, badge_name)
            
        elif choice == "3":
            print("\n👋 Goodbye!")
            break
            
        else:
            print("❌ Invalid choice. Please try again.")

def main():
    """Main function"""
    if len(sys.argv) == 1:
        # Interactive mode
        interactive_mode()
    elif sys.argv[1] == "create":
        # Command line session creation
        if len(sys.argv) < 4:
            print("Usage: python my_session_manager.py create <session_name> <description>")
            return
        
        session_name = sys.argv[2]
        description = sys.argv[3]
        create_session(session_name, description)
        
    elif sys.argv[1] == "claim":
        # Command line badge claim
        if len(sys.argv) < 3:
            print("Usage: python my_session_manager.py claim <session_id> [badge_name]")
            return
        
        session_id = sys.argv[2]
        badge_name = sys.argv[3] if len(sys.argv) > 3 else None
        claim_badge(session_id, badge_name)
        
    else:
        print("Commands:")
        print("  python my_session_manager.py                    # Interactive mode")
        print("  python my_session_manager.py create <name> <desc>  # Create session")
        print("  python my_session_manager.py claim <session_id>    # Claim badge")

if __name__ == "__main__":
    main()