import { useWallet } from '@txnlab/use-wallet-react'
import { useState, useEffect } from 'react'
import { AlgorandClient } from '@algorandfoundation/algokit-utils'
import { getAlgodConfigFromViteEnvironment, getIndexerConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'

interface NFTAsset {
  assetId: number
  name: string
  unitName: string
  url: string
  total: number
  decimals: number
  creator: string
}

const NFTGallery = () => {
  const [nfts, setNfts] = useState<NFTAsset[]>([])
  const [loading, setLoading] = useState<boolean>(false)
  const { activeAddress } = useWallet()

  const algodConfig = getAlgodConfigFromViteEnvironment()
  const indexerConfig = getIndexerConfigFromViteEnvironment()
  const algorand = AlgorandClient.fromConfig({
    algodConfig,
    indexerConfig,
  })

  const loadUserNFTs = async () => {
    if (!activeAddress) return

    setLoading(true)
    try {
      // Get account info
      const accountInfo = await algorand.client.algod.accountInformation(activeAddress).do()

      const assets = accountInfo.assets || []
      // Try both property formats for created assets
      const createdAssets = accountInfo.createdAssets || []

      // Process user's NFTs

      const nftAssets: NFTAsset[] = []
      
      // Process owned assets
      for (const asset of assets) {
        if (asset.amount > 0) {
          try {
            const assetInfo = await algorand.client.algod.getAssetByID(asset.assetId).do()
            const params = assetInfo.params
            
            // Check if it's an NFT (handle BigInt)
            const total = Number(params.total)
            const decimals = Number(params.decimals)
            if (total === 1 && decimals === 0) {
              nftAssets.push({
                assetId: Number(asset.assetId), // Convert BigInt to number
                name: params.name || 'Unnamed NFT',
                unitName: params.unitName || 'NFT',
                url: params.url || '',
                total: total, // Use converted number
                decimals: decimals, // Use converted number
                creator: params.creator
              })
            }
          } catch (error) {
            // Skip assets that can't be fetched
          }
        }
      }
      
      // Process created assets (these are automatically owned by creator)
      for (const asset of createdAssets) {
        try {
          const params = asset.params
          
          // Check if it's an NFT (handle BigInt)
          const total = Number(params.total)
          const decimals = Number(params.decimals)
          if (total === 1 && decimals === 0) {
            nftAssets.push({
              assetId: Number(asset.index), // Convert BigInt to number
              name: params.name || 'Unnamed NFT',
              unitName: params.unitName || 'NFT',
              url: params.url || '',
              total: total, // Use converted number
              decimals: decimals, // Use converted number
              creator: params.creator
            })
          }
        } catch (error) {
          // Skip assets that can't be processed
        }
      }

      // Remove duplicates and sort by asset ID (newest first)
      const uniqueNfts = nftAssets.filter((nft, index, self) => 
        index === self.findIndex(n => n.assetId === nft.assetId)
      )
      uniqueNfts.sort((a, b) => b.assetId - a.assetId)
      setNfts(uniqueNfts)

    } catch (error) {
      console.error('Error loading NFTs:', error)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    if (activeAddress) {
      loadUserNFTs()
    } else {
      setNfts([])
    }
  }, [activeAddress])

  const viewOnExplorer = (assetId: number) => {
    window.open(`https://testnet.explorer.perawallet.app/asset/${assetId}`, '_blank')
  }

  // Debug function removed for production

  const isAlgoRewardsBadge = (nft: NFTAsset) => {
    return nft.name.toLowerCase().includes('algorewards') || 
           nft.unitName.toLowerCase().includes('badge') ||
           nft.unitName.toLowerCase().includes('arbadge') ||
           nft.unitName.toLowerCase().includes('s3badge') ||
           nft.unitName.toLowerCase().includes('s4badge') ||
           nft.unitName.toLowerCase().includes('s5badge')
  }

  if (!activeAddress) {
    return (
      <div className="card bg-base-100 shadow-xl">
        <div className="card-body text-center">
          <h2 className="card-title justify-center">
            <span className="mr-2">🖼️</span>
            Your NFT Collection
          </h2>
          <p className="text-gray-500">Connect your wallet to view your NFT badges</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white rounded-2xl shadow-lg border border-gray-100">
      <div className="p-6">
        <div className="flex items-center justify-between mb-6">
          <div className="flex items-center gap-3">
            <div className="inline-flex items-center justify-center w-10 h-10 bg-purple-100 rounded-full">
              <span className="text-xl">🖼️</span>
            </div>
            <div>
              <h2 className="text-xl font-bold text-gray-800">Your NFT Collection</h2>
              <p className="text-sm text-gray-600">AlgoRewards badges and other NFTs</p>
            </div>
          </div>
          {nfts.length > 0 && (
            <div className="bg-purple-100 text-purple-700 px-3 py-1 rounded-full text-sm font-semibold">
              {nfts.length} NFT{nfts.length !== 1 ? 's' : ''}
            </div>
          )}
        </div>
        
        {loading ? (
          <div className="flex justify-center py-8">
            <span className="loading loading-spinner loading-lg"></span>
          </div>
        ) : nfts.length === 0 ? (
          <div className="text-center py-12">
            <div className="inline-flex items-center justify-center w-16 h-16 bg-gray-100 rounded-full mb-4">
              <span className="text-2xl text-gray-400">🖼️</span>
            </div>
            <h3 className="text-lg font-semibold text-gray-800 mb-2">No NFTs Found</h3>
            <p className="text-gray-600 mb-6 max-w-sm mx-auto">
              Create your first AlgoRewards badge to get started building your collection!
            </p>
            <button 
              className="bg-blue-600 hover:bg-blue-700 text-white px-6 py-2 rounded-lg font-semibold transition-colors duration-200"
              onClick={loadUserNFTs}
              disabled={loading}
            >
              🔄 Refresh Gallery
            </button>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {nfts.map((nft) => (
              <div 
                key={nft.assetId} 
                className={`bg-gray-50 rounded-xl p-4 border transition-all duration-200 hover:shadow-lg hover:scale-105 ${
                  isAlgoRewardsBadge(nft) 
                    ? 'border-purple-300 bg-gradient-to-br from-purple-50 to-blue-50' 
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <div className="space-y-3">
                  <div className="flex items-start justify-between">
                    <h3 className="font-semibold text-gray-800 text-sm leading-tight">{nft.name}</h3>
                    {isAlgoRewardsBadge(nft) && (
                      <div className="bg-purple-100 text-purple-700 px-2 py-1 rounded-full text-xs font-semibold">
                        AlgoRewards
                      </div>
                    )}
                  </div>
                  
                  <div className="mb-3">
                    {nft.url && nft.url.includes('placeholder') ? (
                      <div className="w-full h-24 bg-purple-500 rounded-lg flex items-center justify-center text-white text-xs font-bold text-center">
                        {nft.name}
                      </div>
                    ) : nft.url ? (
                      <img 
                        src={nft.url} 
                        alt={nft.name}
                        className="w-full h-24 object-cover rounded-lg"
                        onError={(e) => {
                          e.currentTarget.style.display = 'none'
                          e.currentTarget.nextElementSibling!.classList.remove('hidden')
                        }}
                      />
                    ) : null}
                    <div className="w-full h-24 bg-gray-300 rounded-lg flex items-center justify-center text-gray-600 text-xs hidden">
                      No Image
                    </div>
                  </div>
                  
                  <div className="text-xs text-gray-500 space-y-1">
                    <p><strong>Unit:</strong> {nft.unitName}</p>
                    <p><strong>Asset ID:</strong> {nft.assetId}</p>
                    <p><strong>Supply:</strong> {nft.total} (NFT)</p>
                  </div>
                  
                  <div className="flex justify-between items-center pt-2">
                    <div className="text-xs text-gray-500">
                      ID: {nft.assetId}
                    </div>
                    <button 
                      className="bg-blue-100 text-blue-700 hover:bg-blue-200 px-3 py-1 rounded-lg text-xs font-semibold transition-colors duration-200"
                      onClick={() => viewOnExplorer(nft.assetId)}
                    >
                      🔍 Explorer
                    </button>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
        
        {nfts.length > 0 && (
          <div className="mt-6 text-center border-t border-gray-200 pt-6">
            <button 
              className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-semibold transition-colors duration-200"
              onClick={loadUserNFTs}
              disabled={loading}
            >
              🔄 Refresh Collection
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default NFTGallery