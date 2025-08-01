import { useWallet } from '@txnlab/use-wallet-react'
import React, { useState } from 'react'
import ConnectWallet from './components/ConnectWallet'
import RealNFTClaimer from './components/RealNFTClaimer'
import NFTGallery from './components/NFTGallery'
import { validateAttendanceCode } from './config/attendanceCodes'

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

interface SessionsConfig {
  [key: string]: SessionData
}

// Sessions configuration - all 6 sessions
const SESSIONS_CONFIG: SessionsConfig = {
  "session-3": {
    id: "session-3",
    name: "From concept to creation: designing your solution with blockchain",
    date: "August 5",
    time: "12:00 PM ET / 06:00 PM CEST",
    topics: [
      "From idea to startup: The power of testing",
      "User feedback to refine your idea", 
      "Aligning and enhancing your idea with blockchain"
    ],
    color: "#8B5CF6", // Purple
    unitName: "S3BADGE",
    badgeName: "Session 3 Badge - AlgoRewards",
    imageUrl: "https://via.placeholder.com/400x400/8B5CF6/FFFFFF?text=Session+3+Badge",
    active: true // Currently active
  },
  "session-4": {
    id: "session-4",
    name: "NFTs & beyond: mastering blockchain for builders",
    date: "August 7",
    time: "12:00 PM ET / 06:00 PM CEST",
    topics: [
      "NFTs unpacked: What they are and why they matter",
      "Exploring NFT use cases",
      "Why Algorand for NFTs?",
      "Hands-on activity: minting an NFT using no-code tools"
    ],
    color: "#059669", // Green
    unitName: "S4BADGE",
    badgeName: "Session 4 Badge - AlgoRewards",
    imageUrl: "https://via.placeholder.com/400x400/059669/FFFFFF?text=Session+4+Badge",
    active: true // Currently active
  },
  "session-5": {
    id: "session-5",
    name: "Create, transfer, innovate: no-code tools on Algorand",
    date: "August 12",
    time: "12:00 PM ET / 06:00 PM CEST",
    topics: [
      "What is an asset on a blockchain?",
      "Understanding Algorand Standard Assets (ASA)",
      "Hands-on activity: minting your asset",
      "Intro to Lora: A no-code tool on Algorand",
      "Building and executing transactions",
      "Start building your pitch deck"
    ],
    color: "#DC2626", // Red
    unitName: "S5BADGE",
    badgeName: "Session 5 Badge - AlgoRewards",
    imageUrl: "https://via.placeholder.com/400x400/DC2626/FFFFFF?text=Session+5+Badge",
    active: true // Currently active
  },
  "session-6": {
    id: "session-6",
    name: "Final presentations, networking, and your next steps",
    date: "August 14",
    time: "12:00 PM ET / 06:00 PM CEST",
    topics: [
      "Algorand Foundation Builders and Startup Programs",
      "Web3 masterclasses, Startup Challenges, Accelerator and More",
      "Present your idea (Optional but encouraged)"
    ],
    color: "#7C3AED", // Indigo
    unitName: "S6BADGE",
    badgeName: "Session 6 Badge - AlgoRewards",
    imageUrl: "https://via.placeholder.com/400x400/7C3AED/FFFFFF?text=Session+6+Badge",
    active: true // Currently active
  }
}

