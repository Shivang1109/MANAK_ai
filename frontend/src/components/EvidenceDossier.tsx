import { X, FileText, CheckCircle2, ExternalLink } from 'lucide-react';
import { Source } from '../types';

interface EvidenceDossierProps {
  sources: Source[];
  isOpen: boolean;
  onClose: () => void;
  selectedStandard?: string;
}

export default function EvidenceDossier({ sources, isOpen, onClose, selectedStandard }: EvidenceDossierProps) {
  if (!isOpen) return null;

  return (
    <div className="dossier-overlay" onClick={onClose}>
      <aside className="dossier" onClick={(e) => e.stopPropagation()}>
        <div className="dossier-header">
          <div>
            <div className="dossier-tag">
              <CheckCircle2 size={13} className="text-emerald-500" />
              <span>OFFICIAL EVIDENCE</span>
            </div>
            <h2 className="dossier-title">Evidence Dossier</h2>
            <p className="dossier-subtitle">
              {selectedStandard ? `Retrieved clauses for ${selectedStandard}` : 'Exact clauses and gazette extracts supporting this response.'}
            </p>
          </div>
          <button className="close-btn" onClick={onClose} aria-label="Close evidence dossier">
            <X size={18} />
          </button>
        </div>

        <div className="dossier-body">
          {sources.length === 0 ? (
            <div className="dossier-empty">
              <FileText size={32} className="empty-icon" />
              <p>No explicit clause citation attached to this item, or context was inferred from BIS general regulatory guidelines.</p>
            </div>
          ) : (
            <div className="dossier-sources">
              {sources.map((source, idx) => (
                <div key={idx} className="source-card">
                  <div className="source-top">
                    <span className="source-badge">Source [{idx + 1}]</span>
                    {source.relevanceScore !== undefined && (
                      <span className="source-relevance">
                        {Math.round(source.relevanceScore * 100)}% match
                      </span>
                    )}
                  </div>

                  <div className="source-standard-box">
                    <span className="source-standard">{source.standardNumber || 'Indian Standard'}</span>
                    {source.clause && (
                      <span className="source-clause">Clause {source.clause}</span>
                    )}
                  </div>

                  <div className="source-title">{source.title || 'Official Bureau of Indian Standards Specification'}</div>

                  {source.contentPreview && (
                    <div className="quote-box">
                      <div className="quote-label">Relevant Extracted Text</div>
                      <div className="quote-text">"{source.contentPreview}"</div>
                    </div>
                  )}

                  <div className="source-meta-row">
                    <div className="meta-item">
                      <span className="meta-key">Document:</span>
                      <span className="meta-val">{source.documentType || 'Official BIS Gazette'}</span>
                    </div>
                    {source.page && source.page > 0 && (
                      <div className="meta-item">
                        <span className="meta-key">Page:</span>
                        <span className="meta-val">Pg. {source.page}</span>
                      </div>
                    )}
                  </div>

                  <a
                    href="https://www.services.bis.gov.in/"
                    target="_blank"
                    rel="noreferrer"
                    className="view-doc-btn"
                  >
                    <span>Verify on BIS Portal</span>
                    <ExternalLink size={12} />
                  </a>
                </div>
              ))}
            </div>
          )}
        </div>

        <style>{`
          .dossier-overlay {
            position: fixed;
            inset: 0;
            background: rgba(15, 23, 42, 0.45);
            backdrop-filter: blur(3px);
            z-index: 100;
            display: flex;
            justify-content: flex-end;
            animation: fadeIn 0.15s ease-out;
          }

          @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }

          @keyframes slideIn {
            from { transform: translateX(100%); }
            to { transform: translateX(0); }
          }

          .dossier {
            background: #FFFFFF;
            border-left: 1px solid #E2E8F0;
            padding: 28px 24px;
            width: 440px;
            max-width: 90vw;
            height: 100vh;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            box-shadow: -8px 0 24px rgba(0, 0, 0, 0.12);
            animation: slideIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
          }

          .dossier-header {
            display: flex;
            align-items: flex-start;
            justify-content: space-between;
            padding-bottom: 16px;
            border-bottom: 1px solid #E2E8F0;
            margin-bottom: 20px;
          }

          .dossier-tag {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            font-size: 11px;
            font-weight: 700;
            letter-spacing: 0.5px;
            color: #065F46;
            background: #ECFDF5;
            padding: 3px 8px;
            border-radius: 4px;
            margin-bottom: 6px;
          }

          .dossier-title {
            font-family: var(--serif);
            font-size: 22px;
            font-weight: 700;
            color: #17233B;
            margin: 0 0 4px;
          }

          .dossier-subtitle {
            font-size: 13px;
            color: #64748B;
            margin: 0;
            line-height: 1.4;
          }

          .close-btn {
            all: unset;
            cursor: pointer;
            padding: 6px;
            border-radius: 6px;
            color: #64748B;
            display: flex;
            align-items: center;
            justify-content: center;
            transition: all 0.15s;
          }

          .close-btn:hover {
            background: #F1F5F9;
            color: #0F172A;
          }

          .dossier-body {
            flex: 1;
          }

          .dossier-empty {
            text-align: center;
            padding: 48px 16px;
            color: #64748B;
            font-size: 13.5px;
            line-height: 1.6;
          }

          .empty-icon {
            margin: 0 auto 12px;
            color: #94A3B8;
            opacity: 0.7;
          }

          .dossier-sources {
            display: flex;
            flex-direction: column;
            gap: 16px;
          }

          .source-card {
            background: #F8FAFC;
            border: 1px solid #E2E8F0;
            border-radius: 10px;
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 10px;
          }

          .source-top {
            display: flex;
            align-items: center;
            justify-content: space-between;
          }

          .source-badge {
            font-size: 11px;
            font-weight: 700;
            color: #475569;
            background: #E2E8F0;
            padding: 2px 7px;
            border-radius: 4px;
          }

          .source-relevance {
            font-size: 11.5px;
            font-weight: 600;
            color: #15803D;
            background: #DCFCE7;
            padding: 2px 8px;
            border-radius: 4px;
          }

          .source-standard-box {
            display: flex;
            align-items: baseline;
            gap: 8px;
            flex-wrap: wrap;
          }

          .source-standard {
            font-size: 15px;
            font-weight: 700;
            color: #16243D;
          }

          .source-clause {
            font-size: 12px;
            font-weight: 600;
            color: #9C6B2E;
            background: #FEF3C7;
            padding: 2px 8px;
            border-radius: 4px;
          }

          .source-title {
            font-size: 13.5px;
            color: #334155;
            font-weight: 500;
            line-height: 1.4;
          }

          .quote-box {
            background: #FFFFFF;
            border: 1px solid #E2E8F0;
            border-left: 3px solid #9C6B2E;
            border-radius: 6px;
            padding: 10px 12px;
          }

          .quote-label {
            font-size: 10.5px;
            text-transform: uppercase;
            font-weight: 700;
            letter-spacing: 0.4px;
            color: #94A3B8;
            margin-bottom: 4px;
          }

          .quote-text {
            font-size: 12.5px;
            font-family: var(--sans);
            color: #1E293B;
            line-height: 1.5;
            font-style: italic;
          }

          .source-meta-row {
            display: flex;
            gap: 14px;
            font-size: 12px;
            color: #64748B;
            padding-top: 4px;
          }

          .meta-key {
            color: #94A3B8;
            margin-right: 4px;
          }

          .meta-val {
            font-weight: 600;
            color: #475569;
          }

          .view-doc-btn {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 6px;
            background: #FFFFFF;
            border: 1px solid #CBD5E1;
            padding: 7px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            color: #1E293B;
            text-decoration: none;
            transition: all 0.15s;
            margin-top: 2px;
          }

          .view-doc-btn:hover {
            background: #F1F5F9;
            border-color: #94A3B8;
            color: #0F172A;
          }
        `}</style>
      </aside>
    </div>
  );
}
