# 🔍 AlgoRewards Validation Guide

## ✅ How to Verify Your Transactions Worked

### 1. **Check TestNet Explorer**
Visit: https://testnet.algoexplorer.io/application/743652051

**What to look for:**
- ✅ App exists and is deployed
- ✅ Creator address matches your wallet
- ✅ Recent transactions to this app

### 2. **Check Your Wallet**
1. Open Pera Wallet
2. Switch to TestNet (not MainNet)
3. Check transaction history
4. Look for recent transactions

**What to look for:**
- ✅ Session creation transaction
- ✅ Badge claiming transaction
- ✅ App call transactions to 743652051

### 3. **Check Transaction Details**
For each transaction, verify:
- ✅ **Application ID:** 743652051
- ✅ **Method Called:** createSession or claimBadge
- ✅ **Status:** Confirmed
- ✅ **Fee:** Reasonable amount (usually 0.001 ALGO)

### 4. **Frontend Validation**
In your browser at http://localhost:5173/:
- ✅ Session creation shows success message
- ✅ Badge claiming shows success message
- ✅ No error messages in console

### 5. **Expected Success Messages**
- **Session Creation:** "Session created: [session_name] (ID: [session_id])"
- **Badge Claiming:** "Badge claimed for session: [session_id] by: [your_address]"

## 🔗 Useful Links
- **TestNet Explorer:** https://testnet.algoexplorer.io/
- **Your App:** https://testnet.algoexplorer.io/application/743652051
- **AlgoKit Docs:** https://github.com/algorandfoundation/algokit-cli

## 📊 Validation Checklist
- [ ] App deployed to TestNet
- [ ] Session creation transaction sent
- [ ] Badge claiming transaction sent
- [ ] Transactions appear in wallet
- [ ] Transactions appear on explorer
- [ ] Frontend shows success messages
- [ ] No errors in browser console

## 🐛 Troubleshooting
If something doesn't work:
1. Check you're on TestNet (not MainNet)
2. Verify wallet has TestNet ALGO
3. Check browser console for errors
4. Try refreshing the page
5. Reconnect wallet if needed
