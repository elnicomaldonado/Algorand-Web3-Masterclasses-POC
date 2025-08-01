// Attendance codes for sessions
// These codes are provided during live events and should remain secret

const SESSION_CODES = {
  "session-3": "INNOVATE",
  "session-4": "DIGITAL", 
  "session-5": "BUILDER",
  "session-6": "FUTURE"
}

// Simple obfuscation function
const obfuscateCode = (code: string): string => {
  return btoa(code).split('').reverse().join('')
}

// Deobfuscate function
const deobfuscateCode = (obfuscated: string): string => {
  return atob(obfuscated.split('').reverse().join(''))
}

// Obfuscated codes
const OBFUSCATED_CODES = {
  "session-3": obfuscateCode(SESSION_CODES["session-3"]),
  "session-4": obfuscateCode(SESSION_CODES["session-4"]),
  "session-5": obfuscateCode(SESSION_CODES["session-5"]),
  "session-6": obfuscateCode(SESSION_CODES["session-6"])
}

export const validateAttendanceCode = (sessionId: string, inputCode: string): boolean => {
  const obfuscatedCode = OBFUSCATED_CODES[sessionId as keyof typeof OBFUSCATED_CODES]
  if (!obfuscatedCode) return false
  
  try {
    const expectedCode = deobfuscateCode(obfuscatedCode)
    return inputCode.toUpperCase() === expectedCode
  } catch {
    return false
  }
}

export default SESSION_CODES 