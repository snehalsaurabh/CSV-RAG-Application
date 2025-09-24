import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import api from '../lib/api'
import { useAuth } from '../context/AuthContext'
import type { StatsResponse } from '../types'


function formatNumber(num: number): string {
  return num.toLocaleString()
}

function calculatePercentage(value: number, total: number): number {
  return (value / total) * 100
}

export default function StatsPage() {
  const { logout } = useAuth()
  const [stats, setStats] = useState<StatsResponse | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    const fetchStats = async () => {
      setLoading(true)
      setError(null)
      try {
        const { data } = await api.get<StatsResponse>('/stats')
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

  return (
    <div className="container page-bg">
      <header className="header">
        <h2>Founder Statistics</h2>
        <div className="header-actions">
          <Link to="/">
            <button>← Back to Chat</button>
          </Link>
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      <div className="stats-overview card">
        <h3 className="stats-title">📊 Overview</h3>
        <div className="stats-highlights">
          <div className="highlight-item">
            <div className="highlight-number">{formatNumber(stats.total_founders)}</div>
            <div className="highlight-label">Total Founders</div>
          </div>
          <div className="highlight-item">
            <div className="highlight-number">{formatNumber(stats.unique_companies)}</div>
            <div className="highlight-label">Companies</div>
          </div>
          <div className="highlight-item">
            <div className="highlight-number">{formatNumber(stats.unique_locations)}</div>
            <div className="highlight-label">Locations</div>
          </div>
          <div className="highlight-item">
            <div className="highlight-number">{formatNumber(stats.total_documented_achievements)}</div>
            <div className="highlight-label">Achievements</div>
          </div>
        </div>
      </div>

      <div className="stats-grid">
        {/* Roles Distribution */}
        <div className="card">
          <h3 className="stats-title">👥 Roles Distribution</h3>
          <div className="stats-list">
            {Object.entries(stats.roles).map(([role, count], index) => (
              <div key={role} className="stats-item">
                <div className="stats-rank">#{index + 1}</div>
                <div className="stats-label">{role}</div>
                <div className="stats-value">{count}</div>
                <div className="stats-bar">
                  <div
                    className="stats-bar-fill"
                    style={{ width: `${calculatePercentage(count, stats.total_founders)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Industry Distribution */}
        <div className="card">
          <h3 className="stats-title">🏢 Industry Distribution</h3>
          <div className="stats-list">
            {Object.entries(stats.industry_distribution).map(([industry, count], index) => (
              <div key={industry} className="stats-item">
                <div className="stats-rank">#{index + 1}</div>
                <div className="stats-label">{industry}</div>
                <div className="stats-value">{count}</div>
                <div className="stats-bar">
                  <div
                    className="stats-bar-fill"
                    style={{ width: `${calculatePercentage(count, stats.total_founders)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Top Skills */}
        <div className="card">
          <h3 className="stats-title">� Key Skills</h3>
          <div className="stats-list">
            {Object.entries(stats.top_skills).map(([skill, count], index) => (
              <div key={skill} className="stats-item">
                <div className="stats-rank">#{index + 1}</div>
                <div className="stats-label">{skill}</div>
                <div className="stats-value">{count}</div>
                <div className="stats-bar">
                  <div
                    className="stats-bar-fill"
                    style={{ width: `${calculatePercentage(count, stats.total_founders)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Notable Backgrounds */}
        <div className="card">
          <h3 className="stats-title">🎯 Notable Backgrounds</h3>
          <div className="stats-list">
            {Object.entries(stats.top_backgrounds).map(([background, count], index) => (
              <div key={background} className="stats-item">
                <div className="stats-rank">#{index + 1}</div>
                <div className="stats-label">{background}</div>
                <div className="stats-value">{count}</div>
                <div className="stats-bar">
                  <div
                    className="stats-bar-fill"
                    style={{ width: `${calculatePercentage(count, stats.total_founders)}%` }}
                  />
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Diversity Insights */}
        <div className="stats-insights card">
          <h3 className="stats-title">🌈 Diversity Insights</h3>
          <div className="insights-grid">
            <div className="insight-item">
              <div className="insight-icon">�</div>
              <div className="insight-content">
                <div className="insight-value">{stats.geographic_coverage}</div>
                <div className="insight-label">Geographic Coverage</div>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon">�</div>
              <div className="insight-content">
                <div className="insight-value">{stats.diversity_score.role_diversity}</div>
                <div className="insight-label">Role Diversity</div>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon">🔧</div>
              <div className="insight-content">
                <div className="insight-value">{stats.diversity_score.skill_diversity}</div>
                <div className="insight-label">Skill Diversity</div>
              </div>
            </div>
            <div className="insight-item">
              <div className="insight-icon">🎯</div>
              <div className="insight-content">
                <div className="insight-value">{stats.diversity_score.background_diversity}</div>
                <div className="insight-label">Background Diversity</div>
              </div>
            </div>
          </div>
        </div>

        {/* Sample Achievements */}
        <div className="card">
          <h3 className="stats-title">🏆 Notable Achievements</h3>
          <div className="stats-list">
            {stats.sample_achievements.map((achievement, index) => (
              <div key={index} className="stats-item">
                <div className="stats-rank">#{index + 1}</div>
                <div className="stats-label">{achievement}</div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
