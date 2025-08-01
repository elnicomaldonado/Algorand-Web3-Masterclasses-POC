#!/usr/bin/env python3
"""
Utility script for creating AlgoRewards sessions and managing badge claims
"""

import os
import sys
from dotenv import load_dotenv
from ipfs_utils import IPFSMetadataManager
import algokit_utils

# Load environment variables
load_dotenv()

def create_session_with_metadata(
    session_id: str,
    session_name: str,
    session_description: str,
    badge_image_url: str = None,
    attributes: dict = None
):
    """Create a session with IPFS metadata"""
    
    # Initialize IPFS manager
    ipfs_manager = IPFSMetadataManager()
    
    try:
        # Create and upload metadata to IPFS
        print(f"Creating metadata for session: {session_name}")
        metadata_url = ipfs_manager.create_and_upload_badge_metadata(
            session_name=session_name,
            session_description=session_description,
            session_id=session_id,
            badge_image_url=badge_image_url,
            attributes=attributes
        )
        
        print(f"Metadata uploaded to IPFS: {metadata_url}")
        
        # Initialize Algorand client
        algorand = algokit_utils.AlgorandClient.from_environment()
        deployer = algorand.account.from_environment("DEPLOYER")
        
        # Get app client
        from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import (
            AlgoRewardsContractFactory,
        )
        
        factory = algorand.client.get_typed_app_factory(
            AlgoRewardsContractFactory, default_sender=deployer.address
        )
        
        # Get app client by ID (replace with your actual app ID)
        app_id = int(os.getenv('APP_ID', '743652051'))
        app_client = factory.getAppClientById({"appId": app_id})
        
        # Create session on blockchain
        print(f"Creating session on blockchain...")
        response = app_client.send.create_session(
            args={
                "session_id": session_id,
                "session_name": session_name,
                "session_description": session_description,
                "metadata_url": metadata_url
            }
        )
        
        print(f"Session created successfully!")
        print(f"Session ID: {session_id}")
        print(f"Session Number: {getattr(response, 'return', 'N/A')}")
        print(f"Metadata URL: {metadata_url}")
        
        return metadata_url
        
    except Exception as e:
        print(f"Error creating session: {e}")
        return None

def claim_badge(
    session_id: str,
    recipient_address: str,
    asset_name: str = None,
    asset_unit: str = None,
    metadata_url: str = None
):
    """Claim a badge for a session"""
    
    try:
        # Initialize Algorand client
        algorand = algokit_utils.AlgorandClient.from_environment()
        deployer = algorand.account.from_environment("DEPLOYER")
        
        # Get app client
        from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import (
            AlgoRewardsContractFactory,
        )
        
        factory = algorand.client.get_typed_app_factory(
            AlgoRewardsContractFactory, default_sender=deployer.address
        )
        
        # Get app client by ID
        app_id = int(os.getenv('APP_ID', '743652051'))
        app_client = factory.getAppClientById({"appId": app_id})
        
        # Set default asset name and unit if not provided
        if not asset_name:
            asset_name = f"AlgoRewards Badge - {session_id}"
        if not asset_unit:
            asset_unit = f"BADGE-{session_id}"
        
        # If no metadata URL provided, we need to get it from the session
        if not metadata_url:
            # Get session info to extract metadata URL
            session_info = app_client.send.get_session_info(
                args={"session_id": session_id}
            )
            # Parse session info to get metadata URL
            # This is a simplified approach - in production you'd parse the session data properly
            metadata_url = "ipfs://QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme.md"
        
        print(f"Claiming badge for session: {session_id}")
        print(f"Recipient: {recipient_address}")
        print(f"Asset Name: {asset_name}")
        print(f"Asset Unit: {asset_unit}")
        
        # Claim the badge
        response = app_client.send.claim_badge(
            args={
                "session_id": session_id,
                "recipient_address": recipient_address,
                "asset_name": asset_name,
                "asset_unit": asset_unit,
                "metadata_url": metadata_url
            }
        )
        
        print(f"Badge claimed successfully!")
        print(f"Asset ID: {getattr(response, 'return', 'N/A')}")
        
        return getattr(response, 'return', None)
        
    except Exception as e:
        print(f"Error claiming badge: {e}")
        return None

def main():
    """Main function for command line usage"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python create_session.py create <session_id> <session_name> <description>")
        print("  python create_session.py claim <session_id> <recipient_address>")
        return
    
    command = sys.argv[1]
    
    if command == "create":
        if len(sys.argv) < 5:
            print("Usage: python create_session.py create <session_id> <session_name> <description>")
            return
        
        session_id = sys.argv[2]
        session_name = sys.argv[3]
        description = sys.argv[4]
        
        create_session_with_metadata(
            session_id=session_id,
            session_name=session_name,
            session_description=description
        )
        
    elif command == "claim":
        if len(sys.argv) < 4:
            print("Usage: python create_session.py claim <session_id> <recipient_address>")
            return
        
        session_id = sys.argv[2]
        recipient_address = sys.argv[3]
        
        claim_badge(
            session_id=session_id,
            recipient_address=recipient_address
        )
        
    else:
        print("Unknown command. Use 'create' or 'claim'")

if __name__ == "__main__":
    main() 