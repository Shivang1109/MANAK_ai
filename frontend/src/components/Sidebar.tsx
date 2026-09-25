import { MessageSquare, Search, BarChart3, Database, CheckCircle2, Sparkles } from 'lucide-react';

interface SidebarProps {
  activeView: string;
  onViewChange: (view: string) => void;
  onSelectSampleQuery?: (query: string) => void;
}

export default function Sidebar({ activeView, onViewChange, onSelectSampleQuery }: SidebarProps) {
  const navItems = [
    { id: 'chat', label: 'Ask ManakAI', icon: MessageSquare, badge: 'RAG' },
    { id: 'finder', label: 'Find Standard', icon: Search, badge: 'Hero' },
    { id: 'admin', label: 'Analytics', icon: BarChart3, badge: 'Live' },
  ];

  const quickStandards = [
    { code: 'IS 10500', name: 'Drinking Water' },
    { code: 'IS 16102', name: 'LED Bulbs' },
    { code: 'IS 269', name: 'Cement Quality' },
    { code: 'IS 1293', name: 'Plugs & Sockets' },
  ];

  return (
    <nav className="sidebar">
      <div className="brand-section">
        <div className="wordmark">
          <Sparkles size={18} className="sparkle-icon" />
          <span>MANAK<span className="wordmark-ai">AI</span></span>
        </div>
        <div className="tagline">Evidence-First BIS Intelligence</div>
        <div className="gov-badge">Bureau of Indian Standards Assistant</div>
      </div>

      <div className="nav-group">
        <div className="group-label">WORKSPACES</div>
        <div className="nav">
          {navItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeView === item.id;
            return (
              <button
                key={item.id}
                className={`nav-btn ${isActive ? 'active' : ''}`}
                onClick={() => onViewChange(item.id)}
              >
                <div className="btn-left">
                  <Icon className="nav-icon" size={16} strokeWidth={isActive ? 2.2 : 1.8} />
                  <span className="btn-text">{item.label}</span>
                </div>
                {item.badge && (
                  <span className={`pill-badge ${isActive ? 'active-pill' : ''}`}>
                    {item.badge}
                  </span>
                )}
              </button>
            );
          })}
        </div>
      </div>

      <div className="nav-group">
        <div className="group-label">KNOWLEDGE BASE</div>
        <div className="kb-stats-card">
          <div className="kb-stat-row">
            <Database size={13} className="text-amber-400" />
            <span className="kb-title">15 Standards</span>
          </div>
          <div className="kb-detail">4,047 indexed chunks with clause-level embeddings</div>
        </div>

        <div className="quick-list">
          {quickStandards.map((std) => (
            <button
              key={std.code}
              className="quick-item"
              onClick={() => {
                onViewChange('chat');
                if (onSelectSampleQuery) {
                  onSelectSampleQuery(`What are the key requirements under ${std.code} for ${std.name}?`);
                }
              }}
            >
              <span className="quick-code">{std.code}</span>
              <span className="quick-name">{std.name}</span>
            </button>
          ))}
        </div>
      </div>

      <div className="rail-foot">
        <div className="foot-status">
          <CheckCircle2 size={13} className="foot-check" />
          <span className="foot-title">Evidence-Grounded</span>
        </div>
        <p className="foot-desc">
          Answers strictly reference official BIS gazettes, specifications, and clause indices.
        </p>
      </div>

      <style>{`
        .sidebar {
          background: #141E33;
          color: #E2E8F0;
          padding: 24px 16px;
          display: flex;
          flex-direction: column;
          gap: 20px;
          width: 240px;
          height: 100vh;
          position: fixed;
          left: 0;
          top: 0;
          border-right: 1px solid rgba(255, 255, 255, 0.08);
          z-index: 20;
          overflow-y: auto;
        }

        .brand-section {
          padding-bottom: 12px;
          border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        }

        .wordmark {
          display: flex;
          align-items: center;
          gap: 8px;
          font-family: var(--serif);
          font-size: 21px;
          font-weight: 700;
          letter-spacing: 0.5px;
          color: #F8FAFC;
        }

        .sparkle-icon {
          color: #D4AF37;
        }

        .wordmark-ai {
          color: #D4AF37;
          margin-left: 1px;
        }

        .tagline {
          font-size: 12px;
          font-weight: 500;
          color: #94A3B8;
          margin-top: 3px;
          letter-spacing: 0.2px;
        }

        .gov-badge {
          display: inline-block;
          font-size: 10px;
          font-weight: 600;
          color: #CBD5E1;
          background: rgba(255, 255, 255, 0.06);
          padding: 3px 6px;
          border-radius: 4px;
          margin-top: 8px;
          border: 1px solid rgba(255, 255, 255, 0.08);
        }

        .nav-group {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .group-label {
          font-size: 10.5px;
          font-weight: 700;
          letter-spacing: 0.8px;
          color: #64748B;
          padding-left: 6px;
        }

        .nav {
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .nav-btn {
          all: unset;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 9px 12px;
          border-radius: 8px;
          font-size: 13.5px;
          font-weight: 500;
          color: #CBD5E1;
          cursor: pointer;
          transition: all 0.15s ease;
        }

        .btn-left {
          display: flex;
          align-items: center;
          gap: 10px;
        }

        .nav-icon {
          opacity: 0.75;
          flex: 0 0 auto;
        }

        .nav-btn:hover {
          background: rgba(255, 255, 255, 0.07);
          color: #FFFFFF;
        }

        .nav-btn.active {
          background: rgba(212, 175, 55, 0.16);
          color: #F8FAFC;
          font-weight: 600;
          border: 1px solid rgba(212, 175, 55, 0.28);
        }

        .nav-btn.active .nav-icon {
          opacity: 1;
          color: #D4AF37;
        }

        .pill-badge {
          font-size: 10.5px;
          font-weight: 600;
          color: #94A3B8;
          background: rgba(255, 255, 255, 0.06);
          padding: 2px 6px;
          border-radius: 4px;
        }

        .active-pill {
          background: rgba(212, 175, 55, 0.25);
          color: #FDE047;
        }

        .kb-stats-card {
          background: rgba(255, 255, 255, 0.04);
          border: 1px solid rgba(255, 255, 255, 0.08);
          border-radius: 8px;
          padding: 10px 12px;
        }

        .kb-stat-row {
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .kb-title {
          font-size: 12.5px;
          font-weight: 600;
          color: #E2E8F0;
        }

        .kb-detail {
          font-size: 11px;
          color: #94A3B8;
          margin-top: 4px;
          line-height: 1.4;
        }

        .quick-list {
          display: flex;
          flex-direction: column;
          gap: 3px;
          margin-top: 4px;
        }

        .quick-item {
          all: unset;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 6px 8px;
          border-radius: 6px;
          cursor: pointer;
          font-size: 12px;
          transition: background 0.15s;
        }

        .quick-item:hover {
          background: rgba(255, 255, 255, 0.06);
        }

        .quick-code {
          font-weight: 600;
          color: #D4AF37;
        }

        .quick-name {
          color: #94A3B8;
          font-size: 11.5px;
        }

        .rail-foot {
          margin-top: auto;
          background: rgba(16, 185, 129, 0.08);
          border: 1px solid rgba(16, 185, 129, 0.2);
          border-radius: 8px;
          padding: 12px;
        }

        .foot-status {
          display: flex;
          align-items: center;
          gap: 6px;
          color: #34D399;
          font-weight: 600;
          font-size: 11.5px;
        }

        .foot-check {
          flex-shrink: 0;
        }

        .foot-desc {
          font-size: 11px;
          color: #94A3B8;
          line-height: 1.4;
          margin-top: 4px;
        }
      `}</style>
    </nav>
  );
}
