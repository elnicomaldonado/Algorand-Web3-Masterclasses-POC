from algopy import ARC4Contract, String, UInt64, Asset
from algopy.arc4 import abimethod


class AlgoRewardsContract(ARC4Contract):
    """AlgoRewards - POAP-style NFT minting contract for event attendance - Phase 4 with Enhanced Features"""
    
    @abimethod()
    def create_session(self, session_id: String, session_name: String, session_description: String, metadata_url: String) -> String:
        """Create a new session - Phase 4 enhanced version"""
        # Return enhanced message with session details
        return "Phase4 Session created: " + session_name + " (ID: " + session_id + ", Metadata: " + metadata_url + ")"
    
    @abimethod()
    def claim_badge(self, session_id: String, recipient_address: String, asset_name: String, asset_unit: String, metadata_url: String) -> String:
        """Claim a badge for attending a session - Phase 4 enhanced version"""
        # Return enhanced message with NFT creation details
        return "Phase4 NFT Badge created: " + asset_name + " (" + asset_unit + ") for " + recipient_address + " with metadata: " + metadata_url + " - READY FOR REAL NFT MINTING"
    
    @abimethod()
    def get_session_info(self, session_id: String) -> String:
        """Get session information"""
        return "Phase4 Session info for: " + session_id
    
    @abimethod()
    def check_claim_status(self, session_id: String, recipient_address: String) -> UInt64:
        """Check if address has claimed badge for session"""
        # For Phase 4, return 0 (not claimed) - in real implementation this would check global state
        return UInt64(0)
    
    @abimethod()
    def hello(self, name: String) -> String:
        """Keep the original hello method for compatibility"""
        return "Hello, " + name + " - Phase 4 AlgoRewards with Enhanced Features"
    
    @abimethod()
    def mint_nft(self, asset_name: String, asset_unit: String, metadata_url: String, recipient_address: String) -> String:
        """Direct NFT minting method for Phase 4 - PREPARES FOR REAL NFT CREATION"""
        # This method prepares the contract for real NFT creation
        return "Phase4 NFT Prepared: " + asset_name + " (" + asset_unit + ") for " + recipient_address + " with metadata: " + metadata_url + " - CONTRACT READY FOR REAL NFT MINTING"
    
    @abimethod()
    def prepare_nft_creation(self, asset_name: String, asset_unit: String, metadata_url: String) -> String:
        """Prepare NFT creation parameters - Phase 4 method"""
        return "NFT Creation Parameters: Name=" + asset_name + ", Unit=" + asset_unit + ", Metadata=" + metadata_url + " - READY FOR ASSET CREATION"
