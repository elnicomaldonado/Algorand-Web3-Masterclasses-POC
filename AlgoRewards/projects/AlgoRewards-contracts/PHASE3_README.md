# AlgoRewards Phase 3: Real NFT Minting Implementation

## Overview

Phase 3 enhances AlgoRewards with real NFT minting capabilities, replacing the string-based MVP approach with actual non-transferable NFT badges that include ARC-19 metadata and IPFS integration.

## Key Features

### 🎯 Real NFT Minting

- **Non-transferable NFTs**: Badges are minted as actual Algorand assets with `default_frozen=true`
- **ARC-19 Metadata**: Compliant metadata format for Algorand NFTs
- **IPFS Integration**: Decentralized metadata storage using IPFS
- **Session Management**: Admin-controlled session creation with metadata

### 🔧 Technical Implementation

#### Smart Contract Enhancements

- **State Management**: Global state for session tracking and claim verification
- **Asset Creation**: In-app asset creation with proper parameters
- **Access Control**: Creator-only session creation
- **Duplicate Prevention**: One badge per address per session

#### Frontend Updates

- **Session Creator**: Admin interface for creating new sessions
- **Enhanced Badge Claimer**: Real NFT minting with asset ID returns
- **Improved UI**: Better user experience with clear feature descriptions

## Contract Methods

### Session Management

```python
def create_session(session_id: String, session_name: String,
                  session_description: String, metadata_url: String) -> UInt64
```

- Creates a new session with IPFS metadata
- Only contract creator can create sessions
- Returns session number

### Badge Claiming

```python
def claim_badge(session_id: String, recipient_address: String,
                asset_name: String, asset_unit: String, metadata_url: String) -> Asset
```

- Claims a badge for session attendance
- Creates actual NFT with ARC-19 metadata
- Returns the created asset ID
- Prevents duplicate claims

### Utility Methods

```python
def get_session_info(session_id: String) -> String
def check_claim_status(session_id: String, recipient_address: String) -> UInt64
```

## IPFS Integration

### Metadata Structure

```json
{
  "name": "AlgoRewards Badge - {session_name}",
  "description": "Attendance badge for {session_name}",
  "image": "ipfs://{image_hash}",
  "external_url": "https://algorewards.com",
  "attributes": [
    { "trait_type": "Session ID", "value": "session_id" },
    { "trait_type": "Session Name", "value": "session_name" },
    { "trait_type": "Badge Type", "value": "Attendance" },
    { "trait_type": "Minted Date", "value": "timestamp" },
    { "trait_type": "Non-Transferable", "value": true }
  ]
}
```

### IPFS Upload

- Uses Pinata API for IPFS uploads
- Requires `PINATA_API_KEY` and `PINATA_SECRET_KEY` environment variables
- Returns `ipfs://{hash}` URLs for metadata

## Usage Instructions

### 1. Environment Setup

#### Backend Dependencies

```bash
cd AlgoRewards-contracts
poetry install
```

#### Environment Variables

```bash
# Required for IPFS uploads
PINATA_API_KEY=your_pinata_api_key
PINATA_SECRET_KEY=your_pinata_secret_key

# Algorand configuration
ALGOD_SERVER=https://testnet-api.algonode.cloud
ALGOD_TOKEN=
ALGOD_PORT=443
DEPLOYER_MNEMONIC=your_deployer_mnemonic
```

### 2. Contract Deployment

```bash
cd AlgoRewards-contracts
poetry run python -m smart_contracts.algo_rewards_contract.deploy_config
```

### 3. Session Creation

#### Using Python Script

```bash
python create_session.py create "masterclass-001" "Algorand Masterclass" "Learn about Algorand smart contracts"
```

#### Using Frontend

1. Connect wallet as admin
2. Click "Create New Session (Admin)"
3. Fill in session details
4. Submit to create session

### 4. Badge Claiming

#### Using Python Script

