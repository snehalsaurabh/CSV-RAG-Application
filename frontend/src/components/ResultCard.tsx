import { useState } from 'react'
import type { FounderResult } from '../types'

interface Props {
  result: FounderResult
  onShowMore: (id: string) => void
  expanded?: boolean
  details?: {
    about: string
    idea: string
    keywords: string
    linkedin: string
    notes: string
  }
}

export default function ResultCard({ result, onShowMore, expanded = false, details }: Props) {
  const [isExpanded, setIsExpanded] = useState(expanded)

  const toggle = () => {
    if (!isExpanded) onShowMore(result.id)
    setIsExpanded((v) => !v)
  }

  return (
    <div className="card result">
      <div className="result-header">
        <div>
          <div className="result-title">{result.founder_name}</div>
          <div className="result-sub">{result.role} · {result.company} · {result.location}</div>
        </div>
        <div className="provenance">ID: {result.id} · Row: {result.row_id}</div>
      </div>
      <div className="snippet">{result.snippet}</div>
      <div className="matched">Matched on: {result.matched_fields.join(', ')}</div>
      <button className="link-btn" onClick={toggle}>{isExpanded ? 'Hide details' : 'Show more'}</button>
      {isExpanded && details && (
        <div className="details">
          <p><strong>About:</strong> {details.about}</p>
          <p><strong>Idea:</strong> {details.idea}</p>
          <p><strong>Keywords:</strong> {details.keywords}</p>
          <p><strong>LinkedIn:</strong> <a href={details.linkedin} target="_blank" rel="noreferrer">{details.linkedin}</a></p>
          {details.notes && <p><strong>Notes:</strong> {details.notes}</p>}
        </div>
      )}
    </div>
  )
}


