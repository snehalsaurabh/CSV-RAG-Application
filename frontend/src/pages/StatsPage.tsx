import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../lib/api'
import type { StatsData } from '../types'
import { useAuth } from '../context/AuthContext'

export default function StatsPage() {
  const { logout } = useAuth()
  const [stats, setStats] = useState<StatsData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true)
      setError(null)
      try {
        const { data } = await api.get<StatsData>('/stats')
        setStats(data)
      } catch (err) {
        const message = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
        setError(message || 'Failed to load statistics')
      } finally {
        setLoading(false)
      }
    }

    void fetchStats()
  }, [])

  if (loading) {
    return (
      <div className="container page-bg">
        <header className="header">
          <h2>Dataset Statistics</h2>
          <div className="header-actions">
            <Link to="/">
              <button>← Back to Chat</button>
            </Link>
            <button onClick={logout}>Logout</button>
          </div>
        </header>
        <div className="card">
          <div className="title">Loading statistics...</div>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="container page-bg">
        <header className="header">
          <h2>Dataset Statistics</h2>
          <div className="header-actions">
            <Link to="/">
              <button>← Back to Chat</button>
            </Link>
            <button onClick={logout}>Logout</button>
          </div>
        </header>
        <div className="error">{error}</div>
      </div>
    )
  }

  if (!stats) {
    return null
  }

  // Convert objects to sorted arrays for display
  const sortedRoles = Object.entries(stats.roles)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 10)

  const sortedStages = Object.entries(stats.stages)
    .sort(([, a], [, b]) => b - a)

  const sortedKeywords = Object.entries(stats.top_keywords)
    .sort(([, a], [, b]) => b - a)

  return (
    <div className="container page-bg">
      <header className="header">
        <h2>Dataset Statistics</h2>
        <div className="header-actions">
          <Link to="/">
            <button>← Back to Chat</button>
          </Link>
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      <div className="stats-grid">
        {/* Overview Card */}
        <div className="card stats-overview">
          <h3 className="stats-title">📊 Dataset Overview</h3>
          <div className="stats-highlights">
            <div className="highlight-item">
              <div className="highlight-number">{stats.total_founders.toLocaleString()}</div>
              <div className="highlight-label">Total Founders</div>
            </div>
            <div className="highlight-item">
              <div className="highlight-number">{stats.locations.toLocaleString()}</div>
              <div className="highlight-label">Unique Locations</div>
            </div>
            <div className="highlight-item">
              <div className="highlight-number">{Object.keys(stats.roles).length}</div>
              <div className="highlight-label">Different Roles</div>
            </div>
            <div className="highlight-item">
              <div className="highlight-number">{Object.keys(stats.stages).length}</div>
              <div className="highlight-label">Company Stages</div>
            </div>
          </div>
        </div>

        {/* Top Roles Card */}
        <div className="card">
          <h3 className="stats-title">👥 Top Founder Roles</h3>
          <div className="stats-list">
            {sortedRoles.map(([role, count], index) => (
              <div key={role} className="stats-item">
                <div className="stats-rank">#{index + 1}</div>
                <div className="stats-label">{role}</div>
                <div className="stats-value">{count}</div>
                <div className="stats-bar">
                  <div 
                    className="stats-bar-fill" 
                    style={{ width: `${(count / sortedRoles[0][1]) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Company Stages Card */}
        <div className="card">
          <h3 className="stats-title">🚀 Company Stages</h3>
          <div className="stats-list">
            {sortedStages.map(([stage, count], index) => (
              <div key={stage} className="stats-item">
                <div className="stats-rank">#{index + 1}</div>
                <div className="stats-label">{stage}</div>
                <div className="stats-value">{count}</div>
                <div className="stats-bar">
                  <div 
                    className="stats-bar-fill" 
                    style={{ width: `${(count / sortedStages[0][1]) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Keywords Card */}
        <div className="card">
          <h3 className="stats-title">🔍 Most Popular Keywords</h3>
          <div className="stats-list">
            {sortedKeywords.map(([keyword, count], index) => (
              <div key={keyword} className="stats-item">
                <div className="stats-rank">#{index + 1}</div>
                <div className="stats-label">{keyword}</div>
                <div className="stats-value">{count}</div>
                <div className="stats-bar">
                  <div 
                    className="stats-bar-fill" 
                    style={{ width: `${(count / sortedKeywords[0][1]) * 100}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Quality Insights Card */}
        <div className="card stats-insights">
          <h3 className="stats-title">💡 Dataset Quality Insights</h3>
          <div className="insights-grid">
            <div className="insight-item">
              <div className="insight-icon">🌍</div>
              <div className="insight-content">
                <div className="insight-value">{stats.locations}</div>
                <div className="insight-label">Global reach across {stats.locations} unique locations</div>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon">📈</div>
              <div className="insight-content">
                <div className="insight-value">{((Object.keys(stats.top_keywords).length / stats.total_founders) * 100).toFixed(1)}%</div>
                <div className="insight-label">Keyword diversity ratio shows rich profile data</div>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon">🎯</div>
              <div className="insight-content">
                <div className="insight-value">{Object.keys(stats.roles).length}</div>
                <div className="insight-label">Role diversity enables precise matching</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
