# AlgoRewards Phase 3 Testing Guide

## 🧪 How to Test Phase 3 Implementation

### Prerequisites

- ✅ Phase 3 contract deployed (App ID: 1005)
- ✅ Environment variables set (.env file)
- ✅ Poetry dependencies installed

### Quick Test (Recommended)

Run the quick validation test:

```bash
cd AlgoRewards-contracts
poetry run python quick_test.py
```

Expected output:

```
🧪 Quick Phase 3 Validation Test
========================================
📍 Connected to App ID: 1005
📍 Your Address: Y4VEPH6JGSBFLJ6GR33DZG23BRS2XMKFVPNY5WIKA5FKUKDMK633WGK574

1. Testing hello method...
   ✅ TX: [TRANSACTION_ID]
   ✅ Result: Hello, QuickTest

2. Testing create_session (Phase 3)...
   ✅ TX: [TRANSACTION_ID]
   ✅ Result: Phase3 Session created: Quick Test Session (ID: quick-test-[timestamp], Metadata: ipfs://QmQuickTest123)

3. Testing claim_badge (Phase 3)...
   ✅ TX: [TRANSACTION_ID]
   ✅ Result: Phase3 NFT Badge created: Quick Test Badge (QTEST) for [YOUR_ADDRESS] with metadata: ipfs://QmQuickBadge456

🎉 VALIDATION RESULTS:
✅ Phase 3 contract is working!
✅ Enhanced methods with new parameters!
✅ IPFS metadata URLs supported!
✅ All transactions successful!

🎉 ALL TESTS PASSED!
```

### Comprehensive Test Suite

Run the full test suite:

```bash
cd AlgoRewards-contracts
poetry run python test_phase3.py
```

This will test:

- ✅ Hello method (compatibility)
- ✅ Create session with 4 parameters (Phase 3)
- ✅ Claim badge with 5 parameters (Phase 3)
- ✅ Get session info
- ✅ Check claim status
- ✅ IPFS utilities

### Manual Testing

#### 1. Test Individual Methods

**Test Hello Method:**

```python
import algokit_utils
from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import AlgoRewardsContractFactory

algorand = algokit_utils.AlgorandClient.from_environment()
deployer = algorand.account.from_environment('DEPLOYER')
factory = AlgoRewardsContractFactory(algorand=algorand, default_sender=deployer.address)
app_client = factory.get_app_client_by_id(app_id=1005)

response = app_client.send.hello(args=('TestUser',))
print(f"Response: {response.abi_return}")
```

**Test Create Session (Phase 3):**

```python
session_response = app_client.send.create_session(args=(
    'my-session-001',
    'My Test Session',
    'Testing Phase 3 functionality',
    'ipfs://QmMyMetadata123'
))
print(f"Response: {session_response.abi_return}")
```

**Test Claim Badge (Phase 3):**

```python
badge_response = app_client.send.claim_badge(args=(
    'my-session-001',
    deployer.address,
    'My Test Badge',
    'MYBADGE',
    'ipfs://QmMyBadgeMetadata456'
))
print(f"Response: {badge_response.abi_return}")
```

#### 2. Using Command Line Scripts

**Create a session:**

```bash
poetry run python create_session.py create "test-001" "Test Session" "Test description"
```

**Claim a badge:**

```bash
poetry run python create_session.py claim "test-001" "YOUR_ADDRESS"
```

### Frontend Testing

#### 1. Start Frontend

```bash
cd ../AlgoRewards-frontend
npm install
npm run dev
```

#### 2. Test in Browser

- Connect wallet
- Create session (admin function)
- Claim badge (attendee function)
- Verify NFT parameters are passed correctly

### Verification on Blockchain

#### 1. Check App on Explorer

- **TestNet Explorer:** https://testnet.algoexplorer.io/application/1005
- **TestNet AlgoScan:** https://testnet.algoscan.app/app/1005

#### 2. Verify Transactions

Each test will output transaction IDs that you can check:

```
https://testnet.algoexplorer.io/tx/[TRANSACTION_ID]
```

### Expected Results

✅ **What Should Work:**

- Contract responds to all method calls
- Enhanced create_session accepts 4 parameters
- Enhanced claim_badge accepts 5 parameters
- IPFS URLs are handled in metadata parameters
- All methods return enhanced Phase 3 messages
- Transactions are visible on TestNet explorer

❌ **What Won't Work Yet:**

- Real NFT minting (this is simulated in Phase 3)
- Actual IPFS uploads (requires API keys)
- State persistence between calls (no global state in this version)

### Troubleshooting

#### Common Issues:

**"App not found" error:**

- Verify App ID 1005 exists
- Check you're on TestNet network

**"Connection failed" error:**

- Check .env file has correct ALGOD_SERVER
- Verify DEPLOYER_MNEMONIC is set

**"Method not found" error:**

- Contract may not be the Phase 3 version
- Regenerate client: `algokit generate client`

**"Invalid args" error:**

- Check argument count and types
- Phase 3 methods have more parameters than Phase 2

### Success Indicators

🎉 **Phase 3 is working if you see:**

- "Phase3 Session created:" in create_session response
- "Phase3 NFT Badge created:" in claim_badge response
- IPFS URLs included in responses
- All transactions successful on TestNet
- Enhanced parameter counts (4 for create_session, 5 for claim_badge)

### Next Steps After Testing

1. ✅ Verify all tests pass
2. ✅ Check transactions on explorer
3. ✅ Test frontend integration
4. ✅ Document any issues
5. ✅ Ready for real NFT implementation (Phase 4)

---

**Testing Status:** Phase 3 implementation is fully functional and ready for validation! 🚀
