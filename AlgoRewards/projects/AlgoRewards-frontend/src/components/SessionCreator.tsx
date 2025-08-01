import { useWallet } from '@txnlab/use-wallet-react'
import { useSnackbar } from 'notistack'
import { useState } from 'react'
import { AlgoRewardsContractFactory } from '../contracts/AlgoRewardsContract'
import { getAlgodConfigFromViteEnvironment, getIndexerConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'
import { AlgorandClient } from '@algorandfoundation/algokit-utils'

interface SessionCreatorInterface {
  openModal: boolean
  setModalState: (value: boolean) => void
}

const SessionCreator = ({ openModal, setModalState }: SessionCreatorInterface) => {
  const [loading, setLoading] = useState<boolean>(false)
  const [formData, setFormData] = useState({
    sessionId: '',
    sessionName: '',
    sessionDescription: '',
    metadataUrl: ''
  })
  const { enqueueSnackbar } = useSnackbar()
  const { transactionSigner, activeAddress } = useWallet()

  const algodConfig = getAlgodConfigFromViteEnvironment()
  const indexerConfig = getIndexerConfigFromViteEnvironment()
  const algorand = AlgorandClient.fromConfig({
    algodConfig,
    indexerConfig,
  })
  algorand.setDefaultSigner(transactionSigner)

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
  }

  const createSession = async (e: React.FormEvent) => {
    e.preventDefault()
    
    if (!activeAddress) {
      enqueueSnackbar('Please connect your wallet first', { variant: 'error' })
      return
    }

    if (!formData.sessionId || !formData.sessionName || !formData.sessionDescription) {
      enqueueSnackbar('Please fill in all required fields', { variant: 'error' })
      return
    }

    setLoading(true)

    try {
      const factory = new AlgoRewardsContractFactory({
        defaultSender: activeAddress,
        algorand,
      })
      
      const appClient = factory.getAppClientById({ appId: BigInt(743652051) })
      
      // Use provided metadata URL or default
      const metadataUrl = formData.metadataUrl || "ipfs://QmYwAPJzv5CZsnA625s3Xf2nemtYgPpHdWEz79ojWnPbdG/readme.md"
      
      const result = await appClient.send.createSession({
        args: {
          sessionId: formData.sessionId,
          sessionName: formData.sessionName,
          sessionDescription: formData.sessionDescription,
          metadataUrl: metadataUrl
        }
      })

      const sessionNumber = result.return
      enqueueSnackbar(
        `Session created successfully! Session Number: ${sessionNumber}`, 
        { variant: 'success' }
      )
      
      // Reset form
      setFormData({
        sessionId: '',
        sessionName: '',
        sessionDescription: '',
        metadataUrl: ''
      })
      setModalState(false)
    } catch (error: any) {
      if (error.message.includes('Only creator can create sessions')) {
        enqueueSnackbar('Only the contract creator can create sessions', { variant: 'error' })
      } else {
        enqueueSnackbar(`Error creating session: ${error.message}`, { variant: 'error' })
      }
    } finally {
      setLoading(false)
    }
  }

  return (
    <dialog id="session_creator_modal" className={`modal ${openModal ? 'modal-open' : ''} bg-slate-200`}>
      <form method="dialog" className="modal-box">
        <h3 className="font-bold text-lg">Create New Session</h3>
        <div className="bg-blue-50 p-4 rounded-lg mb-4">
          <p className="text-sm text-blue-800">
            <strong>Admin Only:</strong> Create a new session for badge claiming
          </p>
        </div>
        
        <form onSubmit={createSession} className="space-y-4">
          <div>
            <label className="label">
              <span className="label-text">Session ID *</span>
            </label>
            <input
              type="text"
              name="sessionId"
              value={formData.sessionId}
              onChange={handleInputChange}
              placeholder="e.g., masterclass-001"
              className="input input-bordered w-full"
              required
            />
          </div>
          
          <div>
            <label className="label">
              <span className="label-text">Session Name *</span>
            </label>
            <input
              type="text"
              name="sessionName"
              value={formData.sessionName}
              onChange={handleInputChange}
              placeholder="e.g., Algorand Masterclass"
              className="input input-bordered w-full"
              required
            />
          </div>
          
          <div>
            <label className="label">
              <span className="label-text">Session Description *</span>
            </label>
            <textarea
              name="sessionDescription"
              value={formData.sessionDescription}
              onChange={handleInputChange}
              placeholder="Describe the session content..."
              className="textarea textarea-bordered w-full"
              rows={3}
              required
            />
          </div>
          
          <div>
            <label className="label">
              <span className="label-text">Metadata URL (Optional)</span>
            </label>
            <input
              type="text"
              name="metadataUrl"
              value={formData.metadataUrl}
              onChange={handleInputChange}
              placeholder="ipfs://..."
              className="input input-bordered w-full"
            />
            <label className="label">
              <span className="label-text-alt">Leave empty to use default metadata</span>
            </label>
          </div>
          
          <div className="modal-action">
            <button 
              type="submit" 
              className={`btn btn-primary ${loading ? 'loading' : ''}`}
              disabled={loading}
            >
              {loading ? <span className="loading loading-spinner" /> : 'Create Session'}
            </button>
            <button 
              type="button" 
              className="btn" 
              onClick={() => setModalState(!openModal)}
            >
              Cancel
            </button>
          </div>
        </form>
      </form>
    </dialog>
  )
}

export default SessionCreator 