const Home = () => {
  const { activeAddress, wallets } = useWallet()
  const [openWalletModal, setOpenWalletModal] = useState(false)
  const [realNFTClaimerModal, setRealNFTClaimerModal] = useState(false)
  const [selectedSession, setSelectedSession] = useState<string>("session-3")
  const [attendanceCode, setAttendanceCode] = useState("")
  const [isCodeValid, setIsCodeValid] = useState(false)

  // Get active sessions
  const activeSessions = Object.values(SESSIONS_CONFIG).filter(session => session.active)
  const currentSession = SESSIONS_CONFIG[selectedSession]

  const checkAttendanceCode = (code: string) => {
    // Check if the code matches the current session's attendance code
    return validateAttendanceCode(selectedSession, code)
  }

  const handleAttendanceCodeChange = (code: string) => {
    setAttendanceCode(code)
    setIsCodeValid(checkAttendanceCode(code))
  }

  const handleClaimAttendance = () => {
    if (isCodeValid && activeAddress) {
      setRealNFTClaimerModal(true)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Header */}
      <header className="border-b border-slate-800 bg-slate-900/50 backdrop-blur-sm">
        <div className="container mx-auto px-4 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
              <span className="text-white text-lg">🎁</span>
            </div>
            <h1 className="text-xl font-bold text-white">AlgoRewards</h1>
          </div>

          {!activeAddress ? (
            <button
              onClick={() => setOpenWalletModal(true)}
              className="bg-purple-600 hover:bg-purple-700 text-white px-4 py-2 rounded-lg font-semibold transition-colors duration-200 flex items-center"
            >
              <span className="mr-2">🔗</span>
              Connect Wallet
            </button>
          ) : (
            <div className="flex items-center space-x-3">
              <div className="bg-green-900/50 text-green-300 border border-green-700 px-3 py-1 rounded-full text-sm font-semibold flex items-center">
                <span className="w-2 h-2 bg-green-400 rounded-full mr-2 animate-pulse"></span>
                Connected
              </div>
              <span className="text-sm text-slate-300 font-mono">
                {activeAddress.slice(0, 6)}...{activeAddress.slice(-4)}
              </span>
              <button
                onClick={async () => {
                  if (wallets) {
                    const activeWallet = wallets.find((w) => w.isActive)
                    if (activeWallet) {
                      await activeWallet.disconnect()
                    } else {
                      // Required for logout/cleanup of inactive providers
                      localStorage.removeItem('@txnlab/use-wallet:v3')
                      window.location.reload()
                    }
                  }
                }}
                className="bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded-lg text-sm font-semibold transition-colors duration-200 flex items-center"
              >
                <span className="mr-1">🚪</span>
                Logout
              </button>
            </div>
          )}
        </div>
      </header>

      <main className="container mx-auto px-4 py-8 space-y-12">
        {/* Hero Section */}
        <section className="text-center space-y-6">
          <div className="space-y-4">
            <h2 className="text-4xl md:text-6xl font-bold text-white">Proof of Attendance</h2>
            <p className="text-xl text-slate-300 max-w-2xl mx-auto">
              Verify your participation in Algorand masterclasses and earn blockchain-verified certificates
            </p>
          </div>
        </section>

        {/* How It Works */}
        <section className="space-y-6">
          <h3 className="text-2xl font-bold text-white text-center">How It Works</h3>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-slate-800/30 border border-slate-700 rounded-xl text-center">
              <div className="p-6">
                <div className="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold">1</span>
                </div>
                <h4 className="font-semibold text-white mb-2">Attend Event</h4>
                <p className="text-slate-400 text-sm">Join an Algorand masterclass and participate actively</p>
              </div>
            </div>

            <div className="bg-slate-800/30 border border-slate-700 rounded-xl text-center">
              <div className="p-6">
                <div className="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold">2</span>
                </div>
                <h4 className="font-semibold text-white mb-2">Get Code</h4>
                <p className="text-slate-400 text-sm">Receive a unique attendance code during the event</p>
              </div>
            </div>

            <div className="bg-slate-800/30 border border-slate-700 rounded-xl text-center">
              <div className="p-6">
                <div className="w-12 h-12 bg-purple-600 rounded-full flex items-center justify-center mx-auto mb-4">
                  <span className="text-white font-bold">3</span>
                </div>
                <h4 className="font-semibold text-white mb-2">Claim NFT</h4>
                <p className="text-slate-400 text-sm">Mint your proof of attendance as an NFT on Algorand</p>
              </div>
            </div>
          </div>
        </section>

        {/* Available Sessions */}
        <section className="space-y-6">
          <h3 className="text-2xl font-bold text-white text-center">Available Sessions</h3>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {activeSessions.map((session) => (
              <div 
                key={session.id}
                className={`bg-slate-800/50 border rounded-xl p-6 cursor-pointer transition-all duration-200 ${
                  selectedSession === session.id 
                    ? 'border-purple-500 bg-slate-800/70' 
                    : 'border-slate-700 hover:border-slate-600'
                }`}
                onClick={() => setSelectedSession(session.id)}
              >
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div 
                      className="w-4 h-4 rounded-full" 
                      style={{ backgroundColor: session.color }}
                    ></div>
                    <h4 className="font-semibold text-white text-lg">{session.name}</h4>
                  </div>
                  {selectedSession === session.id && (
                    <div className="bg-purple-600 text-white px-2 py-1 rounded-full text-xs font-semibold">
                      Selected
                    </div>
                  )}
                </div>
                
                <div className="space-y-3">
                  <div className="flex items-center space-x-2 text-slate-300">
                    <span>📅</span>
                    <span>{session.date} | {session.time}</span>
                  </div>
                  
                  <div className="space-y-2">
                    <p className="text-sm text-slate-400 font-medium">Topics:</p>
                    <ul className="space-y-1">
                      {session.topics.slice(0, 2).map((topic, index) => (
                        <li key={index} className="text-xs text-slate-400 flex items-start space-x-2">
                          <span className="w-1 h-1 bg-slate-500 rounded-full mt-2 flex-shrink-0"></span>
                          <span>{topic}</span>
                        </li>
                      ))}
                      {session.topics.length > 2 && (
                        <li className="text-xs text-slate-500">
                          +{session.topics.length - 2} more topics
                        </li>
                      )}
                    </ul>
                  </div>
                  
                  <div className="pt-2">
                    <div className="text-xs text-slate-500">
                      Secret code provided during event
                    </div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Current Event */}
        <section className="space-y-6">
          <h3 className="text-2xl font-bold text-white text-center">Claim Your Badge</h3>

          <div className="bg-slate-800/50 border border-slate-700 rounded-xl backdrop-blur-sm">
            <div className="p-6">
              <div className="flex items-start justify-between mb-6">
                <div className="space-y-2">
                  <h3 className="text-white text-xl font-bold">{currentSession.name}</h3>
                  <p className="text-slate-300">
                    Session {currentSession.id.split('-')[1]} - {currentSession.topics.length} learning topics
                  </p>
                </div>
                <div className="bg-green-900/50 text-green-300 border border-green-700 px-3 py-1 rounded-full text-sm font-semibold">
                  Live Now
                </div>
              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="space-y-4">
                  <div className="flex items-center space-x-3 text-slate-300">
                    <span className="text-purple-400">📅</span>
                    <span>{currentSession.date}</span>
                  </div>
                  <div className="flex items-center space-x-3 text-slate-300">
                    <span className="text-purple-400">🕐</span>
                    <span>{currentSession.time}</span>
                  </div>
                  <div className="flex items-center space-x-3 text-slate-300">
                    <span className="text-purple-400">📍</span>
                    <span>Virtual Event</span>
                  </div>
                  <div className="flex items-center space-x-3 text-slate-300">
                    <span className="text-purple-400">👥</span>
                    <span>AlgoRewards Masterclass</span>
                  </div>
                  
                  <div className="bg-slate-900/50 p-4 rounded-lg border border-slate-700">
                    <h4 className="font-semibold text-white mb-3">Learning Topics:</h4>
                    <ul className="space-y-2">
                      {currentSession.topics.map((topic, index) => (
                        <li key={index} className="text-sm text-slate-300 flex items-start space-x-2">
                          <span className="w-1.5 h-1.5 bg-purple-400 rounded-full mt-2 flex-shrink-0"></span>
                          <span>{topic}</span>
                        </li>
                      ))}
                    </ul>
                  </div>
                </div>

                <div className="space-y-4">
                  <div className="p-4 bg-slate-900/50 rounded-lg border border-slate-700">
                    <h4 className="font-semibold text-white mb-2">Claim Your Attendance</h4>
                    <div className="space-y-3">
                      <div>
                        <label htmlFor="attendance-code" className="text-slate-300 text-sm font-medium">
                          Attendance Code
                        </label>
                        <input
                          id="attendance-code"
                          type="text"
                          placeholder="Enter code provided during event"
                          value={attendanceCode}
                          onChange={(e) => handleAttendanceCodeChange(e.target.value)}
                          className="w-full mt-1 px-3 py-2 bg-slate-800 border border-slate-600 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-purple-500"
                        />
                      </div>
                      <button
                        onClick={handleClaimAttendance}
                        disabled={!activeAddress || !isCodeValid}
                        className={`w-full py-2 px-4 rounded-lg font-semibold transition-colors duration-200 flex items-center justify-center ${
                          activeAddress && isCodeValid
                            ? 'bg-purple-600 hover:bg-purple-700 text-white'
                            : 'bg-slate-700 text-slate-400 cursor-not-allowed'
                        }`}
                      >
                        <span className="mr-2">🎨</span>
                        Claim {currentSession.badgeName}
                      </button>
                      {attendanceCode && !isCodeValid && (
                        <p className="text-red-400 text-sm">Invalid attendance code</p>
                      )}
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* NFT Collection - Only show when wallet is connected */}
        {activeAddress && (
          <section className="space-y-6">
            <h3 className="text-2xl font-bold text-white text-center">🖼️ Your NFT Collection</h3>
            <NFTGallery />
          </section>
        )}

        <ConnectWallet
          openModal={openWalletModal}
          closeModal={() => setOpenWalletModal(false)}
        />

        <RealNFTClaimer
          sessionId={currentSession.id}
          sessionName={currentSession.name}
          sessionData={currentSession}
          attendanceCode={attendanceCode}
          openModal={realNFTClaimerModal}
          setModalState={setRealNFTClaimerModal}
        />
      </main>

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-900/50 mt-16">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between space-y-4 md:space-y-0">
            <div className="flex items-center space-x-2">
              <div className="w-6 h-6 bg-gradient-to-r from-purple-500 to-pink-500 rounded-lg flex items-center justify-center">
                <span className="text-white text-sm">🎁</span>
              </div>
              <span className="text-slate-300">AlgoRewards</span>
            </div>

            <div className="flex items-center space-x-6 text-sm text-slate-400">
              <a href="#" className="hover:text-white transition-colors">
                About
              </a>
              <a href="#" className="hover:text-white transition-colors">
                Events
              </a>
              <a href="#" className="hover:text-white transition-colors">
                Support
              </a>
              <a href="#" className="hover:text-white transition-colors flex items-center space-x-1">
                <span>Algorand</span>
                <span>🔗</span>
              </a>
            </div>
          </div>

          <div className="border-t border-slate-800 my-6"></div>

          <div className="text-center text-sm text-slate-500">
            <p>© 2025 AlgoRewards. Built on Algorand blockchain.</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home