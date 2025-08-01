#!/usr/bin/env python3
"""
Production NFT Minter for AlgoRewards
Creates and manages POAP-style NFT badges for event attendance
"""

import os
import json
import hashlib
import time
from typing import Dict, Any, Optional
from algosdk import transaction, account, mnemonic
from algokit_utils import AlgorandClient


class AlgoRewardsNFTMinter:
    """Production-ready NFT minter for AlgoRewards badges"""
    
    def __init__(self):
        """Initialize the NFT minter with Algorand client"""
        self.algorand = AlgorandClient.from_environment()
        self.algod_client = self.algorand.algod_client
        
        # Load deployer account
        deployer_mnemonic = os.getenv('DEPLOYER_MNEMONIC')
        if not deployer_mnemonic:
            raise ValueError("DEPLOYER_MNEMONIC not set in environment")
        
        self.private_key = mnemonic.to_private_key(deployer_mnemonic)
        self.address = account.address_from_private_key(self.private_key)
    
    def create_badge_metadata(
        self, 
        session_name: str, 
        session_id: str,
        recipient_address: str,
        custom_properties: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create ARC-3 compliant metadata for badge NFT
        
        Args:
            session_name: Name of the learning session
            session_id: Unique session identifier
            recipient_address: Badge recipient's address
            custom_properties: Optional custom properties
            
        Returns:
            ARC-3 compliant metadata dictionary
        """
        base_metadata = {
            "name": f"AlgoRewards Badge - {session_name}",
            "description": f"Proof of attendance for '{session_name}' learning session. This badge certifies successful completion of educational milestones in the Algorand ecosystem.",
            "image": "https://via.placeholder.com/400x400/4F46E5/FFFFFF?text=AlgoRewards+Badge",
            "image_mimetype": "image/png",
            "background_color": "4F46E5",
            "external_url": "https://algorand.org",
            "properties": {
                "category": "Education",
                "type": "POAP",
                "issuer": "AlgoRewards Platform",
                "session": session_name,
                "session_id": session_id,
                "recipient": recipient_address,
                "date_issued": time.strftime("%Y-%m-%d"),
                "network": "Algorand",
                "standard": "ARC-3",
                "traits": [
                    {
                        "trait_type": "Achievement",
                        "value": "Session Complete"
                    },
                    {
                        "trait_type": "Session",
                        "value": session_name
                    },
                    {
                        "trait_type": "Date",
                        "value": time.strftime("%Y-%m-%d")
                    },
                    {
                        "trait_type": "Platform",
                        "value": "AlgoRewards"
                    }
                ]
            }
        }
        
        # Add custom properties if provided
        if custom_properties:
            base_metadata["properties"].update(custom_properties)
        
        return base_metadata
    
    def compute_metadata_hash(self, metadata: Dict[str, Any]) -> bytes:
        """
        Compute ARC-19 compliant metadata hash
        
        Args:
            metadata: Metadata dictionary
            
        Returns:
            SHA-256 hash of metadata as bytes
        """
        metadata_json = json.dumps(metadata, separators=(',', ':'), sort_keys=True)
        return hashlib.sha256(metadata_json.encode()).digest()
    
    def mint_badge_nft(
        self, 
        session_name: str,
        session_id: str, 
        recipient_address: str,
        metadata_url: str,
        custom_properties: Optional[Dict[str, Any]] = None
    ) -> int:
        """
        Mint a badge NFT for session completion
        
        Args:
            session_name: Name of the learning session
            session_id: Unique session identifier
            recipient_address: Address to receive the badge
            metadata_url: IPFS URL for metadata JSON
            custom_properties: Optional custom metadata properties
            
        Returns:
            Asset ID of the created NFT
        """
        # Create metadata
        metadata = self.create_badge_metadata(
            session_name, session_id, recipient_address, custom_properties
        )
        metadata_hash = self.compute_metadata_hash(metadata)
        
        # NFT parameters
        asset_name = f"AlgoRewards Badge"  # Keep it simple for wallet display
        unit_name = "ARBADGE"
        total = 1
        decimals = 0
        default_frozen = False  # Allow transfers
        
        # Get transaction parameters
        params = self.algod_client.suggested_params()
        
        # Create asset creation transaction
        txn = transaction.AssetCreateTxn(
            sender=self.address,
            sp=params,
            total=total,
            decimals=decimals,
            default_frozen=default_frozen,
            manager=self.address,
            reserve=self.address,
            freeze=self.address,
            clawback=self.address,
            unit_name=unit_name,
            asset_name=asset_name,
            url=metadata_url,
            metadata_hash=metadata_hash
        )
        
        # Sign and send transaction
        signed_txn = txn.sign(self.private_key)
        txid = self.algod_client.send_transaction(signed_txn)
        
        # Wait for confirmation
        result = transaction.wait_for_confirmation(self.algod_client, txid, 5)
        asset_id = result['asset-index']
        
        # Transfer to recipient if different from creator
        if recipient_address != self.address:
            self._transfer_nft_to_recipient(asset_id, recipient_address)
        
        return asset_id
    
    def _transfer_nft_to_recipient(self, asset_id: int, recipient_address: str):
        """
        Transfer NFT to recipient (requires recipient to opt-in first)
        
        Args:
            asset_id: Asset ID of the NFT
            recipient_address: Recipient's address
        """
        # Note: In production, recipient should opt-in first
        # This is a simplified version
        params = self.algod_client.suggested_params()
        
        # Create transfer transaction
        transfer_txn = transaction.AssetTransferTxn(
            sender=self.address,
            sp=params,
            receiver=recipient_address,
            amt=1,
            index=asset_id
        )
        
        # Sign and send
        signed_txn = transfer_txn.sign(self.private_key)
        txid = self.algod_client.send_transaction(signed_txn)
        
        # Wait for confirmation
        transaction.wait_for_confirmation(self.algod_client, txid, 5)


def main():
    """Example usage"""
    try:
        minter = AlgoRewardsNFTMinter()
        
        # Example: mint a badge
        asset_id = minter.mint_badge_nft(
            session_name="Algorand Smart Contracts 101",
            session_id="algo-sc-001",
            recipient_address=minter.address,  # Mint to self for testing
            metadata_url="https://bafkreihddthm5xr6n5fhtyg3kv4vd2wwfhewgm4j3qamynwc4f4k7tiwoa.ipfs.nftstorage.link/",
            custom_properties={
                "difficulty": "Beginner",
                "duration_hours": 2
            }
        )
        
        print(f"✅ Badge NFT minted successfully!")
        print(f"   Asset ID: {asset_id}")
        print(f"   Explorer: https://testnet.explorer.perawallet.app/asset/{asset_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()