import QRCode from 'qrcode'
import { useState, useEffect } from 'react'

interface QRCodeGeneratorInterface {
  sessionId: string
  sessionName: string
}

const QRCodeGenerator = ({ sessionId, sessionName }: QRCodeGeneratorInterface) => {
  const [qrCodeUrl, setQrCodeUrl] = useState<string>('')
  const [loading, setLoading] = useState<boolean>(true)

  useEffect(() => {
    const generateQR = async () => {
      try {
        setLoading(true)
        const claimUrl = `${window.location.origin}/claim/${sessionId}`
        const qrDataUrl = await QRCode.toDataURL(claimUrl, {
          width: 256,
          margin: 2,
          color: {
            dark: '#000000',
            light: '#FFFFFF'
          }
        })
        setQrCodeUrl(qrDataUrl)
      } catch (error) {
        console.error('Error generating QR code:', error)
      } finally {
        setLoading(false)
      }
    }

    if (sessionId) {
      generateQR()
    }
  }, [sessionId])

  if (loading) {
    return (
      <div className="text-center">
        <span className="loading loading-spinner loading-lg"></span>
        <p className="mt-2">Generating QR code...</p>
      </div>
    )
  }

  return (
    <div className="text-center">
      <h3 className="font-bold text-lg mb-4">QR Code for {sessionName}</h3>
      {qrCodeUrl && (
        <div className="flex flex-col items-center">
          <img src={qrCodeUrl} alt="QR Code" className="w-64 h-64 mb-4 border-2 border-gray-200 rounded-lg" />
          <p className="text-sm text-gray-600 mb-2">Scan this QR code to claim your badge</p>
          <p className="text-xs text-gray-500 font-mono">Session ID: {sessionId}</p>
        </div>
      )}
    </div>
  )
}

export default QRCodeGenerator
