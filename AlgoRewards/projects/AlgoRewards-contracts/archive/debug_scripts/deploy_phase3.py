#!/usr/bin/env python3
"""
Phase 3 Deployment Script for AlgoRewards
Deploys the enhanced contract with real NFT minting capabilities
"""

import os
import sys
from dotenv import load_dotenv
import algokit_utils
import logging

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def check_environment():
    """Check if required environment variables are set"""
    required_vars = [
        'ALGOD_SERVER',
        'DEPLOYER_MNEMONIC'
    ]
    
    missing_vars = []
    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        logger.error(f"Missing required environment variables: {missing_vars}")
        logger.info("Please set these variables in your .env file")
        return False
    
    logger.info("Environment variables check passed")
    return True

def deploy_contract():
    """Deploy the Phase 3 contract"""
    try:
        logger.info("Starting Phase 3 contract deployment...")
        
        # Import the deployment function
        from smart_contracts.algo_rewards_contract.deploy_config import deploy
        
        # Run deployment
        deploy()
        
        logger.info("✅ Phase 3 contract deployed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"❌ Contract deployment failed: {e}")
        return False

def test_contract_functionality():
    """Test basic contract functionality"""
    try:
        logger.info("Testing contract functionality...")
        
        from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import (
            AlgoRewardsContractFactory,
        )
        
        # Initialize client
        algorand = algokit_utils.AlgorandClient.from_environment()
        deployer = algorand.account.from_environment("DEPLOYER")
        
        factory = algorand.client.get_typed_app_factory(
            AlgoRewardsContractFactory, default_sender=deployer.address
        )
        
        # Get app client by ID (you'll need to update this with your actual app ID)
        app_id = int(os.getenv('APP_ID', '743652051'))
        app_client = factory.getAppClientById({"appId": app_id})
        
        # Test hello method
        response = app_client.send.hello(args={"name": "Phase3"})
        logger.info(f"✅ Hello test passed: {getattr(response, 'return', 'N/A')}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Contract test failed: {e}")
        return False

def create_sample_session():
    """Create a sample session for testing"""
    try:
        logger.info("Creating sample session...")
        
        from create_session import create_session_with_metadata
        
        result = create_session_with_metadata(
            session_id="phase3-demo",
            session_name="Phase 3 Demo Session",
            session_description="Demonstration of real NFT minting capabilities",
            badge_image_url="https://example.com/badge.png",
            attributes={
                "Phase": "3",
                "Type": "Demo",
                "Features": "Real NFT Minting"
            }
        )
        
        if result:
            logger.info("✅ Sample session created successfully!")
            return True
        else:
            logger.error("❌ Sample session creation failed")
            return False
            
    except Exception as e:
        logger.error(f"❌ Sample session creation failed: {e}")
        return False

def main():
    """Main deployment function"""
    logger.info("🚀 AlgoRewards Phase 3 Deployment")
    logger.info("=" * 50)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    # Deploy contract
    if not deploy_contract():
        sys.exit(1)
    
    # Test functionality
    if not test_contract_functionality():
        logger.warning("⚠️ Contract test failed, but deployment may still be successful")
    
    # Create sample session (optional)
    create_sample = input("Create sample session for testing? (y/n): ").lower().strip()
    if create_sample == 'y':
        if not create_sample_session():
            logger.warning("⚠️ Sample session creation failed")
    
    logger.info("=" * 50)
    logger.info("🎉 Phase 3 deployment completed!")
    logger.info("Next steps:")
    logger.info("1. Update your frontend with the new contract")
    logger.info("2. Test session creation and badge claiming")
    logger.info("3. Configure IPFS metadata uploads")
    logger.info("4. Deploy to production when ready")

if __name__ == "__main__":
    main() 