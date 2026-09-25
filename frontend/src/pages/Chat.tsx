import { useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import { LogOut, User as UserIcon, ChevronRight } from 'lucide-react';
import Sidebar from '../components/Sidebar';
import ChatView from '../components/ChatView';
import FinderView from '../components/FinderView';
import AdminView from '../components/AdminView';
import EvidenceDossier from '../components/EvidenceDossier';
import type { Source } from '../types';

export default function Chat() {
  const [activeView, setActiveView] = useState<'chat' | 'finder' | 'admin'>('chat');
  const [evidenceSources, setEvidenceSources] = useState<Source[]>([]);
  const [showEvidence, setShowEvidence] = useState(false);
  const [initialQuery, setInitialQuery] = useState<string>('');
  const { user, logout } = useAuth();

  const handleShowEvidence = (sources: Source[]) => {
    setEvidenceSources(sources);
    setShowEvidence(true);
  };

  const handleAskAboutStandard = (standardCode: string, standardTitle?: string) => {
    const q = standardTitle
      ? `What are the key technical requirements, testing procedures, and certification scheme under ${standardCode} (${standardTitle})?`
      : `What are the key requirements and certification procedures under ${standardCode}?`;
    setInitialQuery(q);
    setActiveView('chat');
  };

  const getViewTitle = () => {
    switch (activeView) {
      case 'chat':
        return 'Ask ManakAI';
      case 'finder':
        return 'Find Standard';
      case 'admin':
        return 'Analytics & Compliance';
      default:
        return 'Dashboard';
    }
  };

  return (
    <div className="app-shell">
      <Sidebar
        activeView={activeView}
        onViewChange={(view) => setActiveView(view as any)}
        onSelectSampleQuery={(query) => {
          setInitialQuery(query);
          setActiveView('chat');
        }}
      />

      <div className="main-content">
        {/* Institutional Top Navbar (PDF Page 1) */}
        <header className="top-nav-bar">
          <div className="breadcrumbs">
            <span className="crumb-root">MANAKAI</span>
            <ChevronRight size={13} className="crumb-sep" />
            <span className="crumb-section">Intelligence Platform</span>
            <ChevronRight size={13} className="crumb-sep" />
            <span className="crumb-current">{getViewTitle()}</span>
          </div>

          <div className="user-bar">
            <div className="user-pill">
              <div className="avatar-circle">
                <UserIcon size={13} />
              </div>
              <span className="user-name">{user?.username || 'Demo User'}</span>
              <span className="role-tag">{user?.role || 'OFFICER'}</span>
            </div>

            <button className="logout-btn" onClick={logout} title="Sign out">
              <LogOut size={15} />
              <span>Logout</span>
            </button>
          </div>
        </header>

        {/* Workspaces */}
        <main className="workspace-body">
          {activeView === 'chat' && (
            <ChatView
              onShowEvidence={handleShowEvidence}
              onNavigateToFinder={() => setActiveView('finder')}
              initialQuery={initialQuery}
              onClearInitialQuery={() => setInitialQuery('')}
            />
          )}

          {activeView === 'finder' && (
            <FinderView
              onShowEvidence={handleShowEvidence}
              onAskAboutStandard={handleAskAboutStandard}
            />
          )}

          {activeView === 'admin' && <AdminView />}
        </main>
      </div>

      {/* Slide-in Evidence Dossier Drawer (PDF Page 7-8) */}
      <EvidenceDossier
        sources={evidenceSources}
        isOpen={showEvidence}
        onClose={() => setShowEvidence(false)}
      />

      <style>{`
        .app-shell {
          display: flex;
          min-height: 100vh;
          background: #F4F3ED;
        }

        .main-content {
          flex: 1;
          margin-left: 240px;
          display: flex;
          flex-direction: column;
          min-height: 100vh;
          position: relative;
        }

        .top-nav-bar {
          background: #FFFFFF;
          border-bottom: 1px solid #E2E8F0;
          height: 52px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 40px;
          position: sticky;
          top: 0;
          z-index: 15;
        }

        .breadcrumbs {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 13px;
        }

        .crumb-root {
          font-weight: 700;
          color: #16243D;
          letter-spacing: 0.5px;
        }

        .crumb-sep {
          color: #94A3B8;
        }

        .crumb-section {
          color: #64748B;
        }

        .crumb-current {
          color: #9C6B2E;
          font-weight: 600;
        }

        .user-bar {
          display: flex;
          align-items: center;
          gap: 14px;
        }

        .user-pill {
          display: flex;
          align-items: center;
          gap: 7px;
          background: #F8FAFC;
          border: 1px solid #E2E8F0;
          padding: 4px 10px;
          border-radius: 20px;
        }

        .avatar-circle {
          width: 22px;
          height: 22px;
          border-radius: 50%;
          background: #16243D;
          color: #FFFFFF;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .user-name {
          font-size: 12.5px;
          font-weight: 600;
          color: #1E293B;
        }

        .role-tag {
          font-size: 10px;
          font-weight: 700;
          color: #9C6B2E;
          background: #FEF3C7;
          padding: 1px 6px;
          border-radius: 4px;
          letter-spacing: 0.3px;
        }

        .logout-btn {
          all: unset;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 5px;
          font-size: 12.5px;
          font-weight: 500;
          color: #64748B;
          padding: 6px 10px;
          border-radius: 6px;
          transition: all 0.15s;
        }

        .logout-btn:hover {
          background: #FEF2F2;
          color: #DC2626;
        }

        .workspace-body {
          flex: 1;
        }
      `}</style>
    </div>
  );
}
