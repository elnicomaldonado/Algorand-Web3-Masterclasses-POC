# AlgoRewards - Production Setup

A clean, production-ready POAP-style NFT badge system for event attendance on Algorand.

## 🏗️ Architecture

### Smart Contract
- **Purpose**: Session management and attendance verification
- **Location**: `smart_contracts/algo_rewards_contract/production_contract.py`
- **Features**: 
  - Session creation
  - Attendance verification
  - Badge minting authorization

### NFT Minting
- **Purpose**: Create and manage badge NFTs off-chain
- **Location**: `scripts/production/nft_minter.py`
- **Features**:
  - ARC-3 & ARC-19 compliant NFTs
  - Automatic metadata generation
  - Production-ready error handling

### Frontend
- **Purpose**: User interface for claiming and viewing badges
- **Location**: `../AlgoRewards-frontend/`
- **Features**:
  - Wallet connection
  - NFT badge creation
  - Personal NFT gallery

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Set environment variables
export DEPLOYER_MNEMONIC="your 25-word mnemonic here"
export ALGOD_SERVER="https://testnet-api.algonode.cloud"
export INDEXER_SERVER="https://testnet-idx.algonode.cloud"
```

### 2. Deploy Smart Contract

```bash
cd scripts/production
python deploy_production.py
```

### 3. Start Frontend

```bash
cd ../../AlgoRewards-frontend
npm install
npm run dev
```

## 📁 File Structure

```
AlgoRewards-contracts/
├── smart_contracts/
│   └── algo_rewards_contract/
│       ├── production_contract.py    # Clean production contract
│       └── contract.py              # Legacy contract (for reference)
├── scripts/
│   └── production/
│       ├── deploy_production.py     # Contract deployment
│       ├── nft_minter.py           # NFT creation utility
│       └── session_manager.py      # Session management
├── archive/
│   └── debug_scripts/              # Archived debug/test files
└── PRODUCTION_README.md            # This file

AlgoRewards-frontend/
├── src/
│   ├── components/
│   │   ├── RealNFTClaimer.tsx     # NFT creation UI
│   │   ├── NFTGallery.tsx         # NFT display gallery
│   │   └── ConnectWallet.tsx      # Wallet connection
│   └── Home.tsx                   # Main application
└── package.json
```

## 🎯 Key Features

### ✅ Smart Contract
- Session creation and management
- Attendance verification
- Authorization for badge minting
- Gas-efficient operations

### ✅ NFT System
- True NFTs (total=1, decimals=0)
- ARC-3 metadata standard
- ARC-19 metadata hash integrity
- Wallet-compatible display

### ✅ Frontend
- Clean, modern UI
- Real-time NFT creation
- Personal gallery view
- Mobile responsive

## 🔧 Development

### Adding New Features

1. **Smart Contract**: Modify `production_contract.py`
2. **NFT Logic**: Update `nft_minter.py`
3. **Frontend**: Add components in `../AlgoRewards-frontend/src/components/`

### Testing

```bash
# Test NFT minting
python scripts/production/nft_minter.py

# Test contract deployment
python scripts/production/deploy_production.py
```

## 📊 Production Checklist

### Pre-Deployment
- [ ] Environment variables configured
- [ ] Deployer account funded
- [ ] Contract tested on TestNet
- [ ] Frontend connected to correct App ID

### Post-Deployment
- [ ] Contract deployed successfully
- [ ] Frontend updated with new App ID
- [ ] NFT creation tested
- [ ] Gallery display verified

## 🌐 Network Configuration

### TestNet (Current)
- Algod: `https://testnet-api.algonode.cloud`
- Indexer: `https://testnet-idx.algonode.cloud`
- Explorer: `https://testnet.explorer.perawallet.app`

### MainNet (Production)
- Algod: `https://mainnet-api.algonode.cloud`
- Indexer: `https://mainnet-idx.algonode.cloud`
- Explorer: `https://explorer.perawallet.app`

## 🎨 NFT Standards

### ARC-3 (Metadata)
- Rich metadata with traits
- Image URLs and descriptions
- Custom properties support

### ARC-19 (Integrity)
- SHA-256 metadata hash
- Tamper-proof metadata
- Standards compliance

## 📱 Wallet Compatibility

- ✅ Pera Wallet
- ✅ MyAlgo Wallet
- ✅ Algorand Wallet
- ✅ Any ARC-1 compatible wallet

## 🤝 Contributing

1. Keep the production code clean
2. Archive debug/test files in `archive/`
3. Follow TypeScript best practices in frontend
4. Maintain ARC standards compliance

## 📄 License

MIT License - See LICENSE file for details