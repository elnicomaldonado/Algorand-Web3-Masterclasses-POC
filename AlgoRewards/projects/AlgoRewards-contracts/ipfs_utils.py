import json
import requests
from typing import Dict, Any
import os
from datetime import datetime


class IPFSMetadataManager:
    """Utility class for creating and uploading NFT metadata to IPFS"""
    
    def __init__(self, pinata_api_key: str = None, pinata_secret_key: str = None):
        self.pinata_api_key = pinata_api_key or os.getenv('PINATA_API_KEY')
        self.pinata_secret_key = pinata_secret_key or os.getenv('PINATA_SECRET_KEY')
    
    def create_badge_metadata(
        self,
        session_name: str,
        session_description: str,
        session_id: str,
        badge_image_url: str = None,
        attributes: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Create ARC-19 compliant metadata for a badge NFT"""
        
        # Base metadata structure
        metadata = {
            "name": f"AlgoRewards Badge - {session_name}",
            "description": f"Attendance badge for {session_name}. {session_description}",
            "image": badge_image_url or "https://ipfs.io/ipfs/QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme.md",
            "external_url": "https://algorewards.com",
            "attributes": [
                {
                    "trait_type": "Session ID",
                    "value": session_id
                },
                {
                    "trait_type": "Session Name", 
                    "value": session_name
                },
                {
                    "trait_type": "Badge Type",
                    "value": "Attendance"
                },
                {
                    "trait_type": "Minted Date",
                    "value": datetime.now().isoformat()
                },
                {
                    "trait_type": "Non-Transferable",
                    "value": True
                }
            ]
        }
        
        # Add custom attributes if provided
        if attributes:
            for key, value in attributes.items():
                metadata["attributes"].append({
                    "trait_type": key,
                    "value": value
                })
        
        return metadata
    
    def upload_to_ipfs(self, metadata: Dict[str, Any]) -> str:
        """Upload metadata to IPFS using Pinata"""
        if not self.pinata_api_key or not self.pinata_secret_key:
            raise ValueError("Pinata API credentials required for IPFS upload")
        
        headers = {
            'pinata_api_key': self.pinata_api_key,
            'pinata_secret_api_key': self.pinata_secret_key,
            'Content-Type': 'application/json'
        }
        
        # Prepare the data for Pinata
        data = {
            'pinataMetadata': {
                'name': 'AlgoRewards Badge Metadata',
                'keyvalues': {
                    'type': 'nft-metadata',
                    'project': 'algorewards'
                }
            },
            'pinataContent': metadata
        }
        
        try:
            response = requests.post(
                'https://api.pinata.cloud/pinning/pinJSONToIPFS',
                headers=headers,
                json=data
            )
            response.raise_for_status()
            
            result = response.json()
            ipfs_hash = result['IpfsHash']
            
            # Return the IPFS URL
            return f"ipfs://{ipfs_hash}"
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Failed to upload to IPFS: {str(e)}")
    
    def create_and_upload_badge_metadata(
        self,
        session_name: str,
        session_description: str,
        session_id: str,
        badge_image_url: str = None,
        attributes: Dict[str, Any] = None
    ) -> str:
        """Create metadata and upload to IPFS in one step"""
        metadata = self.create_badge_metadata(
            session_name=session_name,
            session_description=session_description,
            session_id=session_id,
            badge_image_url=badge_image_url,
            attributes=attributes
        )
        
        return self.upload_to_ipfs(metadata)


# Example usage
if __name__ == "__main__":
    # Example of creating and uploading metadata
    ipfs_manager = IPFSMetadataManager()
    
    # Create sample metadata
    metadata_url = ipfs_manager.create_and_upload_badge_metadata(
        session_name="Algorand Masterclass",
        session_description="Learn about Algorand smart contracts and NFTs",
        session_id="masterclass-001",
        badge_image_url="https://example.com/badge-image.png",
        attributes={
            "Difficulty": "Intermediate",
            "Duration": "2 hours",
            "Instructor": "AlgoRewards Team"
        }
    )
    
    print(f"Metadata uploaded to IPFS: {metadata_url}") 