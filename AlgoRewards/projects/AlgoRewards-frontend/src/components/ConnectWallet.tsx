import { useWallet, Wallet, WalletId } from '@txnlab/use-wallet-react'
import Account from './Account'

interface ConnectWalletInterface {
  openModal: boolean
  closeModal: () => void
}

const ConnectWallet = ({ openModal, closeModal }: ConnectWalletInterface) => {
  const { wallets, activeAddress } = useWallet()

  const isKmd = (wallet: Wallet) => wallet.id === WalletId.KMD

  return (
    <dialog id="connect_wallet_modal" className={`modal ${openModal ? 'modal-open' : ''}`} style={{ display: openModal ? 'block' : 'none' }}>
      <form method="dialog" className="modal-box max-w-md bg-white rounded-2xl shadow-2xl">
        <div className="text-center mb-6">
          <div className="inline-flex items-center justify-center w-16 h-16 bg-blue-100 rounded-full mb-4">
            <span className="text-2xl">👛</span>
          </div>
          <h3 className="font-bold text-2xl text-gray-800">Connect Your Wallet</h3>
          <p className="text-gray-600 mt-2">Choose your preferred Algorand wallet</p>
        </div>

        <div className="space-y-4">
          {activeAddress && (
            <div className="bg-green-50 rounded-xl p-4 border border-green-200">
              <div className="flex items-center gap-3 mb-3">
                <div className="w-3 h-3 bg-green-500 rounded-full"></div>
                <span className="font-semibold text-green-700">Connected</span>
              </div>
              <Account />
            </div>
          )}

          {!activeAddress && (
            <div className="space-y-3">
              {wallets?.map((wallet) => (
                <button
                  data-test-id={`${wallet.id}-connect`}
                  className="flex items-center gap-4 w-full p-4 border border-gray-200 rounded-xl hover:border-blue-300 hover:bg-blue-50 transition-all duration-200"
                  key={`provider-${wallet.id}`}
                  onClick={() => {
                    return wallet.connect()
                  }}
                >
                  {!isKmd(wallet) && (
                    <img
                      alt={`wallet_icon_${wallet.id}`}
                      src={wallet.metadata.icon}
                      className="w-8 h-8 object-contain"
                    />
                  )}
                  <span className="font-semibold text-gray-800">
                    {isKmd(wallet) ? 'LocalNet Wallet' : wallet.metadata.name}
                  </span>
                </button>
              ))}
            </div>
          )}
        </div>

        <div className="flex gap-3 mt-6 pt-6 border-t border-gray-200">
          <button
            data-test-id="close-wallet-modal"
            className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg font-semibold transition-colors duration-200"
            onClick={() => {
              closeModal()
            }}
          >
            Close
          </button>
          {activeAddress && (
            <button
              className="flex-1 bg-red-100 hover:bg-red-200 text-red-700 px-4 py-2 rounded-lg font-semibold transition-colors duration-200"
              data-test-id="logout"
              onClick={async () => {
                if (wallets) {
                  const activeWallet = wallets.find((w) => w.isActive)
                  if (activeWallet) {
                    await activeWallet.disconnect()
                    closeModal() // Close modal after disconnect
                  } else {
                    // Required for logout/cleanup of inactive providers
                    // For instance, when you login to localnet wallet and switch network
                    // to testnet/mainnet or vice verse.
                    localStorage.removeItem('@txnlab/use-wallet:v3')
                    window.location.reload()
                  }
                }
              }}
            >
              🚪 Disconnect
            </button>
          )}
        </div>
      </form>
    </dialog>
  )
}
export default ConnectWallet
