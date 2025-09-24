import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

export default function LoginPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const onSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await login(username, password)
      navigate('/')
    } catch (err) {
      const message = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(message || 'Login failed')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="container page-bg">
      <div className="card auth-card">
        <h1 className="title">Founder RAG Chat</h1>
        <p className="subtitle">AI-powered founder matching and discovery</p>
        {error && <div className="error">{error}</div>}
        <form onSubmit={onSubmit} className="form">
          <label>
            Username
            <input value={username} onChange={(e) => setUsername(e.target.value)} placeholder="demo" required />
          </label>
          <label>
            Password
            <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="demo" required />
          </label>
          <button disabled={loading} type="submit">{loading ? 'Signing in...' : 'Sign In'}</button>
        </form>
        <div className="hint-box">
          <div className="hint-title">Demo Credentials:</div>
          <div className="hint-row">Username: <code>demo</code> | Password: <code>demo</code></div>
          <div className="hint-row">Username: <code>admin</code> | Password: <code>demo</code></div>
        </div>
      </div>
    </div>
  )
}


