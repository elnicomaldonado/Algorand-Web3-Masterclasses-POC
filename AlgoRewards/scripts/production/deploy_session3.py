#!/usr/bin/env python3
"""
Session 3 MVP Deployment Script
Deploys the AlgoRewards contract specifically for Session 3
"""

import os
import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from smart_contracts.algo_rewards_contract.production_contract import AlgoRewardsContract
from algokit_utils import (
    ApplicationClient,
    ApplicationSpecification,
    get_localnet_default_account,
    get_algod_client,
    get_indexer_client,
)
from algosdk.atomic_transaction_composer import AccountTransactionSigner
from algosdk.mnemonic import to_private_key


def deploy_session3_contract():
    """Deploy the Session 3 MVP contract"""
    
    print("🚀 Deploying Session 3 MVP Contract...")
    
    # Get the contract specification
    app_spec = ApplicationSpecification.from_json(AlgoRewardsContract.contract())
    
    # Get the client
    algod_client = get_algod_client()
    indexer_client = get_indexer_client()
    
    # Get the default account
    account = get_localnet_default_account(algod_client)
    
    # Create the application client
    app_client = ApplicationClient(
        algod_client=algod_client,
        app_spec=app_spec,
        signer=AccountTransactionSigner(account.private_key),
        template_values={"VERSION": "1.0.0"},
    )
    
    # Deploy the application
    app_id, app_address, txid = app_client.create()
    
    print(f"✅ Session 3 Contract Deployed Successfully!")
    print(f"📋 App ID: {app_id}")
    print(f"📍 App Address: {app_address}")
    print(f"🔗 Transaction ID: {txid}")
    
    # Test the contract
    print("\n🧪 Testing Session 3 Contract...")
    
    # Test hello method
    result = app_client.call(AlgoRewardsContract.hello, name="Session 3")
    print(f"✅ Hello test: {result.return_value}")
    
    # Test session info
    result = app_client.call(AlgoRewardsContract.get_session3_info)
    print(f"✅ Session info: {result.return_value}")
    
    # Test eligibility validation
    result = app_client.call(
        AlgoRewardsContract.validate_session3_eligibility,
        attendee_address=account.address
    )
    print(f"✅ Eligibility test: {result.return_value}")
    
    # Test attendance verification
    result = app_client.call(
        AlgoRewardsContract.verify_session3_attendance,
        attendee_address=account.address,
        verification_code="SESSION3"
    )
    print(f"✅ Attendance verification: {result.return_value}")
    
    # Test badge authorization
    result = app_client.call(
        AlgoRewardsContract.authorize_session3_badge_mint,
        recipient_address=account.address,
        badge_metadata_url="https://example.com/session3-badge.json"
    )
    print(f"✅ Badge authorization: {result.return_value}")
    
    print(f"\n🎉 Session 3 MVP Contract is ready!")
    print(f"📱 Frontend can now connect to App ID: {app_id}")
    print(f"🔗 TestNet Explorer: https://testnet.explorer.perawallet.app/application/{app_id}")
    
    return app_id, app_address


if __name__ == "__main__":
    try:
        app_id, app_address = deploy_session3_contract()
        
        # Save deployment info
        deployment_info = {
            "app_id": app_id,
            "app_address": app_address,
            "session": "Session 3",
            "deployment_date": "2025-01-27",
            "purpose": "MVP Session 3 Badge Minting"
        }
        
        # Write to a file for reference
        with open("session3_deployment.json", "w") as f:
            import json
            json.dump(deployment_info, f, indent=2)
        
        print(f"\n📄 Deployment info saved to session3_deployment.json")
        
    except Exception as e:
        print(f"❌ Deployment failed: {e}")
        sys.exit(1) 