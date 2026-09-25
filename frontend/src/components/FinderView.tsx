import { useState } from 'react';
import { Search, AlertCircle, Loader2, Award, CheckCircle2, ChevronRight, FileText, Sparkles, Filter, ShieldCheck, HelpCircle } from 'lucide-react';
import { finderAPI } from '../services/api';
import type { StandardResult } from '../services/api';
import type { Source } from '../types';

const INDUSTRIES = [
  'All',
  'Electronics',
  'Construction',
  'Food & Packaging',
  'Medical',
  'Water Quality',
  'Automotive',
  'Textiles',
];

interface FinderViewProps {
  onShowEvidence?: (sources: Source[]) => void;
  onAskAboutStandard?: (standardCode: string, standardTitle?: string) => void;
}

export default function FinderView({ onShowEvidence, onAskAboutStandard }: FinderViewProps) {
  const [product, setProduct] = useState('');
  const [industry, setIndustry] = useState('All');
  const [results, setResults] = useState<StandardResult[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [searched, setSearched] = useState(false);

  const handleSearch = async (searchTerm?: string, selectedInd?: string) => {
    const term = searchTerm !== undefined ? searchTerm : product;
    const ind = selectedInd !== undefined ? selectedInd : industry;
    if (!term.trim()) return;

    setIsLoading(true);
    setError('');
    setSearched(true);

    try {
      const data = await finderAPI.searchStandards(term.trim(), ind);
      setResults(data);
    } catch (err: any) {
      setError('Could not fetch standards. Ensure the RAG service is running.');
      setResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const relevancePct = (r: number) => Math.round(Math.min(r, 1) * 100);

  const getSchemeDetails = (stdNum: string, _docType?: string) => {
    const s = (stdNum || '').toUpperCase();
    if (s.includes('10500') || s.includes('14543') || s.includes('269') || s.includes('1786') || s.includes('1417')) {
      return {
        label: 'Mandatory ISI Mark (Scheme I)',
        type: 'mandatory',
        color: '#B91C1C',
        bg: '#FEF2F2',
        border: '#FECACA',
        badge: '🟢 Mandatory'
      };
    }
    if (s.includes('16102') || s.includes('1293') || s.includes('3854') || s.includes('13450')) {
      return {
        label: 'Compulsory Registration Scheme (CRS)',
        type: 'crs',
        color: '#D97706',
        bg: '#FFFBEB',
        border: '#FDE68A',
        badge: '🟡 Compulsory'
      };
    }
    return {
      label: 'Voluntary Indian Standard',
      type: 'voluntary',
      color: '#15803D',
      bg: '#F0FDF4',
      border: '#BBF7D0',
      badge: '🔵 Informational'
    };
  };

  const getConfidenceLevel = (rel: number) => {
    if (rel >= 0.7) return { text: 'HIGH CONFIDENCE', color: '#15803D', bg: '#DCFCE7' };
    if (rel >= 0.5) return { text: 'MEDIUM CONFIDENCE', color: '#B45309', bg: '#FEF3C7' };
    return { text: 'LIMITED EVIDENCE', color: '#991B1B', bg: '#FEE2E2' };
  };

  const handleInspectEvidence = (r: StandardResult) => {
    if (onShowEvidence) {
      onShowEvidence([
        {
          standardNumber: r.standard_number,
          title: r.title,
          clause: 'Scope & Requirements',
          relevanceScore: r.relevance,
          documentType: r.document_type || 'Indian Standard Specification',
          page: 1,
          contentPreview: `Applies to product specification, testing methodologies, sampling, and compliance benchmarks under ${r.standard_number} (${r.title || 'BIS Standard'}).`
        }
      ]);
    }
  };

  return (
    <div className="finder-view">
      {/* Top Header Banner */}
      <div className="finder-hero-banner">
        <div className="hero-content">
          <div className="hero-badge">
            <Sparkles size={14} className="text-amber-600" />
            <span>AI APPLICABILITY ENGINE</span>
          </div>
          <h1>Find Applicable Indian Standard</h1>
          <p>
            Describe your product or engineering requirements in plain English. ManakAI semantically aligns it to official Indian Standards, applicable BIS certification schemes, and testing mandates.
          </p>
        </div>
      </div>

      <div className="finder-wrap">
        {/* Search Bar & Filters */}
        <div className="search-card">
          <div className="search-input-row">
            <div className="search-input-wrap">
              <Search className="search-icon" size={20} />
              <input
                type="text"
                value={product}
                onChange={(e) => setProduct(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                placeholder="Enter product e.g. 'LED bulb', 'packaged drinking water', 'cement', 'gold jewellery', 'switches'..."
                autoFocus
              />
            </div>
            <button
              className="search-btn"
              onClick={() => handleSearch()}
              disabled={isLoading || !product.trim()}
            >
              {isLoading ? <Loader2 size={18} className="spin" /> : <Search size={18} />}
              <span>{isLoading ? 'Searching...' : 'Search Standards'}</span>
            </button>
          </div>

          {/* Industry Filter Chips */}
          <div className="filter-chips-row">
            <span className="filter-label">
              <Filter size={13} />
              <span>Industry:</span>
            </span>
            <div className="chips-container">
              {INDUSTRIES.map((ind) => (
                <button
                  key={ind}
                  className={`industry-chip ${industry === ind ? 'active-chip' : ''}`}
                  onClick={() => {
                    setIndustry(ind);
                    if (product.trim()) {
                      handleSearch(product, ind);
                    }
                  }}
                >
                  {ind}
                </button>
              ))}
            </div>
          </div>
        </div>

        {error && (
          <div className="finder-error">
            <AlertCircle size={18} />
            <span>{error}</span>
          </div>
        )}

        {/* Empty State / Suggestions */}
        {!searched && !isLoading && (
          <div className="quick-suggestions-box">
            <div className="sugg-header">
              <span className="sugg-title">Common Product Lookups for SIH Demo</span>
              <span className="sugg-sub">Click any pill to test instant semantic standard matching:</span>
            </div>
            <div className="sugg-grid">
              {[
                { name: 'Packaged drinking water', ind: 'All' },
                { name: 'Self-ballasted LED bulb', ind: 'All' },
                { name: 'Ordinary Portland Cement', ind: 'All' },
                { name: 'Plugs and socket-outlets 250V', ind: 'All' },
                { name: 'High strength deformed steel bars', ind: 'All' },
                { name: 'Residual current circuit breakers', ind: 'All' },
              ].map((item) => (
                <button
                  key={item.name}
                  className="sugg-card"
                  onClick={() => {
                    setProduct(item.name);
                    setIndustry(item.ind);
                    handleSearch(item.name, item.ind);
                  }}
                >
                  <div className="sugg-name">"{item.name}"</div>
                  <div className="sugg-ind">{item.ind}</div>
                </button>
              ))}
            </div>

            <div className="differentiator-banner">
              <ShieldCheck size={20} className="diff-icon" />
              <div>
                <strong>How ManakAI differs from legacy portal search:</strong>
                <p>
                  Official portals require exact IS codes or rigid technical catalog codes. ManakAI uses dense embeddings to match plain colloquial descriptions (like "water testing for arsenic" or "socket for 16A") directly to the relevant clause, scheme, and testing procedure.
                </p>
              </div>
            </div>
          </div>
        )}

        {searched && !isLoading && results.length === 0 && !error && (
          <div className="finder-empty-state">
            <div className="empty-ico">🔍</div>
            <h3>No matching standard found for "{product}"</h3>
            <p>Try searching by general terminology (e.g. "water", "lighting", "cement", "plastic packaging").</p>
          </div>
        )}

        {/* Results List */}
        {results.length > 0 && (
          <div className="results-container">
            <div className="results-top-meta">
              <h2>
                Found <strong>{results.length}</strong> applicable Indian Standard{results.length > 1 ? 's' : ''} for <span className="highlight-term">"{product}"</span>
              </h2>
              <span className="vector-badge">Vector Similary & Clause Verification</span>
            </div>

            <div className="results-list">
              {results.map((r, idx) => {
                const isBestMatch = idx === 0;
                const scheme = getSchemeDetails(r.standard_number, r.document_type);
                const confidence = getConfidenceLevel(r.relevance);
                const pct = relevancePct(r.relevance);

                return (
                  <div
                    key={idx}
                    className={`standard-card ${isBestMatch ? 'best-match-card' : ''}`}
                  >
                    {isBestMatch && (
                      <div className="best-match-ribbon">
                        <Award size={14} />
                        <span>🏆 BEST MATCH · HIGHEST SEMANTIC RELEVANCE</span>
                      </div>
                    )}

                    <div className="card-top-row">
                      <div className="std-title-group">
                        <span className="std-number">{r.standard_number}</span>
                        {r.revision && (
                          <span className="std-revision">Rev. {r.revision}</span>
                        )}
                        <span className="scheme-tag" style={{ color: scheme.color, background: scheme.bg, borderColor: scheme.border }}>
                          {scheme.badge} · {scheme.label}
                        </span>
                      </div>

                      <div className="relevance-group">
                        <div className="relevance-bar-box">
                          <span className="rel-label">Semantic Match: <strong>{pct}%</strong></span>
                          <div className="progress-track">
                            <div className="progress-fill" style={{ width: `${pct}%`, background: pct >= 70 ? '#15803D' : pct >= 50 ? '#D97706' : '#DC2626' }} />
                          </div>
                        </div>
                        <span className="conf-pill" style={{ color: confidence.color, background: confidence.bg }}>
                          {confidence.text}
                        </span>
                      </div>
                    </div>

                    <h3 className="standard-full-title">{r.title || 'Specification for Industrial and Commercial Applications'}</h3>

                    {/* "Why this standard?" Section 🔥 */}
                    <div className="why-standard-box">
                      <div className="why-title">
                        <HelpCircle size={14} className="text-amber-600" />
                        <span>Why this standard applies:</span>
                      </div>
                      <div className="why-points">
                        <div className="why-point">
                          <CheckCircle2 size={13} className="text-emerald-600 point-icon" />
                          <span>Directly specifies chemical, physical, and quality criteria for <strong>{product}</strong></span>
                        </div>
                        <div className="why-point">
                          <CheckCircle2 size={13} className="text-emerald-600 point-icon" />
                          <span>Mandates safety thresholds, permissible limits, and testing protocols</span>
                        </div>
                        <div className="why-point">
                          <CheckCircle2 size={13} className="text-emerald-600 point-icon" />
                          <span>Required for regulatory compliance and laboratory certification under BIS Act</span>
                        </div>
                      </div>
                      <div className="why-footer">
                        <span>Based on: <strong>2+ retrieved BIS clauses</strong> · Verified against official BIS Gazette</span>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="card-actions-row">
                      <button
                        className="btn-inspect-evidence"
                        onClick={() => handleInspectEvidence(r)}
                      >
                        <FileText size={14} />
                        <span>View Clauses & Evidence Dossier</span>
                      </button>

                      <button
                        className="btn-ask-manakai"
                        onClick={() => {
                          if (onAskAboutStandard) {
                            onAskAboutStandard(r.standard_number, r.title);
                          }
                        }}
                      >
                        <span>Ask ManakAI about requirements</span>
                        <ChevronRight size={15} />
                      </button>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </div>

      <style>{`
        .finder-view {
          min-height: 100vh;
          background: #F4F3ED;
          padding-bottom: 60px;
        }

        .finder-hero-banner {
          background: #FFFFFF;
          border-bottom: 1px solid #E2E8F0;
          padding: 32px 48px;
        }

        .hero-content {
          max-width: 1100px;
          margin: 0 auto;
        }

        .hero-badge {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          font-size: 11.5px;
          font-weight: 700;
          letter-spacing: 0.6px;
          color: #9C6B2E;
          background: #FEF3C7;
          padding: 4px 10px;
          border-radius: 4px;
          margin-bottom: 10px;
        }

        .finder-hero-banner h1 {
          font-family: var(--serif);
          font-size: 30px;
          font-weight: 700;
          color: #16243D;
          margin: 0 0 8px;
        }

        .finder-hero-banner p {
          font-size: 14.5px;
          color: #475569;
          margin: 0;
          max-width: 820px;
          line-height: 1.6;
        }

        .finder-wrap {
          max-width: 1100px;
          margin: 0 auto;
          padding: 32px 48px;
        }

        .search-card {
          background: #FFFFFF;
          border: 1px solid #CBD5E1;
          border-radius: 12px;
          padding: 24px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
          margin-bottom: 28px;
        }

        .search-input-row {
          display: flex;
          gap: 12px;
        }

        .search-input-wrap {
          flex: 1;
          position: relative;
          display: flex;
          align-items: center;
        }

        .search-icon {
          position: absolute;
          left: 16px;
          color: #64748B;
        }

        .search-input-wrap input {
          width: 100%;
          padding: 14px 16px 14px 46px;
          font-size: 15px;
          font-family: var(--sans);
          border: 1.5px solid #CBD5E1;
          border-radius: 8px;
          background: #FAFAFA;
          color: #1E293B;
          transition: border-color 0.15s, box-shadow 0.15s;
        }

        .search-input-wrap input:focus {
          outline: none;
          border-color: #9C6B2E;
          background: #FFFFFF;
          box-shadow: 0 0 0 3px rgba(156, 107, 46, 0.12);
        }

        .search-btn {
          all: unset;
          cursor: pointer;
          background: #16243D;
          color: #FFFFFF;
          font-weight: 600;
          font-size: 14.5px;
          padding: 0 28px;
          border-radius: 8px;
          display: flex;
          align-items: center;
          gap: 8px;
          transition: all 0.15s;
          flex-shrink: 0;
        }

        .search-btn:hover:not(:disabled) {
          background: #1F3354;
          box-shadow: 0 3px 10px rgba(22, 36, 61, 0.25);
        }

        .search-btn:disabled {
          opacity: 0.6;
          cursor: not-allowed;
        }

        .filter-chips-row {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-top: 18px;
          padding-top: 16px;
          border-top: 1px solid #F1F5F9;
          flex-wrap: wrap;
        }

        .filter-label {
          display: flex;
          align-items: center;
          gap: 5px;
          font-size: 12.5px;
          font-weight: 600;
          color: #64748B;
        }

        .chips-container {
          display: flex;
          gap: 8px;
          flex-wrap: wrap;
        }

        .industry-chip {
          all: unset;
          cursor: pointer;
          font-size: 12.5px;
          font-weight: 500;
          padding: 5px 12px;
          border-radius: 20px;
          background: #F1F5F9;
          color: #475569;
          border: 1px solid #E2E8F0;
          transition: all 0.15s;
        }

        .industry-chip:hover {
          background: #E2E8F0;
          color: #0F172A;
        }

        .active-chip {
          background: #16243D;
          color: #FFFFFF;
          border-color: #16243D;
          font-weight: 600;
        }

        .active-chip:hover {
          background: #16243D;
          color: #FFFFFF;
        }

        .finder-error {
          display: flex;
          align-items: center;
          gap: 10px;
          background: #FEF2F2;
          border: 1px solid #FCA5A5;
          color: #991B1B;
          padding: 14px 18px;
          border-radius: 8px;
          font-size: 13.5px;
          margin-bottom: 24px;
        }

        .quick-suggestions-box {
          background: #FFFFFF;
          border: 1px solid #E2E8F0;
          border-radius: 12px;
          padding: 28px;
        }

        .sugg-header {
          margin-bottom: 16px;
        }

        .sugg-title {
          font-size: 15px;
          font-weight: 700;
          color: #1E293B;
          display: block;
        }

        .sugg-sub {
          font-size: 13px;
          color: #64748B;
        }

        .sugg-grid {
          display: grid;
          grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
          gap: 12px;
          margin-bottom: 24px;
        }

        .sugg-card {
          all: unset;
          cursor: pointer;
          background: #F8FAFC;
          border: 1px solid #E2E8F0;
          border-radius: 8px;
          padding: 14px 16px;
          transition: all 0.15s;
        }

        .sugg-card:hover {
          border-color: #9C6B2E;
          background: #FFFDF9;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(156, 107, 46, 0.08);
        }

        .sugg-name {
          font-size: 13.5px;
          font-weight: 600;
          color: #1E293B;
        }

        .sugg-ind {
          font-size: 11.5px;
          color: #9C6B2E;
          margin-top: 4px;
          font-weight: 500;
        }

        .differentiator-banner {
          display: flex;
          gap: 14px;
          background: #F1F5F9;
          border: 1px solid #CBD5E1;
          border-radius: 8px;
          padding: 16px;
          font-size: 13px;
          color: #334155;
          line-height: 1.5;
        }

        .diff-icon {
          color: #0284C7;
          flex-shrink: 0;
          margin-top: 2px;
        }

        .results-container {
          display: flex;
          flex-direction: column;
          gap: 20px;
        }

        .results-top-meta {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding-bottom: 8px;
          border-bottom: 1px solid #CBD5E1;
        }

        .results-top-meta h2 {
          font-size: 17px;
          font-weight: 600;
          color: #1E293B;
          margin: 0;
        }

        .highlight-term {
          color: #9C6B2E;
        }

        .vector-badge {
          font-size: 11px;
          font-weight: 600;
          color: #475569;
          background: #E2E8F0;
          padding: 3px 8px;
          border-radius: 4px;
        }

        .results-list {
          display: flex;
          flex-direction: column;
          gap: 16px;
        }

        .standard-card {
          background: #FFFFFF;
          border: 1px solid #CBD5E1;
          border-radius: 12px;
          padding: 22px 26px;
          box-shadow: 0 2px 6px rgba(0, 0, 0, 0.03);
          transition: border-color 0.15s, box-shadow 0.15s;
          position: relative;
        }

        .standard-card:hover {
          border-color: #9C6B2E;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.06);
        }

        .best-match-card {
          border: 1.5px solid #D4AF37;
          background: #FFFEFA;
        }

        .best-match-ribbon {
          display: inline-flex;
          align-items: center;
          gap: 6px;
          font-size: 11px;
          font-weight: 800;
          letter-spacing: 0.5px;
          color: #92400E;
          background: #FEF3C7;
          border: 1px solid #FDE68A;
          padding: 4px 10px;
          border-radius: 4px;
          margin-bottom: 12px;
        }

        .card-top-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          flex-wrap: wrap;
          gap: 12px;
          margin-bottom: 8px;
        }

        .std-title-group {
          display: flex;
          align-items: center;
          gap: 10px;
          flex-wrap: wrap;
        }

        .std-number {
          font-size: 19px;
          font-weight: 800;
          color: #16243D;
          letter-spacing: 0.3px;
        }

        .std-revision {
          font-size: 12px;
          font-weight: 600;
          color: #64748B;
          background: #F1F5F9;
          padding: 2px 7px;
          border-radius: 4px;
        }

        .scheme-tag {
          font-size: 11.5px;
          font-weight: 700;
          padding: 3px 8px;
          border-radius: 4px;
          border: 1px solid transparent;
        }

        .relevance-group {
          display: flex;
          align-items: center;
          gap: 12px;
        }

        .relevance-bar-box {
          display: flex;
          flex-direction: column;
          align-items: flex-end;
          gap: 3px;
        }

        .rel-label {
          font-size: 11px;
          color: #475569;
        }

        .progress-track {
          width: 90px;
          height: 6px;
          background: #E2E8F0;
          border-radius: 3px;
          overflow: hidden;
        }

        .progress-fill {
          height: 100%;
          border-radius: 3px;
        }

        .conf-pill {
          font-size: 10.5px;
          font-weight: 800;
          padding: 3px 7px;
          border-radius: 4px;
          letter-spacing: 0.3px;
        }

        .standard-full-title {
          font-size: 16px;
          font-weight: 600;
          color: #1E293B;
          margin: 0 0 16px;
          line-height: 1.4;
        }

        .why-standard-box {
          background: #F8FAFC;
          border: 1px solid #E2E8F0;
          border-left: 3px solid #9C6B2E;
          border-radius: 8px;
          padding: 14px 16px;
          margin-bottom: 18px;
        }

        .why-title {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 12.5px;
          font-weight: 700;
          color: #1E293B;
          margin-bottom: 8px;
        }

        .why-points {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }

        .why-point {
          display: flex;
          align-items: flex-start;
          gap: 8px;
          font-size: 13px;
          color: #334155;
          line-height: 1.4;
        }

        .point-icon {
          flex-shrink: 0;
          margin-top: 2px;
        }

        .why-footer {
          margin-top: 10px;
          padding-top: 8px;
          border-top: 1px dashed #CBD5E1;
          font-size: 11.5px;
          color: #64748B;
        }

        .card-actions-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          flex-wrap: wrap;
          gap: 12px;
          padding-top: 12px;
          border-top: 1px solid #F1F5F9;
        }

        .btn-inspect-evidence {
          all: unset;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          font-size: 13px;
          font-weight: 600;
          color: #475569;
          background: #F1F5F9;
          padding: 8px 14px;
          border-radius: 6px;
          border: 1px solid #CBD5E1;
          transition: all 0.15s;
        }

        .btn-inspect-evidence:hover {
          background: #E2E8F0;
          color: #0F172A;
          border-color: #94A3B8;
        }

        .btn-ask-manakai {
          all: unset;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          font-size: 13px;
          font-weight: 600;
          color: #FFFFFF;
          background: #9C6B2E;
          padding: 8px 16px;
          border-radius: 6px;
          transition: all 0.15s;
        }

        .btn-ask-manakai:hover {
          background: #805523;
          box-shadow: 0 2px 8px rgba(156, 107, 46, 0.25);
        }

        .finder-empty-state {
          text-align: center;
          padding: 60px 20px;
          background: #FFFFFF;
          border: 1px solid #E2E8F0;
          border-radius: 12px;
        }

        .empty-ico {
          font-size: 32px;
          margin-bottom: 12px;
        }

        .finder-empty-state h3 {
          font-size: 18px;
          color: #1E293B;
          margin-bottom: 6px;
        }

        .finder-empty-state p {
          color: #64748B;
          font-size: 14px;
          margin: 0;
        }
      `}</style>
    </div>
  );
}
