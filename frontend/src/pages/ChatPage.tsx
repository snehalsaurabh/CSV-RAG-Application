import { useEffect, useMemo, useRef, useState } from 'react'
import api from '../lib/api'
import type { FounderDetails, FounderResult, SearchQuery } from '../types'
import ResultCard from '../components/ResultCard'
import { useAuth } from '../context/AuthContext'

export default function ChatPage() {
  const { logout } = useAuth()
  const [query, setQuery] = useState('healthtech founder in India with AI background')
  // Limit parsing: accept optional trailing "limit:N" token in the query; default 10
  const [limit, setLimit] = useState<number>(10)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [results, setResults] = useState<FounderResult[]>([])
  const [detailsMap, setDetailsMap] = useState<Record<string, FounderDetails | undefined>>({})
  const cacheRef = useRef<Map<string, FounderResult[]>>(new Map())
  const debounceRef = useRef<ReturnType<typeof setTimeout> | null>(null)
  const sentinelRef = useRef<HTMLDivElement | null>(null)
  const PAGE_SIZE = 5
  const [page, setPage] = useState(1)

  // Parse optional limit from query string
  const parsed = useMemo(() => {
    const match = query.match(/^(.*?)(?:\s+limit\s*:\s*(\d{1,2}))?\s*$/i)
    const raw = match?.[1]?.trim() ?? query.trim()
    const lim = match?.[2] ? Math.max(1, Math.min(10, Number(match[2]))) : 10
    return { cleaned: raw, limit: lim }
  }, [query])

  const cleanedQuery = parsed.cleaned

  useEffect(() => {
    setLimit(parsed.limit)
  }, [parsed.limit])

  const search = async () => {
    setLoading(true)
    setError(null)
    try {
      const key = `${cleanedQuery}__${limit}`
      const cached = cacheRef.current.get(key)
      if (cached) {
        setResults(cached)
      } else {
        const payload: SearchQuery = { query: cleanedQuery, limit }
        const { data } = await api.post<FounderResult[]>('/search', payload)
        cacheRef.current.set(key, data)
        setResults(data)
      }
      setPage(1)
    } catch (err) {
      const message = (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail
      setError(message || 'Search failed')
    } finally {
      setLoading(false)
    }
  }

  // Debounced auto-search when query/limit changes
  useEffect(() => {
    if (!cleanedQuery.trim()) return
    if (debounceRef.current) clearTimeout(debounceRef.current)
    debounceRef.current = setTimeout(() => {
      void search()
    }, 600)
    return () => {
      if (debounceRef.current) clearTimeout(debounceRef.current)
    }
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [cleanedQuery, limit])

  const fetchDetails = async (id: string) => {
    if (detailsMap[id]) return
    try {
      const { data } = await api.get<FounderDetails>(`/founder/${id}`)
      setDetailsMap((m) => ({ ...m, [id]: data }))
    } catch {
      // ignore
    }
  }

  

  // IntersectionObserver to auto-load next page
  useEffect(() => {
    const node = sentinelRef.current
    if (!node) return
    const observer = new IntersectionObserver((entries) => {
      const entry = entries[0]
      if (entry.isIntersecting && !loading) {
        const totalPages = Math.max(1, Math.ceil(results.length / PAGE_SIZE))
        setPage((p) => (p < totalPages ? p + 1 : p))
      }
    }, { threshold: 1.0 })
    observer.observe(node)
    return () => observer.disconnect()
  }, [results.length, loading])

  const totalPages = Math.max(1, Math.ceil(results.length / PAGE_SIZE))
  const startIndex = (page - 1) * PAGE_SIZE
  const endIndex = startIndex + PAGE_SIZE
  const visibleResults = results.slice(startIndex, endIndex)

  return (
    <div className="container page-bg">
      <header className="header">
        <h2>Founder RAG Chat</h2>
        <div className="header-actions">
          <button onClick={logout}>Logout</button>
        </div>
      </header>

      <div className="card sticky-search">
        <form className="search-form single" onSubmit={(e) => { e.preventDefault(); void search() }}>
          <input
            className="query-input"
            placeholder="Ask in natural language… (optional: add 'limit: 3' at end; default 10)"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
          <button type="submit" disabled={loading}>{loading ? 'Searching…' : 'Search'}</button>
        </form>
        <div className="muted small">Using limit: {limit}</div>
        {error && <div className="error">{error}</div>}
      </div>

      <div className="results">
        {visibleResults.map(r => (
          <ResultCard
            key={r.id}
            result={r}
            onShowMore={fetchDetails}
            details={detailsMap[r.id] ? {
              about: detailsMap[r.id]!.about,
              idea: detailsMap[r.id]!.idea,
              keywords: detailsMap[r.id]!.keywords,
              linkedin: detailsMap[r.id]!.linkedin,
              notes: detailsMap[r.id]!.notes,
            } : undefined}
          />
        ))}
        {!loading && results.length === 0 && (
          <div className="empty card">
            <div className="title">Try a query</div>
            <div className="subtitle">e.g. “healthtech founder in India with AI background limit: 5”</div>
          </div>
        )}
        {results.length > 0 && (
          <div className="pagination">
            <button disabled={page <= 1} onClick={() => setPage((p) => Math.max(1, p - 1))}>Prev</button>
            <span className="muted small">Page {page} of {totalPages}</span>
            <button disabled={page >= totalPages} onClick={() => setPage((p) => Math.min(totalPages, p + 1))}>Next</button>
          </div>
        )}
        <div ref={sentinelRef} />
      </div>
    </div>
  )
}


