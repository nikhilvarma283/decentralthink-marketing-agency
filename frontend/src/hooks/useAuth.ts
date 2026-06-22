import { useState, useEffect } from 'react'

interface AuthState {
  isAuthenticated: boolean
  user: null | { id: string; email: string; role: string }
  token: null | string
}

export function useAuth() {
  const [auth, setAuth] = useState<AuthState>({
    isAuthenticated: false,
    user: null,
    token: null,
  })

  useEffect(() => {
    // Check for stored token on mount
    const token = localStorage.getItem('auth_token')
    if (token) {
      setAuth((prev) => ({
        ...prev,
        isAuthenticated: true,
        token,
      }))
    }
  }, [])

  const login = (token: string, user: AuthState['user']) => {
    localStorage.setItem('auth_token', token)
    setAuth({
      isAuthenticated: true,
      token,
      user,
    })
  }

  const logout = () => {
    localStorage.removeItem('auth_token')
    setAuth({
      isAuthenticated: false,
      token: null,
      user: null,
    })
  }

  return {
    ...auth,
    login,
    logout,
  }
}