```bash
python create_session.py claim "masterclass-001" "RECIPIENT_ADDRESS"
```

#### Using Frontend

1. Connect wallet as attendee
2. Click "Claim Badge NFT (Attendee)"
3. Confirm transaction
4. Receive NFT in wallet

## Frontend Features

### Session Creator (Admin)

- **Session ID**: Unique identifier for the session
- **Session Name**: Display name for the session
- **Description**: Detailed session description
- **Metadata URL**: Optional IPFS metadata URL

### Badge Claimer (Attendee)

- **Real NFT Minting**: Creates actual Algorand assets
- **Asset ID Return**: Shows the created NFT asset ID
- **Duplicate Prevention**: Prevents multiple claims
- **Error Handling**: Clear error messages for various scenarios

## Technical Details

### Asset Parameters

```python
asset_params = {
    "asset_name": asset_name.bytes,
    "unit_name": asset_unit.bytes,
    "total": UInt64(1),  # Only 1 NFT per claim
    "decimals": UInt64(0),  # NFTs are indivisible
    "default_frozen": True,  # Non-transferable
    "manager": Global.current_application_address(),
    "reserve": Global.current_application_address(),
    "freeze": Global.current_application_address(),
    "clawback": Global.current_application_address(),
    "url": arc19_url,  # ARC-19 metadata URL
    "metadata_hash": metadata_hash,
    "note": b"AlgoRewards Badge NFT"
}
```

### State Management

- **Session Storage**: `session_` prefix for session data
- **Claim Tracking**: `claim_` prefix for claim verification
- **Counter**: Global session counter

## Testing

### Test Session Creation

```bash
# Create test session
python create_session.py create "test-001" "Test Session" "Test description"

# Claim test badge
python create_session.py claim "test-001" "YOUR_ADDRESS"
```

### Frontend Testing

1. Deploy contract
2. Open frontend
3. Connect wallet
4. Test session creation (admin)
5. Test badge claiming (attendee)

## Security Considerations

### Access Control

- Only contract creator can create sessions
- Session existence verification before claims
- Duplicate claim prevention

### Asset Security

- Non-transferable NFTs (`default_frozen=true`)
- App-controlled asset management
- Proper metadata validation

### IPFS Security

- Metadata hash verification
- ARC-19 compliance
- Decentralized storage

## Next Steps

### Phase 4 Enhancements

- **Batch Operations**: Multiple badge claims
- **Advanced Metadata**: Dynamic attributes
- **Analytics**: Claim tracking and statistics
- **Multi-chain**: Support for other networks

### Production Considerations

- **Gas Optimization**: Minimize transaction costs
- **Error Recovery**: Robust error handling
- **Monitoring**: Transaction monitoring and alerts
- **Backup**: Metadata backup strategies

## Troubleshooting

### Common Issues

#### IPFS Upload Failures

- Verify Pinata API credentials
- Check network connectivity
- Validate metadata format

#### Contract Deployment Issues

- Ensure sufficient ALGO balance
- Verify network configuration
- Check contract compilation

#### Badge Claim Failures

- Verify session exists
- Check for duplicate claims
- Ensure proper wallet connection

### Debug Commands

```bash
# Check session info
python -c "
from smart_contracts.artifacts.algo_rewards_contract.algo_rewards_contract_client import AlgoRewardsContractFactory
import algokit_utils
algorand = algokit_utils.AlgorandClient.from_environment()
factory = algorand.client.get_typed_app_factory(AlgoRewardsContractFactory)
app_client = factory.getAppClientById({'appId': 743652051})
result = app_client.send.get_session_info(args={'session_id': 'test-001'})
print(result.return)
"
```

## Support

For issues and questions:

1. Check the troubleshooting section
2. Review contract logs
3. Verify environment configuration
4. Test with minimal examples

---

**Phase 3 Status**: ✅ Complete with real NFT minting, IPFS integration, and enhanced UI
