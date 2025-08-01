from algopy import ARC4Contract, String, UInt64
from algopy.arc4 import abimethod


class AlgoRewardsContract(ARC4Contract):
    """
    AlgoRewards - Session 3 MVP Contract
    POAP-style NFT badge system for Session 3 attendance verification
    
    This contract handles Session 3 validation and authorization.
    Actual NFT minting is handled off-chain for better performance and flexibility.
    """
    
    @abimethod()
    def verify_session3_attendance(
        self, 
        attendee_address: String,
        verification_code: String
    ) -> UInt64:
        """
        Verify attendance for Session 3
        
        Args:
            attendee_address: Address of the attendee
            verification_code: Verification code provided by organizer
            
        Returns:
            1 if verified, 0 if not verified
        """
        # For MVP, accept any valid address and verification code
        # In production, this would check actual session data and verification codes
        if len(attendee_address) > 0 and len(verification_code) > 0:
            return UInt64(1)
        return UInt64(0)
    
    @abimethod()
    def authorize_session3_badge_mint(
        self, 
        recipient_address: String,
        badge_metadata_url: String
    ) -> String:
        """
        Authorize Session 3 NFT badge minting (actual minting happens off-chain)
        
        Args:
            recipient_address: Address to receive the badge
            badge_metadata_url: IPFS URL for badge metadata
            
        Returns:
            Authorization confirmation
        """
        return f"Session 3 badge minting authorized for {recipient_address}"
    
    @abimethod()
    def get_session3_info(self) -> String:
        """Get Session 3 information"""
        return "Session 3: From concept to creation: designing your solution with blockchain - August 5, 12:00 PM ET / 06:00 PM CEST"
    
    @abimethod()
    def validate_session3_eligibility(
        self, 
        attendee_address: String
    ) -> UInt64:
        """
        Validate if address is eligible for Session 3 badge
        
        Args:
            attendee_address: Address to check eligibility
            
        Returns:
            1 if eligible, 0 if not eligible
        """
        # For MVP, all valid addresses are eligible
        # In production, this would check registration, attendance, etc.
        if len(attendee_address) > 0:
            return UInt64(1)
        return UInt64(0)
    
    @abimethod()
    def hello(self, name: String) -> String:
        """Simple hello method for testing connectivity"""
        return f"Hello, {name} from AlgoRewards Session 3!"