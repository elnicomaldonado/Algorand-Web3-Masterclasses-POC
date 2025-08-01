import { useWallet } from '@txnlab/use-wallet-react'
import { useSnackbar } from 'notistack'
import { useState } from 'react'
import { AlgoRewardsContractFactory } from '../contracts/AlgoRewardsContract'
import { getAlgodConfigFromViteEnvironment, getIndexerConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'
import { AlgorandClient } from '@algorandfoundation/algokit-utils'

interface SessionManagerInterface {
  openModal: boolean
  setModalState: (value: boolean) => void
}

const SessionManager = ({ openModal, setModalState }: SessionManagerInterface) => {
  const [loading, setLoading] = useState<boolean>(false)
  const [sessionId, setSessionId] = useState<string>('')
  const [sessionName, setSessionName] = useState<string>('')
  const [sessionDescription, setSessionDescription] = useState<string>('')
  const { enqueueSnackbar } = useSnackbar()
  const { transactionSigner, activeAddress } = useWallet()

  const algodConfig = getAlgodConfigFromViteEnvironment()
  const indexerConfig = getIndexerConfigFromViteEnvironment()
  const algorand = AlgorandClient.fromConfig({
    algodConfig,
    indexerConfig,
  })
  algorand.setDefaultSigner(transactionSigner)

  const createSession = async () => {
    if (!sessionId || !sessionName) {
      enqueueSnackbar('Please fill in Session ID and Session Name', { variant: 'error' })
      return
    }

    setLoading(true)

    try {
      const factory = new AlgoRewardsContractFactory({
        defaultSender: activeAddress ?? undefined,
        algorand,
      })
      
      const appClient = factory.getAppClientById({ appId: BigInt(743652051) })
      
      const result = await appClient.send.createSession({
        args: {
          sessionId: sessionId,
          sessionName: sessionName,
          sessionDescription: sessionDescription || 'No description provided',
          metadataUrl: 'https://example.com/session-metadata.json'
        }
      })

      enqueueSnackbar(`Session created successfully! Response: ${result.return}`, { variant: 'success' })
      setModalState(false)
      
      // Reset form
      setSessionId('')
      setSessionName('')
      setSessionDescription('')
    } catch (error: any) {
      enqueueSnackbar(`Error creating session: ${error.message}`, { variant: 'error' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <dialog id="session_manager_modal" className={`modal ${openModal ? 'modal-open' : ''} bg-slate-200`}>
      <form method="dialog" className="modal-box">
        <h3 className="font-bold text-lg">Create New Session</h3>
        <p className="text-sm text-gray-600 mb-4">Create a new session for attendees to claim badges</p>
        <br />
        <input
          type="text"
          placeholder="Session ID (e.g., session-001)"
          className="input input-bordered w-full mb-4"
          value={sessionId}
          onChange={(e) => setSessionId(e.target.value)}
        />
        <input
          type="text"
          placeholder="Session Name (e.g., Web3 Masterclass #1)"
          className="input input-bordered w-full mb-4"
          value={sessionName}
          onChange={(e) => setSessionName(e.target.value)}
        />
        <textarea
          placeholder="Session Description (optional)"
          className="textarea textarea-bordered w-full mb-4"
          value={sessionDescription}
          onChange={(e) => setSessionDescription(e.target.value)}
          rows={3}
        />
        <div className="modal-action">
          <button className="btn" onClick={() => setModalState(!openModal)}>
            Close
          </button>
          <button 
            className={`btn btn-primary ${loading ? 'loading' : ''}`} 
            onClick={createSession}
            disabled={loading}
          >
            {loading ? <span className="loading loading-spinner" /> : 'Create Session'}
          </button>
        </div>
      </form>
    </dialog>
  )
}

export default SessionManager
