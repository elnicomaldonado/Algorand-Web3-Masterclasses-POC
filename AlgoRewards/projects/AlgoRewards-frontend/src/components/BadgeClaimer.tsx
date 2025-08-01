import { useWallet } from '@txnlab/use-wallet-react'
import { useSnackbar } from 'notistack'
import { useState } from 'react'
import { AlgoRewardsContractFactory } from '../contracts/AlgoRewardsContract'
import { getAlgodConfigFromViteEnvironment, getIndexerConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'
import { AlgorandClient } from '@algorandfoundation/algokit-utils'

interface BadgeClaimerInterface {
  sessionId: string
  sessionName: string
  openModal: boolean
  setModalState: (value: boolean) => void
}

const BadgeClaimer = ({ sessionId, sessionName, openModal, setModalState }: BadgeClaimerInterface) => {
  const [loading, setLoading] = useState<boolean>(false)
  const { enqueueSnackbar } = useSnackbar()
  const { transactionSigner, activeAddress } = useWallet()

  const algodConfig = getAlgodConfigFromViteEnvironment()
  const indexerConfig = getIndexerConfigFromViteEnvironment()
  const algorand = AlgorandClient.fromConfig({
    algodConfig,
    indexerConfig,
  })
  algorand.setDefaultSigner(transactionSigner)

  const claimBadge = async () => {
    if (!activeAddress) {
      enqueueSnackbar('Please connect your wallet first', { variant: 'error' })
      return
    }

    setLoading(true)

    try {
      const factory = new AlgoRewardsContractFactory({
        defaultSender: activeAddress,
        algorand,
      })
      
      const appClient = factory.getAppClientById({ appId: BigInt(743652051) })
      
      // Generate asset name and unit
      const assetName = `AlgoRewards Badge - ${sessionName}`
      const assetUnit = `BADGE-${sessionId}`
      
      // For now, use a default metadata URL - in production this would come from the session
      const metadataUrl = "ipfs://QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme.md"
      
      const result = await appClient.send.claimBadge({
        args: {
          sessionId: sessionId,
          recipientAddress: activeAddress,
          assetName: assetName,
          assetUnit: assetUnit,
          metadataUrl: metadataUrl
        }
      })

      const assetId = result.return
      enqueueSnackbar(
        `Badge claimed successfully! NFT Asset ID: ${assetId}`, 
        { variant: 'success' }
      )
      setModalState(false)
    } catch (error: any) {
      if (error.message.includes('already claimed')) {
        enqueueSnackbar('You have already claimed this badge!', { variant: 'warning' })
      } else if (error.message.includes('Session does not exist')) {
        enqueueSnackbar('Session does not exist. Please contact the administrator.', { variant: 'error' })
      } else {
        enqueueSnackbar(`Error claiming badge: ${error.message}`, { variant: 'error' })
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <dialog id="badge_claimer_modal" className={`modal ${openModal ? 'modal-open' : ''} bg-slate-200`}>
      <form method="dialog" className="modal-box">
        <h3 className="font-bold text-lg">Claim Your Badge</h3>
        <div className="bg-blue-50 p-4 rounded-lg mb-4">
          <p className="text-sm text-gray-600 mb-2">Session: <span className="font-semibold">{sessionName}</span></p>
          <p className="text-sm text-gray-600">Session ID: <span className="font-mono">{sessionId}</span></p>
        </div>
        <div className="bg-yellow-50 p-4 rounded-lg mb-4">
          <p className="text-sm text-yellow-800">
            <strong>New Feature:</strong> This will mint a real non-transferable NFT badge to your wallet!
          </p>
        </div>
        <br />
        <div className="text-center">
          <p className="mb-4">Click the button below to claim your attendance badge NFT!</p>
          <button 
            className={`btn btn-primary btn-lg ${loading ? 'loading' : ''}`} 
            onClick={claimBadge}
            disabled={loading}
          >
            {loading ? <span className="loading loading-spinner" /> : 'Claim Badge NFT'}
          </button>
        </div>
        <div className="modal-action">
          <button className="btn" onClick={() => setModalState(!openModal)}>
            Close
          </button>
        </div>
      </form>
    </dialog>
  )
}

export default BadgeClaimer
