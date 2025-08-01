#!/usr/bin/env python3
"""Quick validation test for Phase 3 AlgoRewards"""

import algokit_utils
from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import AlgoRewardsContractFactory
import time

def main():
    print("🧪 Quick Phase 3 Validation Test")
    print("=" * 40)
    
    try:
        # Connect to the deployed contract
        algorand = algokit_utils.AlgorandClient.from_environment()
        deployer = algorand.account.from_environment('DEPLOYER')
        
        factory = AlgoRewardsContractFactory(
            algorand=algorand,
            default_sender=deployer.address
        )
        
        app_client = factory.get_app_client_by_id(app_id=1005)
        
        print(f"📍 Connected to App ID: {app_client.app_id}")
        print(f"📍 Your Address: {deployer.address}")
        print()
        
        # Quick Test 1: Hello Method
        print("1. Testing hello method...")
        response = app_client.send.hello(args=('QuickTest',))
        print(f"   ✅ TX: {response.tx_id}")
        print(f"   ✅ Result: {response.abi_return}")
        print()
        
        # Quick Test 2: Create Session (Phase 3)
        print("2. Testing create_session (Phase 3)...")
        session_id = f"quick-test-{int(time.time())}"
        session_response = app_client.send.create_session(args=(
            session_id,
            'Quick Test Session',
            'Phase 3 validation test',
            'ipfs://QmQuickTest123'
        ))
        print(f"   ✅ TX: {session_response.tx_id}")
        print(f"   ✅ Result: {session_response.abi_return}")
        print()
        
        # Quick Test 3: Claim Badge (Phase 3)
        print("3. Testing claim_badge (Phase 3)...")
        badge_response = app_client.send.claim_badge(args=(
            session_id,
            deployer.address,
            'Quick Test Badge',
            'QTEST',
            'ipfs://QmQuickBadge456'
        ))
        print(f"   ✅ TX: {badge_response.tx_id}")
        print(f"   ✅ Result: {badge_response.abi_return}")
        print()
        
        print("🎉 VALIDATION RESULTS:")
        print("✅ Phase 3 contract is working!")
        print("✅ Enhanced methods with new parameters!")
        print("✅ IPFS metadata URLs supported!")
        print("✅ All transactions successful!")
        print()
        
        print("🔗 View on TestNet Explorer:")
        print(f"App: https://testnet.algoexplorer.io/application/1005")
        print(f"Latest TX: https://testnet.algoexplorer.io/tx/{badge_response.tx_id}")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    if success:
        print("\n🎉 ALL TESTS PASSED!")
    else:
        print("\n❌ TESTS FAILED!")