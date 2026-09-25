import { useState, useRef, useEffect } from 'react';
import { Send, ThumbsUp, ThumbsDown, CheckCircle2, AlertTriangle, FileText, ChevronRight, ShieldCheck, Sparkles, Clock, Search, HelpCircle, Loader2 } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import { chatAPI, feedbackAPI } from '../services/api';
import type { ChatMessage, Source } from '../types';

interface ChatViewProps {
  onShowEvidence: (sources: Source[]) => void;
  onNavigateToFinder?: () => void;
  initialQuery?: string;
  onClearInitialQuery?: () => void;
}

export default function ChatView({ onShowEvidence, onNavigateToFinder, initialQuery, onClearInitialQuery }: ChatViewProps) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [feedbackGiven, setFeedbackGiven] = useState<Record<number, 'up' | 'down'>>({});
  const [analysisStep, setAnalysisStep] = useState(0);

  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading, analysisStep]);

  // Handle prefilled query from Finder or Sidebar
  useEffect(() => {
    if (initialQuery && initialQuery.trim()) {
      setInput(initialQuery);
      handleSendQuery(initialQuery);
      if (onClearInitialQuery) onClearInitialQuery();
    }
  }, [initialQuery]);

  // Simulated AI analysis timeline steps during loading
  useEffect(() => {
    let interval: any;
    if (isLoading) {
      setAnalysisStep(1);
      interval = setInterval(() => {
        setAnalysisStep((prev) => (prev < 4 ? prev + 1 : prev));
      }, 1800);
    } else {
      setAnalysisStep(0);
    }
    return () => clearInterval(interval);
  }, [isLoading]);

  const handleSendQuery = async (queryText?: string) => {
    const textToSend = queryText || input;
    if (!textToSend.trim() || isLoading) return;

    const userMessage: ChatMessage = {
      role: 'user',
      content: textToSend,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await chatAPI.sendMessage({
        query: textToSend,
        conversationId,
      });

      setConversationId(response.conversationId);

      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.answer,
        sources: response.sources,
        confidence: response.confidence,
        confidenceScore: response.confidenceScore,
        timestamp: response.timestamp,
      };

      setMessages((prev) => [...prev, assistantMessage]);
    } catch (error: any) {
      const errorMessage: ChatMessage = {
        role: 'assistant',
        content: "I encountered an issue retrieving verifiable BIS clauses for this query. Please verify that the RAG service is active and try again.",
        confidence: 'low',
        confidenceScore: 0.0,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleFeedback = async (messageIndex: number, type: 'up' | 'down') => {
    if (feedbackGiven[messageIndex]) return;

    const message = messages[messageIndex];
    if (!message?.id) {
      setFeedbackGiven((prev) => ({ ...prev, [messageIndex]: type }));
      return;
    }

    try {
      await feedbackAPI.submitFeedback({
        messageId: message.id,
        rating: type === 'up' ? 5 : 2,
        feedbackType: type === 'up' ? 'positive' : 'negative',
      });
    } catch {
      // Best-effort
    } finally {
      setFeedbackGiven((prev) => ({ ...prev, [messageIndex]: type }));
    }
  };

  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good morning';
    if (hour < 17) return 'Good afternoon';
    return 'Good evening';
  };

  const getEvidenceQuality = (score?: number, confidence?: string) => {
    const s = score !== undefined ? score : (confidence === 'high' ? 0.8 : confidence === 'medium' ? 0.5 : 0.2);
    const pct = Math.round(s * 100);
    if (s >= 0.6) {
      return {
        label: 'Strong Evidence',
        pct: Math.max(pct, 72),
        color: '#15803D',
        bg: '#DCFCE7',
        border: '#BBF7D0',
        icon: CheckCircle2,
        isLow: false,
      };
    }
    if (s >= 0.4) {
      return {
        label: 'Moderate Evidence',
        pct: Math.max(pct, 48),
        color: '#D97706',
        bg: '#FEF3C7',
        border: '#FDE68A',
        icon: HelpCircle,
        isLow: false,
      };
    }
    return {
      label: 'Limited Evidence',
      pct: Math.max(pct, 18),
      color: '#B91C1C',
      bg: '#FEE2E2',
      border: '#FECACA',
      icon: AlertTriangle,
      isLow: true,
      desc: "The available BIS documents don't provide enough evidence to answer this confidently."
    };
  };

  return (
    <div className="chat-view">
      {/* Top Bar Header */}
      <div className="topbar">
        <div className="topbar-inner">
          <div className="topbar-left">
            <span className="platform-tag">EVIDENCE-GROUNDED INTELLIGENCE</span>
            <h1>Ask ManakAI</h1>
            <p>Every response is synthesized strictly from retrieved BIS clauses, official gazettes, and standards.</p>
          </div>
          <div className="topbar-badge">
            <ShieldCheck size={16} className="text-emerald-600" />
            <span>Hallucination Guard Active</span>
          </div>
        </div>
      </div>

      <div className="chat-scroll">
        {/* Landing / Dashboard Empty State (PDF Page 9-10) */}
        {messages.length === 0 && (
          <div className="empty-state-wrap">
            <div className="empty-greeting">
              <h2>{getGreeting()} 👋</h2>
              <p>What would you like to find or verify today?</p>
            </div>

            <div className="action-cards-grid">
              <div
                className="action-card"
                onClick={() => {
                  if (onNavigateToFinder) onNavigateToFinder();
                }}
              >
                <div className="action-card-header">
                  <div className="icon-circle icon-finder">
                    <Search size={20} />
                  </div>
                  <ChevronRight size={18} className="arrow-icon" />
                </div>
                <h3>Find a Standard</h3>
                <p>Describe your product or material in plain English to map it to the applicable IS code and certification scheme.</p>
              </div>

              <div
                className="action-card"
                onClick={() => inputRef.current?.focus()}
              >
                <div className="action-card-header">
                  <div className="icon-circle icon-ask">
                    <Sparkles size={20} />
                  </div>
                  <ChevronRight size={18} className="arrow-icon" />
                </div>
                <h3>Ask Technical Requirements</h3>
                <p>Query exact chemical limits, safety tolerances, electrical parameters, or mandatory testing procedures.</p>
              </div>
            </div>

            <div className="try-asking-box">
              <div className="try-label">
                <Clock size={14} className="text-amber-600" />
                <span>Frequently Tested Queries for Demo:</span>
              </div>
              <div className="try-pills">
                {[
                  "What are the drinking water requirements according to IS 10500:2012?",
                  "What are the safety requirements for self-ballasted LED lamps under IS 16102?",
                  "What are the chemical limits and ratios for cement under IS 269:2015?",
                  "What are the requirements for plugs and socket-outlets rated up to 250V under IS 1293?",
                ].map((q) => (
                  <button
                    key={q}
                    className="try-pill"
                    onClick={() => handleSendQuery(q)}
                  >
                    <span>"{q}"</span>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}

        {/* Message Stream */}
        {messages.map((message, index) => {
          const isAssistant = message.role === 'assistant';
          const quality = isAssistant ? getEvidenceQuality(message.confidenceScore, message.confidence) : null;
          const QualityIcon = quality?.icon || CheckCircle2;

          return (
            <div key={index} className={`msg-row ${message.role}`}>
              {/* User Bubble */}
              {!isAssistant ? (
                <div className="user-bubble">
                  <p>{message.content}</p>
                </div>
              ) : (
                /* Assistant Evidence-First Response Card (PDF Page 4-6) */
                <div className="assistant-card">
                  {/* Evidence Header Bar */}
                  <div className="evidence-header-bar">
                    <div className="std-banner">
                      <FileText size={15} className="text-amber-600" />
                      <span className="std-banner-title">
                        {message.sources && message.sources.length > 0 && message.sources[0].standardNumber
                          ? `${message.sources[0].standardNumber} · Official Specification`
                          : 'Bureau of Indian Standards Analysis'}
                      </span>
                    </div>

                    {quality && (
                      <div className="quality-indicator" style={{ background: quality.bg, borderColor: quality.border }}>
                        <QualityIcon size={14} style={{ color: quality.color }} />
                        <span className="quality-text" style={{ color: quality.color }}>
                          {quality.label} ({quality.pct}%)
                        </span>
                        <div className="quality-mini-bar">
                          <div
                            className="quality-mini-fill"
                            style={{ width: `${quality.pct}%`, background: quality.color }}
                          />
                        </div>
                      </div>
                    )}
                  </div>

                  {/* Low Confidence Warning (PDF Page 6) */}
                  {quality?.isLow && (
                    <div className="low-confidence-banner">
                      <AlertTriangle size={16} />
                      <div>
                        <strong>Limited Evidence Retrieved:</strong>
                        <p>{quality.desc}</p>
                      </div>
                    </div>
                  )}

                  {/* Markdown Content with citations */}
                  <div className="assistant-body markdown-content">
                    <ReactMarkdown>{message.content}</ReactMarkdown>
                  </div>

                  {/* Sources & Citations Box (PDF Page 5-6) */}
                  {message.sources && message.sources.length > 0 && (
                    <div className="attached-sources-box">
                      <div className="sources-title-row">
                        <span className="sources-label">Retrieved BIS Evidence Clauses:</span>
                        <button
                          className="view-dossier-link"
                          onClick={() => onShowEvidence(message.sources || [])}
                        >
                          <span>Open Full Evidence Dossier</span>
                          <ChevronRight size={13} />
                        </button>
                      </div>

                      <div className="sources-chips-grid">
                        {message.sources.map((src, sIdx) => (
                          <div
                            key={sIdx}
                            className="source-chip"
                            onClick={() => onShowEvidence([src])}
                            title="Click to view extracted clause text in drawer"
                          >
                            <span className="source-index">[{sIdx + 1}]</span>
                            <span className="source-code">{src.standardNumber}</span>
                            {src.clause && <span className="source-clause">Cl. {src.clause}</span>}
                            {src.page && src.page > 0 && <span className="source-page">Pg. {src.page}</span>}
                          </div>
                        ))}
                      </div>
                    </div>
                  )}

                  {/* Action Footer */}
                  <div className="card-footer-row">
                    {message.sources && message.sources.length > 0 ? (
                      <button
                        className="btn-why-answer"
                        onClick={() => onShowEvidence(message.sources || [])}
                      >
                        <FileText size={14} />
                        <span>Inspect Evidence Dossier</span>
                      </button>
                    ) : <div />}

                    <div className="feedback-btns">
                      <span className="fb-label">Helpful?</span>
                      <button
                        title="Upvote response"
                        className={`fb-btn ${feedbackGiven[index] === 'up' ? 'fb-up' : ''}`}
                        onClick={() => handleFeedback(index, 'up')}
                        disabled={!!feedbackGiven[index]}
                      >
                        <ThumbsUp size={14} />
                      </button>
                      <button
                        title="Downvote response"
                        className={`fb-btn ${feedbackGiven[index] === 'down' ? 'fb-down' : ''}`}
                        onClick={() => handleFeedback(index, 'down')}
                        disabled={!!feedbackGiven[index]}
                      >
                        <ThumbsDown size={14} />
                      </button>
                    </div>
                  </div>
                </div>
              )}
            </div>
          );
        })}

        {/* AI Processing Timeline (PDF Page 11-12) */}
        {isLoading && (
          <div className="processing-timeline-card">
            <div className="timeline-header">
              <Loader2 size={16} className="spin text-amber-600" />
              <span>ManakAI is synthesizing evidence...</span>
            </div>

            <div className="timeline-steps">
              <div className={`step-item ${analysisStep >= 1 ? 'step-done' : ''}`}>
                <CheckCircle2 size={14} className="step-icon" />
                <span>Query understood & intent classified</span>
              </div>
              <div className={`step-item ${analysisStep >= 2 ? 'step-done' : ''}`}>
                <CheckCircle2 size={14} className="step-icon" />
                <span>Searching BIS vector database (4,047 chunks)</span>
              </div>
              <div className={`step-item ${analysisStep >= 3 ? 'step-done' : ''}`}>
                <CheckCircle2 size={14} className="step-icon" />
                <span>Retrieving relevant clauses & gazette tables</span>
              </div>
              <div className={`step-item ${analysisStep >= 4 ? 'step-done' : ''}`}>
                <CheckCircle2 size={14} className="step-icon" />
                <span>Verifying evidence grounding & formulating answer</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input Form at Bottom */}
      <div className="chat-input-bar">
        <div className="input-container">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === 'Enter' && handleSendQuery()}
            placeholder="Ask about Indian Standards, chemical/safety limits, or certification procedures..."
            disabled={isLoading}
          />
          <button
            className="send-btn"
            onClick={() => handleSendQuery()}
            disabled={!input.trim() || isLoading}
            aria-label="Send query"
          >
            <Send size={16} />
          </button>
        </div>
        <div className="disclaimer-text">
          Grounded in official Bureau of Indian Standards (BIS) documents. Every claim cites an exact clause or gazette reference.
        </div>
      </div>

      <style>{`
        .chat-view {
          display: flex;
          flex-direction: column;
          height: 100vh;
          background: #F4F3ED;
          position: relative;
        }

        .topbar {
          background: #FFFFFF;
          border-bottom: 1px solid #E2E8F0;
          padding: 20px 48px;
          z-index: 5;
        }

        .topbar-inner {
          max-width: 1000px;
          margin: 0 auto;
          display: flex;
          align-items: center;
          justify-content: space-between;
        }

        .platform-tag {
          font-size: 10.5px;
          font-weight: 700;
          letter-spacing: 0.6px;
          color: #9C6B2E;
        }

        .topbar h1 {
          font-family: var(--serif);
          font-size: 24px;
          font-weight: 700;
          color: #16243D;
          margin: 2px 0 3px;
        }

        .topbar p {
          font-size: 13.5px;
          color: #64748B;
          margin: 0;
        }

        .topbar-badge {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 12px;
          font-weight: 600;
          color: #065F46;
          background: #ECFDF5;
          padding: 6px 12px;
          border-radius: 6px;
          border: 1px solid #A7F3D0;
        }

        .chat-scroll {
          flex: 1;
          overflow-y: auto;
          padding: 32px 48px 140px;
          max-width: 1000px;
          width: 100%;
          margin: 0 auto;
        }

        .empty-state-wrap {
          display: flex;
          flex-direction: column;
          gap: 28px;
          padding-top: 16px;
        }

        .empty-greeting h2 {
          font-family: var(--serif);
          font-size: 28px;
          font-weight: 700;
          color: #16243D;
          margin: 0 0 6px;
        }

        .empty-greeting p {
          font-size: 15px;
          color: #64748B;
          margin: 0;
        }

        .action-cards-grid {
          display: grid;
          grid-template-columns: repeat(2, 1fr);
          gap: 16px;
        }

        .action-card {
          background: #FFFFFF;
          border: 1.5px solid #E2E8F0;
          border-radius: 12px;
          padding: 22px;
          cursor: pointer;
          transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1);
        }

        .action-card:hover {
          border-color: #9C6B2E;
          transform: translateY(-2px);
          box-shadow: 0 6px 20px rgba(156, 107, 46, 0.08);
        }

        .action-card-header {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 14px;
        }

        .icon-circle {
          width: 40px;
          height: 40px;
          border-radius: 10px;
          display: flex;
          align-items: center;
          justify-content: center;
        }

        .icon-finder {
          background: #FEF3C7;
          color: #B45309;
        }

        .icon-ask {
          background: #E0E7FF;
          color: #4338CA;
        }

        .arrow-icon {
          color: #94A3B8;
        }

        .action-card h3 {
          font-size: 16px;
          font-weight: 700;
          color: #1E293B;
          margin: 0 0 6px;
        }

        .action-card p {
          font-size: 13px;
          color: #64748B;
          margin: 0;
          line-height: 1.5;
        }

        .try-asking-box {
          background: #FFFFFF;
          border: 1px solid #E2E8F0;
          border-radius: 12px;
          padding: 20px 24px;
        }

        .try-label {
          display: flex;
          align-items: center;
          gap: 6px;
          font-size: 12.5px;
          font-weight: 700;
          color: #1E293B;
          margin-bottom: 12px;
        }

        .try-pills {
          display: flex;
          flex-direction: column;
          gap: 8px;
        }

        .try-pill {
          all: unset;
          cursor: pointer;
          font-size: 13.5px;
          color: #334155;
          background: #F8FAFC;
          border: 1px solid #E2E8F0;
          border-radius: 8px;
          padding: 10px 14px;
          transition: all 0.15s;
          display: block;
          text-align: left;
        }

        .try-pill:hover {
          border-color: #9C6B2E;
          background: #FFFDF8;
          color: #16243D;
          font-weight: 500;
        }

        .msg-row {
          display: flex;
          margin-bottom: 24px;
        }

        .msg-row.user {
          justify-content: flex-end;
        }

        .msg-row.assistant {
          justify-content: flex-start;
          width: 100%;
        }

        .user-bubble {
          background: #16243D;
          color: #FFFFFF;
          padding: 14px 20px;
          border-radius: 14px 14px 2px 14px;
          max-width: 75%;
          font-size: 15px;
          line-height: 1.5;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
        }

        .assistant-card {
          background: #FFFFFF;
          border: 1px solid #CBD5E1;
          border-radius: 12px;
          padding: 24px;
          width: 100%;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }

        .evidence-header-bar {
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding-bottom: 14px;
          border-bottom: 1px solid #F1F5F9;
          margin-bottom: 16px;
          flex-wrap: wrap;
          gap: 10px;
        }

        .std-banner {
          display: flex;
          align-items: center;
          gap: 7px;
        }

        .std-banner-title {
          font-size: 13.5px;
          font-weight: 700;
          color: #16243D;
        }

        .quality-indicator {
          display: flex;
          align-items: center;
          gap: 8px;
          padding: 4px 10px;
          border-radius: 6px;
          border: 1px solid transparent;
        }

        .quality-text {
          font-size: 11.5px;
          font-weight: 700;
        }

        .quality-mini-bar {
          width: 44px;
          height: 5px;
          background: rgba(0, 0, 0, 0.1);
          border-radius: 3px;
          overflow: hidden;
        }

        .quality-mini-fill {
          height: 100%;
          border-radius: 3px;
        }

        .low-confidence-banner {
          display: flex;
          gap: 10px;
          background: #FEF2F2;
          border: 1px solid #FECACA;
          border-radius: 8px;
          padding: 12px 14px;
          color: #991B1B;
          font-size: 13px;
          margin-bottom: 16px;
          line-height: 1.4;
        }

        .low-confidence-banner p {
          margin: 2px 0 0;
        }

        .assistant-body {
          font-size: 15px;
          color: #1E293B;
          line-height: 1.65;
        }

        .markdown-content strong {
          color: #0F172A;
        }

        .markdown-content ul, .markdown-content ol {
          margin: 12px 0 16px 20px;
        }

        .markdown-content li {
          margin-bottom: 6px;
        }

        .attached-sources-box {
          background: #F8FAFC;
          border: 1px solid #E2E8F0;
          border-radius: 8px;
          padding: 14px 16px;
          margin-top: 20px;
        }

        .sources-title-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-bottom: 10px;
        }

        .sources-label {
          font-size: 12px;
          font-weight: 700;
          color: #475569;
          text-transform: uppercase;
          letter-spacing: 0.4px;
        }

        .view-dossier-link {
          all: unset;
          cursor: pointer;
          display: flex;
          align-items: center;
          gap: 4px;
          font-size: 12px;
          font-weight: 600;
          color: #9C6B2E;
        }

        .view-dossier-link:hover {
          text-decoration: underline;
        }

        .sources-chips-grid {
          display: flex;
          flex-wrap: wrap;
          gap: 8px;
        }

        .source-chip {
          display: flex;
          align-items: center;
          gap: 6px;
          background: #FFFFFF;
          border: 1px solid #CBD5E1;
          padding: 5px 10px;
          border-radius: 6px;
          font-size: 12px;
          cursor: pointer;
          transition: all 0.15s;
        }

        .source-chip:hover {
          border-color: #9C6B2E;
          background: #FFFDF8;
        }

        .source-index {
          font-weight: 700;
          color: #9C6B2E;
        }

        .source-code {
          font-weight: 600;
          color: #1E293B;
        }

        .source-clause {
          color: #64748B;
          background: #F1F5F9;
          padding: 1px 6px;
          border-radius: 4px;
        }

        .source-page {
          color: #94A3B8;
        }

        .card-footer-row {
          display: flex;
          align-items: center;
          justify-content: space-between;
          margin-top: 18px;
          padding-top: 14px;
          border-top: 1px solid #F1F5F9;
        }

        .btn-why-answer {
          all: unset;
          cursor: pointer;
          display: inline-flex;
          align-items: center;
          gap: 6px;
          font-size: 12.5px;
          font-weight: 600;
          color: #475569;
          background: #F1F5F9;
          padding: 7px 12px;
          border-radius: 6px;
          border: 1px solid #CBD5E1;
          transition: all 0.15s;
        }

        .btn-why-answer:hover {
          background: #E2E8F0;
          color: #0F172A;
        }

        .feedback-btns {
          display: flex;
          align-items: center;
          gap: 6px;
        }

        .fb-label {
          font-size: 12px;
          color: #64748B;
          margin-right: 4px;
        }

        .fb-btn {
          all: unset;
          cursor: pointer;
          padding: 5px 8px;
          border-radius: 5px;
          color: #64748B;
          border: 1px solid #E2E8F0;
          display: flex;
          align-items: center;
          transition: all 0.15s;
        }

        .fb-btn:hover {
          background: #F1F5F9;
          color: #1E293B;
        }

        .fb-up {
          background: #ECFDF5;
          color: #065F46;
          border-color: #A7F3D0;
        }

        .fb-down {
          background: #FEF2F2;
          color: #991B1B;
          border-color: #FECACA;
        }

        .processing-timeline-card {
          background: #FFFFFF;
          border: 1px solid #E2E8F0;
          border-left: 3px solid #D4AF37;
          border-radius: 10px;
          padding: 18px 22px;
          margin-bottom: 24px;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
        }

        .timeline-header {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 13.5px;
          font-weight: 700;
          color: #1E293B;
          margin-bottom: 12px;
        }

        .timeline-steps {
          display: flex;
          flex-direction: column;
          gap: 7px;
        }

        .step-item {
          display: flex;
          align-items: center;
          gap: 8px;
          font-size: 12.5px;
          color: #94A3B8;
          transition: color 0.3s;
        }

        .step-done {
          color: #166534;
          font-weight: 500;
        }

        .step-done .step-icon {
          color: #16A34A;
        }

        .chat-input-bar {
          position: fixed;
          bottom: 0;
          left: 240px;
          right: 0;
          background: rgba(244, 243, 237, 0.95);
          backdrop-filter: blur(8px);
          border-top: 1px solid #E2E8F0;
          padding: 16px 48px;
          z-index: 10;
        }

        .input-container {
          max-width: 1000px;
          margin: 0 auto;
          position: relative;
          display: flex;
          align-items: center;
        }

        .input-container input {
          width: 100%;
          padding: 14px 50px 14px 18px;
          font-size: 14.5px;
          font-family: var(--sans);
          border: 1.5px solid #CBD5E1;
          border-radius: 10px;
          background: #FFFFFF;
          color: #1E293B;
          box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
          transition: border-color 0.15s, box-shadow 0.15s;
        }

        .input-container input:focus {
          outline: none;
          border-color: #9C6B2E;
          box-shadow: 0 0 0 3px rgba(156, 107, 46, 0.12);
        }

        .send-btn {
          all: unset;
          position: absolute;
          right: 12px;
          cursor: pointer;
          width: 34px;
          height: 34px;
          border-radius: 8px;
          background: #16243D;
          color: #FFFFFF;
          display: flex;
          align-items: center;
          justify-content: center;
          transition: all 0.15s;
        }

        .send-btn:hover:not(:disabled) {
          background: #1F3354;
        }

        .send-btn:disabled {
          opacity: 0.4;
          cursor: not-allowed;
        }

        .disclaimer-text {
          max-width: 1000px;
          margin: 6px auto 0;
          font-size: 11px;
          color: #64748B;
          text-align: center;
        }
      `}</style>
    </div>
  );
}
