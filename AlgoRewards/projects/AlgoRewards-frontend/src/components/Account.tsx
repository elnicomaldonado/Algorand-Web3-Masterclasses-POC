import { useWallet } from '@txnlab/use-wallet-react'
import { useMemo } from 'react'
import { ellipseAddress } from '../utils/ellipseAddress'
import { getAlgodConfigFromViteEnvironment } from '../utils/network/getAlgoClientConfigs'

const Account = () => {
  const { activeAddress } = useWallet()
  const algoConfig = getAlgodConfigFromViteEnvironment()

  const networkName = useMemo(() => {
    return algoConfig.network === '' ? 'localnet' : algoConfig.network.toLocaleLowerCase()
  }, [algoConfig.network])

  return (
    <div className="space-y-2">
      <div>
        <span className="text-sm text-gray-600">Address:</span>
        <a 
          className="block font-mono text-sm text-blue-600 hover:text-blue-700 transition-colors" 
          target="_blank" 
          href={`https://lora.algokit.io/${networkName}/account/${activeAddress}/`}
          rel="noopener noreferrer"
        >
          {ellipseAddress(activeAddress)} 🔗
        </a>
      </div>
      <div>
        <span className="text-sm text-gray-600">Network:</span>
        <span className="ml-2 text-sm font-semibold text-orange-600 capitalize">{networkName}</span>
      </div>
    </div>
  )
}

export default Account
