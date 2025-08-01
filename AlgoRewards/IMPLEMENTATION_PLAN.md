# 🚀 AlgoRewards MVP Implementation Plan

## 🎯 Project Overview

**AlgoRewards** is a POAP-style MVP on Algorand that allows event participants to claim unique NFT badges as proof of attendance.

**Current Status:** ✅ Basic project setup complete
- TestNet deployment ready
- Frontend running on TestNet
- Smart contract deployed (App ID: 743651454)

---

## 🎯 Phase 1: Smart Contract Development

### Step 1.1: Update Smart Contract for NFT Minting
**File:** `projects/AlgoRewards-contracts/smart_contracts/algo_rewards_contract/contract.py`

**Current:** Basic "hello" contract
**Target:** NFT minting contract with session management

**Implementation:**
```python
from algopy import ARC4Contract, String, UInt64, Address, Asset
from algopy.arc4 import abimethod, abicall
from algopy import itxn


class AlgoRewardsContract(ARC4Contract):
    """AlgoRewards - POAP-style NFT minting contract for event attendance"""
    
    # Global state to track claimed addresses per session
    claimed_addresses: dict[String, UInt64]
    
    @abimethod()
    def create_session(self, session_id: String, session_name: String, session_description: String) -> Asset:
        """Create a new session and mint the first NFT"""
        # Only creator can create sessions
        assert self.creator == self.sender, "Only creator can create sessions"
        
        # Create the NFT asset
        asset_id = itxn.AssetConfig(
            config_asset_name=session_name,
            config_asset_unit_name="BADGE",
            config_asset_total=1,
            config_asset_decimals=0,
            config_asset_default_frozen=True,
            config_asset_manager=self.app_address,
            config_asset_reserve=self.app_address,
            config_asset_freeze=self.app_address,
            config_asset_clawback=self.app_address,
            fee=0,
            rekey_to=self.app_address
        ).submit()
        
        # Initialize session tracking
        self.claimed_addresses[session_id] = UInt64(0)
        
        return asset_id
    
    @abimethod()
    def claim_badge(self, session_id: String, recipient: Address) -> Asset:
        """Claim a badge for attending a session"""
        # Check if user already claimed
        claimed_key = session_id + "_" + recipient
        assert self.claimed_addresses[claimed_key] == UInt64(0), "Already claimed"
        
        # Mark as claimed
        self.claimed_addresses[claimed_key] = UInt64(1)
        
        # Transfer NFT to recipient
        return Asset(0)  # Placeholder - will be session asset ID
```

### Step 1.2: Build and Deploy Updated Contract
**Commands:**
```bash
# Build the updated contract
algokit project run build

# Deploy to TestNet
algokit project deploy testnet
```

**Expected Output:** New app ID for the updated contract

---

## 🎯 Phase 2: Frontend Component Development

### Step 2.1: Create Session Management Component
**File:** `projects/AlgoRewards-frontend/src/components/SessionManager.tsx`

**Purpose:** Allow organizers to create new sessions

**Features:**
- Session ID input
- Session name input
- Session description input
- Create session button
- Success/error notifications

### Step 2.2: Create Badge Claiming Component
**File:** `projects/AlgoRewards-frontend/src/components/BadgeClaimer.tsx`

**Purpose:** Allow attendees to claim badges

**Features:**
- Session information display
- Claim button
- Already claimed detection
- Success/error notifications

### Step 2.3: Create QR Code Generator
**File:** `projects/AlgoRewards-frontend/src/components/QRCodeGenerator.tsx`

**Purpose:** Generate QR codes for session links

**Dependencies:**
```bash
cd projects/AlgoRewards-frontend
npm install qrcode @types/qrcode
```

### Step 2.4: Update Main App Component
**File:** `projects/AlgoRewards-frontend/src/App.tsx`

**Changes:**
- Add routing for claim pages
- Integrate new components
- Handle session data

---

## 🎯 Phase 3: Metadata and IPFS Integration

### Step 3.1: Create Metadata Structure
**File:** `projects/AlgoRewards-frontend/src/utils/metadata.ts`

**Purpose:** Define NFT metadata structure

**Structure:**
```typescript
interface NFTMetadata {
  name: string
  description: string
  image: string
  attributes: {
    session_id: string
    session_date: string
    event_type: string
  }
}
```

### Step 3.2: IPFS Integration
**Dependencies:**
```bash
npm install ipfs-http-client
```

**Purpose:** Store metadata on IPFS

---

## 🎯 Phase 4: Testing and Refinement

### Step 4.1: Test Complete Flow
1. Create session as organizer
2. Generate QR code
3. Claim badge as attendee
4. Verify NFT in wallet

### Step 4.2: Error Handling
- Network errors
- Wallet connection issues
- Duplicate claims
- Invalid session IDs

### Step 4.3: UI/UX Improvements
- Loading states
- Better error messages
- Responsive design
- Accessibility

---

## �� Implementation Timeline

| Week | Phase | Tasks |
|------|-------|-------|
| 1 | Smart Contract | Update contract, build, deploy |
| 2 | Frontend Components | SessionManager, BadgeClaimer, QRCodeGenerator |
| 3 | Integration | Connect components, test flow |
| 4 | Metadata & IPFS | Metadata structure, IPFS integration |
| 5 | Testing & Polish | Error handling, UI improvements |

---

## ✅ Success Criteria

- [ ] Smart contract can create sessions
- [ ] Smart contract can mint NFTs
- [ ] Smart contract prevents duplicate claims
- [ ] Frontend can create sessions
- [ ] Frontend can claim badges
- [ ] QR codes work for session links
- [ ] Metadata is properly structured
- [ ] Complete flow works end-to-end

---

## 🛠 Development Commands

### Smart Contract
```bash
# Build contract
algokit project run build

# Deploy to TestNet
algokit project deploy testnet

# Deploy to LocalNet
algokit project deploy localnet
```

### Frontend
```bash
# Install dependencies
cd projects/AlgoRewards-frontend
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Project-wide
```bash
# Bootstrap all dependencies
algokit project bootstrap all

# Build all projects
algokit project run build
```

---

## 🐛 Troubleshooting

### Common Issues
1. **Contract deployment fails** - Check wallet balance and network connection
2. **Frontend can't connect** - Verify environment variables and network settings
3. **QR codes not working** - Check URL structure and routing
4. **Metadata not loading** - Verify IPFS connection and metadata structure

### Debug Commands
```bash
# Check contract status
algokit project run build

# Check frontend logs
cd projects/AlgoRewards-frontend && npm run dev

# Check network status
algokit localnet status
```

---

## 📚 Resources

- [AlgoKit Documentation](https://github.com/algorandfoundation/algokit-cli)
- [Algorand Python Documentation](https://github.com/algorandfoundation/puya)
- [React + Vite Documentation](https://vitejs.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)
- [POAP.xyz Reference](https://poap.xyz)

---

## 🎯 Next Steps

1. **Start with Phase 1** - Update the smart contract
2. **Test thoroughly** - Ensure contract works before moving to frontend
3. **Build incrementally** - Test each component as you build it
4. **Document everything** - Keep track of app IDs, addresses, and configurations

**Ready to begin? Start with Step 1.1!**
