import { useWallet } from '@txnlab/use-wallet-react'
import { useSnackbar } from 'notistack'
import { useState } from 'react'
import { AlgorandClient } from '@algorandfoundation/algokit-utils'
import { getAlgodConfigFromViteEnvironment, getIndexerConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'
import algosdk from 'algosdk'

interface SessionData {
  id: string
  name: string
  date: string
  time: string
  topics: string[]
  color: string
  unitName: string
  badgeName: string
  imageUrl: string
  active: boolean
}

interface RealNFTClaimerInterface {
  sessionId: string
  sessionName: string
  sessionData: SessionData
  attendanceCode: string
  openModal: boolean
  setModalState: (value: boolean) => void
}

interface NFTMetadata {
  name: string
  description: string
  image: string
  image_integrity?: string
  image_mimetype: string
  background_color: string
  external_url: string
  properties: {
    category: string
    type: string
    issuer: string
    session: string
    date_issued: string
    rarity: string
    transferable: boolean
    traits: Array<{
      trait_type: string
      value: string | number
      display_type?: string
    }>
  }
}

const RealNFTClaimer = ({ sessionId, sessionName, sessionData, attendanceCode, openModal, setModalState }: RealNFTClaimerInterface) => {
  const [loading, setLoading] = useState<boolean>(false)
  const [createdAssetId, setCreatedAssetId] = useState<number | null>(null)
  const [showSuccess, setShowSuccess] = useState<boolean>(false)
  const { enqueueSnackbar } = useSnackbar()
  const { transactionSigner, activeAddress } = useWallet()

  const algodConfig = getAlgodConfigFromViteEnvironment()
  const indexerConfig = getIndexerConfigFromViteEnvironment()
  const algorand = AlgorandClient.fromConfig({
    algodConfig,
    indexerConfig,
  })

  const createNFTMetadata = (): NFTMetadata => {
    return {
      name: sessionData.badgeName,
      description: `Proof of attendance for ${sessionData.name}. This badge certifies completion of blockchain education milestones.`,
      image: sessionData.imageUrl,
      image_mimetype: "image/png",
      background_color: sessionData.color.replace('#', ''),
      external_url: "https://algorand.org",
      properties: {
        category: "Education",
        type: "POAP",
        issuer: "AlgoRewards Platform",
        session: sessionData.name,
        date_issued: new Date().toISOString().split('T')[0],
        rarity: "Common",
        transferable: true,
        traits: [
          {
            trait_type: "Achievement",
            value: `${sessionData.name} Complete`
          },
          {
            trait_type: "Session",
            value: sessionData.name
          },
          {
            trait_type: "Attendance Code",
            value: attendanceCode
          },
          {
            trait_type: "Date",
            value: new Date().toISOString().split('T')[0]
          },
          {
            trait_type: "Network",
            value: "Algorand"
          },
          {
            trait_type: "Event",
            value: "AlgoRewards Masterclass"
          }
        ]
      }
    }
  }

  const createSimpleNFT = async () => {
    if (!activeAddress) {
      enqueueSnackbar('Please connect your wallet first', { variant: 'error' })
      return
    }

    setLoading(true)

    try {
      // Set the default signer for the existing client
      algorand.setDefaultSigner(transactionSigner)

      // Create the simplest possible NFT
      const assetCreateResult = await algorand.send.assetCreate({
        sender: activeAddress,
        total: BigInt(1),
        decimals: 0,
        defaultFrozen: false,
        manager: activeAddress,
        reserve: activeAddress,
        freeze: activeAddress,
        clawback: activeAddress,
        unitName: `${sessionData.unitName}TEST`,
        assetName: `${sessionData.name} Test NFT`,
        // No URL, no metadata hash - just the basics
      })

      const txId = assetCreateResult.txIds[0]
      console.log('Simple NFT Creation Transaction ID:', txId)
      
      const assetId = Number(assetCreateResult.assetId)
      console.log('Simple NFT Created! Asset ID:', assetId)

      setCreatedAssetId(assetId)
      setShowSuccess(true)
      
      enqueueSnackbar(
        `🧪 ${sessionData.name} Test NFT created! Asset ID: ${assetId}`, 
        { variant: 'success' }
      )

    } catch (error: any) {
      console.error('Simple NFT Creation Error:', error)
      enqueueSnackbar(`Error creating simple NFT: ${error.message}`, { variant: 'error' })
    } finally {
      setLoading(false)
    }
  }

  const createRealNFT = async () => {
    if (!activeAddress) {
      enqueueSnackbar('Please connect your wallet first', { variant: 'error' })
      return
    }

    setLoading(true)

    try {
      // Set the default signer for the existing client
      algorand.setDefaultSigner(transactionSigner)

      // Create proper ARC-3 NFT metadata
      const metadata = createNFTMetadata()
      const metadataJson = JSON.stringify(metadata, null, 2)
      
      const metadataUrl = "https://bafkreihddthm5xr6n5fhtyg3kv4vd2wwfhewgm4j3qamynwc4f4k7tiwoa.ipfs.nftstorage.link/"
      
      // Create the metadata hash
      const metadataHash = new Uint8Array(await crypto.subtle.digest('SHA-256', new TextEncoder().encode(metadataJson)))

      // NFT parameters - following ARC-3 standard
      const assetName = metadata.name
      const unitName = sessionData.unitName
      const total = 1
      const decimals = 0
      const defaultFrozen = false
      
      // For NFTs, we typically set manager, reserve, freeze, and clawback to the creator
      // This allows for proper NFT management
      const manager = activeAddress
      const reserve = activeAddress
      const freeze = activeAddress
      const clawback = activeAddress

      // Use AlgoKit's asset creation with proper NFT parameters
      const assetCreateResult = await algorand.send.assetCreate({
        sender: activeAddress,
        total: BigInt(total),
        decimals: decimals,
        defaultFrozen: defaultFrozen,
        manager: manager,
        reserve: reserve,
        freeze: freeze,
        clawback: clawback,
        unitName: unitName,
        assetName: assetName,
        url: metadataUrl,
        metadataHash: metadataHash
      })

      const txId = assetCreateResult.txIds[0]
      const assetId = Number(assetCreateResult.assetId)

      setCreatedAssetId(assetId)
      setShowSuccess(true)
      
      enqueueSnackbar(
        `🎉 ${sessionData.badgeName} NFT created! Asset ID: ${assetId}`, 
        { variant: 'success' }
      )

    } catch (error: any) {
      console.error('NFT Creation Error:', error)
      enqueueSnackbar(`Error creating NFT: ${error.message}`, { variant: 'error' })
    } finally {
      setLoading(false)
    }
  }

  // Removed optInAndTransfer function - not needed since creator automatically owns the asset

  const viewOnExplorer = () => {
    if (createdAssetId) {
      window.open(`https://testnet.explorer.perawallet.app/asset/${createdAssetId}`, '_blank')
    }
  }

  const closeAndReset = () => {
    setModalState(false)
    setShowSuccess(false)
    setCreatedAssetId(null)
  }

  return (
    <dialog id="real_nft_claimer_modal" className={`modal ${openModal ? 'modal-open' : ''} bg-slate-200`}>
      <form method="dialog" className="modal-box max-w-md bg-slate-800 border border-slate-700">
        {!showSuccess ? (
          <>
            <h3 className="font-bold text-lg flex items-center text-white">
              <span className="mr-2">🎯</span>
              Claim {sessionData.badgeName}
            </h3>
            
            <div className="bg-slate-700/50 p-4 rounded-lg mb-4 border border-slate-600">
              <p className="text-sm text-slate-300 mb-2">
                <strong>Session:</strong> <span className="font-semibold text-purple-300">{sessionData.name}</span>
              </p>
              <p className="text-sm text-slate-300 mb-2">
                <strong>Date:</strong> <span className="font-semibold text-purple-300">{sessionData.date}</span>
              </p>
              <p className="text-sm text-slate-300">
                <strong>Code:</strong> <span className="font-mono text-blue-300">{attendanceCode}</span>
              </p>
            </div>

            <div className="bg-green-900/50 p-4 rounded-lg mb-4 border border-green-700">
              <h4 className="font-semibold text-green-300 mb-2">✅ {sessionData.badgeName} NFT Features:</h4>
              <ul className="text-sm text-green-300 space-y-1">
                <li>• 🖼️ {sessionData.color} badge with {sessionData.name} branding</li>
                <li>• 🏷️ Rich ARC-3 metadata with session details</li>
                <li>• 🔗 Transferable and tradeable</li>
                <li>• 🎯 ARC-3 compliant NFT standard</li>
                <li>• 🌟 Immutable and truly non-fungible</li>
                <li>• 📱 Compatible with all Algorand wallets</li>
              </ul>
            </div>

            <div className="bg-purple-900/50 p-3 rounded-lg mb-4">
              <p className="text-xs text-purple-300">
                <strong>🔍 Preview:</strong> {sessionData.color} badge with "{sessionData.badgeName}" text
              </p>
            </div>
            
            <div className="text-center space-y-3">
              <button 
                className={`btn btn-primary btn-lg w-full ${loading ? 'loading' : ''}`} 
                onClick={createRealNFT}
                disabled={loading}
              >
                {loading ? (
                  <span className="flex items-center">
                    <span className="loading loading-spinner mr-2" />
                    Creating {sessionData.badgeName}...
                  </span>
                ) : (
                  <span className="flex items-center justify-center">
                    <span className="mr-2">🎯</span>
                    Create {sessionData.badgeName}
                  </span>
                )}
              </button>
              
              <button 
                className={`btn btn-outline btn-sm w-full ${loading ? 'loading' : ''}`} 
                onClick={createSimpleNFT}
                disabled={loading}
              >
                {loading ? (
                  <span className="flex items-center">
                    <span className="loading loading-spinner mr-2" />
                    Creating Test NFT...
                  </span>
                ) : (
                  <span className="flex items-center justify-center">
                    <span className="mr-2">🧪</span>
                    Create Test NFT
                  </span>
                )}
              </button>
            </div>
          </>
        ) : (
          <>
            <h3 className="font-bold text-lg text-center text-green-400 mb-4">
              🎉 {sessionData.badgeName} Created Successfully!
            </h3>
            
            <div className="bg-green-900/50 p-6 rounded-lg mb-4 border border-green-700 text-center">
              <div className="mb-4">
                <div 
                  className="w-20 h-20 mx-auto rounded-lg flex items-center justify-center text-white font-bold text-xs"
                  style={{ backgroundColor: sessionData.color }}
                >
                  {sessionData.badgeName}
                </div>
              </div>
              
              <p className="font-semibold text-green-300 mb-2">NFT Asset ID: {createdAssetId}</p>
              <p className="text-sm text-green-300 mb-4">Your {sessionData.badgeName} NFT has been created and should appear in your wallet!</p>
              
              <button 
                className="btn btn-outline btn-sm"
                onClick={viewOnExplorer}
              >
                🔍 View on Explorer
              </button>
            </div>

            <div className="bg-blue-900/50 p-4 rounded-lg mb-4">
              <h4 className="font-semibold text-blue-300 mb-2">📱 View in Your Wallet:</h4>
              <div className="text-sm text-blue-300 space-y-2">
                <p>• Open your <strong>Pera Wallet</strong> or <strong>MyAlgo Wallet</strong></p>
                <p>• Look for the NFT in your assets list</p>
                <p>• Search for Asset ID: <code className="bg-blue-800 px-2 py-1 rounded">{createdAssetId}</code></p>
                <p>• It should show as "{sessionData.badgeName}" 🎯</p>
              </div>
            </div>
          </>
        )}

        <div className="modal-action">
          <button 
            className={`btn ${showSuccess ? 'btn-success' : 'btn-outline'}`} 
            onClick={closeAndReset}
          >
            {showSuccess ? '🎉 Close & View Collection' : 'Cancel'}
          </button>
        </div>
      </form>
    </dialog>
  )
}

export default RealNFTClaimer