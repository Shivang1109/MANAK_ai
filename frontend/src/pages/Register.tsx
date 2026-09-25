import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';
import { Eye, EyeOff, CheckCircle2, ArrowRight, ShieldCheck, Sparkles, BookOpen } from 'lucide-react';

export default function Register() {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const { register } = useAuth();
  const navigate = useNavigate();

  // Password strength calculation
  const getPasswordStrength = (pass: string) => {
    if (!pass) return { score: 0, label: '', color: '#CBD5E1', pct: 0 };
    let score = 0;
    if (pass.length >= 6) score += 1;
    if (pass.length >= 10) score += 1;
    if (/[A-Z]/.test(pass)) score += 1;
    if (/[0-9]/.test(pass)) score += 1;
    if (/[^A-Za-z0-9]/.test(pass)) score += 1;

    if (score <= 1) return { score: 1, label: 'Weak', color: '#EF4444', pct: 25 };
    if (score <= 2) return { score: 2, label: 'Fair', color: '#F59E0B', pct: 50 };
    if (score <= 3) return { score: 3, label: 'Good', color: '#3B82F6', pct: 75 };
    return { score: 4, label: 'Strong', color: '#10B981', pct: 100 };
  };

  const strength = getPasswordStrength(password);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');

    if (password !== confirmPassword) {
      setError('Passwords do not match');
      return;
    }

    if (password.length < 6) {
      setError('Password must be at least 6 characters');
      return;
    }

    setIsLoading(true);

    try {
      await register({ username, email, password });
      navigate('/chat');
    } catch (err: any) {
      setError(err.response?.data?.error || 'Registration failed. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="auth-split-layout">
      {/* Left Panel: Introduction to ManakAI & Value Proposition */}
      <div className="auth-intro-panel">
        <div className="intro-content">
          <div className="brand-header">
            <div className="brand-wordmark">
              <Sparkles size={20} className="gold-accent" />
              <span>MANAK<span className="gold-text">AI</span></span>
            </div>
            <span className="gov-sub-badge">Bureau of Indian Standards Assistant</span>
          </div>

          <div className="hero-text-block">
            <h1>Evidence-first BIS intelligence</h1>
            <p className="hero-subtext">
              Trusted answers. Traceable evidence. Official BIS sources.
            </p>
          </div>

          {/* USP Value Checklist (PDF Page 2) */}
          <div className="usp-checklist">
            <div className="usp-item">
              <CheckCircle2 size={18} className="gold-check" />
              <span>Secure account</span>
            </div>
            <div className="usp-item">
              <CheckCircle2 size={18} className="gold-check" />
              <span>BIS knowledge access</span>
            </div>
            <div className="usp-item">
              <CheckCircle2 size={18} className="gold-check" />
              <span>Traceable answers</span>
            </div>
          </div>

          {/* Process Flow Badge */}
          <div className="process-flow-card">
            <div className="flow-step">
              <BookOpen size={14} className="gold-text" />
              <span>Standards</span>
            </div>
            <ArrowRight size={14} className="flow-arrow" />
            <div className="flow-step">
              <ShieldCheck size={14} className="gold-text" />
              <span>Evidence</span>
            </div>
            <ArrowRight size={14} className="flow-arrow" />
            <div className="flow-step">
              <Sparkles size={14} className="gold-text" />
              <span>Decision support</span>
            </div>
          </div>

          {/* Bottom Authority Footer */}
          <div className="intro-footer">
            <div className="footer-line-1">Powered by official BIS knowledge sources</div>
            <div className="footer-line-2">Standards · Certification · Compliance</div>
            <div className="footer-version">ManakAI v1.0 · Evidence-first BIS Intelligence</div>
          </div>
        </div>
      </div>

      {/* Right Panel: Clean Register Form */}
      <div className="auth-form-panel">
        <div className="form-card-wrapper">
          <div className="auth-card">
            {/* Top Subtle Monogram */}
            <div className="card-top-row">
              <div className="small-monogram">
                <span className="mono-bracket">[</span>
                <ArrowRight size={14} className="mono-arrow" />
                <span className="mono-bracket">]</span>
              </div>
            </div>

            <div className="auth-header">
              <h2>Create your ManakAI account</h2>
              <p>Access evidence-grounded BIS standards intelligence</p>
            </div>

            {error && (
              <div className="auth-error-banner">
                {error}
              </div>
            )}

            <form onSubmit={handleSubmit} className="auth-form">
              <div className="form-field">
                <label htmlFor="reg-username">Username</label>
                <input
                  id="reg-username"
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Choose a username"
                  autoComplete="username"
                  required
                />
              </div>

              <div className="form-field">
                <label htmlFor="reg-email">Email</label>
                <input
                  id="reg-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="your.email@example.com"
                  autoComplete="email"
                  required
                />
              </div>

              <div className="form-field">
                <div className="field-label-row">
                  <label htmlFor="reg-password">Password</label>
                  <button
                    type="button"
                    className="toggle-pw-btn"
                    onClick={() => setShowPassword(!showPassword)}
                    tabIndex={-1}
                    aria-label={showPassword ? 'Hide password' : 'Show password'}
                  >
                    {showPassword ? <EyeOff size={15} /> : <Eye size={15} />}
                  </button>
                </div>
                <div className="password-input-wrap">
                  <input
                    id="reg-password"
                    type={showPassword ? 'text' : 'password'}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    placeholder="At least 6 characters"
                    autoComplete="new-password"
                    required
                  />
                </div>

                {/* Password Strength Indicator (PDF Page 2) */}
                {password.length > 0 && (
                  <div className="password-strength-box">
                    <div className="strength-header">
                      <span>Password strength:</span>
                      <span className="strength-label" style={{ color: strength.color }}>
                        {strength.label}
                      </span>
                    </div>
                    <div className="strength-bar-track">
                      <div
                        className="strength-bar-fill"
                        style={{ width: `${strength.pct}%`, background: strength.color }}
                      />
                    </div>
                  </div>
                )}
              </div>

              <div className="form-field">
                <label htmlFor="reg-confirm">Confirm Password</label>
                <input
                  id="reg-confirm"
                  type={showPassword ? 'text' : 'password'}
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  placeholder="Confirm your password"
                  autoComplete="new-password"
                  required
                />
              </div>

              <button type="submit" disabled={isLoading} className="auth-submit-btn">
                {isLoading ? 'Creating Account...' : 'Create Account'}
              </button>
            </form>

            <div className="auth-footer-nav">
              <span>Already have an account?</span>{' '}
              <Link to="/login" className="auth-link">
                Sign in
              </Link>
            </div>

            {/* Bottom Grounding Micro-badge */}
            <div className="card-grounding-tag">
              <CheckCircle2 size={13} className="text-emerald-600" />
              <span>Grounded in official BIS sources</span>
            </div>
          </div>
        </div>
      </div>

      <style>{`
        .auth-split-layout {
          min-height: 100vh;
          display: flex;
          background: #F4F3ED;
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
          color: #0F172A;
        }

        /* ── Left Intro Panel ────────────────────────────────────────── */
        .auth-intro-panel {
          flex: 1.1;
          background: #141E33;
          color: #F4F3ED;
          padding: 60px 48px;
          display: flex;
          flex-direction: column;
          justify-content: center;
          position: relative;
          border-right: 1px solid rgba(212, 175, 55, 0.2);
        }

        .intro-content {
          max-width: 480px;
          margin: 0 auto;
          display: flex;
          flex-direction: column;
          gap: 32px;
        }

        .brand-header {
          display: flex;
          flex-direction: column;
          gap: 6px;
        }

        .brand-wordmark {
          font-family: Georgia, 'Times New Roman', serif;
          font-size: 28px;
          font-weight: 700;
          letter-spacing: 0.5px;
          display: flex;
          align-items: center;
          gap: 8px;
          color: #FFFFFF;
        }

        .gold-accent {
          color: #D4AF37;
        }

        .gold-text {
          color: #D4AF37;
        }

        .gov-sub-badge {
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: 1px;
          color: #94A3B8;
          font-weight: 600;
        }

        .hero-text-block h1 {
          font-family: Georgia, 'Times New Roman', serif;
          font-size: 34px;
          font-weight: 600;
          line-height: 1.25;
          color: #FFFFFF;
          margin: 0 0 12px 0;
        }

        .hero-subtext {
          font-size: 16px;
          line-height: 1.5;
          color: #CBD5E1;
          margin: 0;
        }

        .usp-checklist {
          display: flex;
          flex-direction: column;
          gap: 14px;
          padding: 16px 0;
        }

        .usp-item {
          display: flex;
          align-items: center;
          gap: 10px;
          font-size: 15px;
          font-weight: 500;
          color: #E2E8F0;
        }

        .gold-check {
          color: #D4AF37;
          flex-shrink: 0;
        }

        .process-flow-card {
          background: rgba(255, 255, 255, 0.05);
          border: 1px solid rgba(212, 175, 55, 0.25);
          border-radius: 10px;
          padding: 12px 18px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          font-size: 13px;
          color: #E2E8F0;
        }

        .flow-step {
          display: flex;
          align-items: center;
          gap: 6px;
          font-weight: 500;
        }

        .flow-arrow {
          color: #94A3B8;
        }

        .intro-footer {
          margin-top: 20px;
          padding-top: 24px;
          border-top: 1px solid rgba(255, 255, 255, 0.1);
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .footer-line-1 {
          font-size: 12px;
          font-weight: 600;
          color: #CBD5E1;
        }

        .footer-line-2 {
          font-size: 12px;
          color: #94A3B8;
        }

        .footer-version {
          font-size: 11px;
          color: #64748B;
          margin-top: 6px;
          font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
        }

        /* ── Right Form Panel ───────────────────────────────────────── */
        .auth-form-panel {
          flex: 1;
          display: flex;
          align-items: center;
          justify-content: center;
          padding: 40px 24px;
          background: #F4F3ED;
        }

        .form-card-wrapper {
          width: 100%;
          max-width: 440px;
        }

        .auth-card {
          background: #FFFFFF;
          border: 1px solid #E2E8F0;
          box-shadow: 0 4px 20px -2px rgba(15, 23, 42, 0.06), 0 2px 6px -1px rgba(15, 23, 42, 0.04);
          border-radius: 14px;
          padding: 36px 32px;
        }

        .card-top-row {
          display: flex;
          justify-content: center;
          margin-bottom: 16px;
        }

        .small-monogram {
          display: inline-flex;
          align-items: center;
          gap: 3px;
          color: #94A3B8;
          font-weight: 600;
          font-size: 14px;
        }

        .mono-bracket {
          color: #D4AF37;
        }

        .mono-arrow {
          color: #141E33;
        }

        .auth-header {
          text-align: center;
          margin-bottom: 24px;
        }

        .auth-header h2 {
          font-family: Georgia, 'Times New Roman', serif;
          font-size: 23px;
          font-weight: 600;
          color: #141E33;
          margin: 0 0 6px 0;
          line-height: 1.3;
        }

        .auth-header p {
          font-size: 13.5px;
          color: #64748B;
          margin: 0;
        }

        .auth-error-banner {
          background: #FEF2F2;
          border: 1px solid #FECACA;
          color: #B91C1C;
          padding: 10px 14px;
          border-radius: 8px;
          font-size: 13px;
          margin-bottom: 18px;
        }

        .auth-form {
          display: flex;
          flex-direction: column;
          gap: 15px;
        }

        .form-field {
          display: flex;
          flex-direction: column;
          gap: 5px;
        }

        .field-label-row {
          display: flex;
          justify-content: space-between;
          align-items: center;
        }

        .form-field label {
          font-size: 13px;
          font-weight: 600;
          color: #334155;
        }

        .toggle-pw-btn {
          background: none;
          border: none;
          color: #64748B;
          cursor: pointer;
          padding: 0;
          display: inline-flex;
          align-items: center;
          transition: color 0.15s;
        }

        .toggle-pw-btn:hover {
          color: #141E33;
        }

        .form-field input {
          width: 100%;
          padding: 9.5px 13px;
          font-size: 14px;
          border: 1px solid #CBD5E1;
          border-radius: 8px;
          background: #FFFFFF;
          color: #0F172A;
          outline: none;
          box-sizing: border-box;
          transition: border-color 0.15s, box-shadow 0.15s;
        }

        .form-field input:focus {
          border-color: #141E33;
          box-shadow: 0 0 0 2px rgba(20, 30, 51, 0.1);
        }

        /* ── Password Strength Bar (PDF Page 2) ──────────────────────── */
        .password-strength-box {
          margin-top: 4px;
          display: flex;
          flex-direction: column;
          gap: 4px;
        }

        .strength-header {
          display: flex;
          justify-content: space-between;
          font-size: 11.5px;
          color: #64748B;
        }

        .strength-label {
          font-weight: 600;
        }

        .strength-bar-track {
          height: 4px;
          background: #E2E8F0;
          border-radius: 2px;
          overflow: hidden;
        }

        .strength-bar-fill {
          height: 100%;
          transition: width 0.25s ease, background-color 0.25s ease;
        }

        .auth-submit-btn {
          margin-top: 8px;
          width: 100%;
          padding: 12px;
          background: #141E33;
          color: #FFFFFF;
          font-weight: 600;
          font-size: 14px;
          border: none;
          border-radius: 8px;
          cursor: pointer;
          transition: background 0.15s, transform 0.05s;
        }

        .auth-submit-btn:hover:not(:disabled) {
          background: #1B2945;
        }

        .auth-submit-btn:active:not(:disabled) {
          transform: translateY(1px);
        }

        .auth-submit-btn:disabled {
          opacity: 0.65;
          cursor: not-allowed;
        }

        .auth-footer-nav {
          text-align: center;
          font-size: 13px;
          color: #64748B;
          margin-top: 20px;
          padding-top: 18px;
          border-top: 1px solid #F1F5F9;
        }

        .auth-link {
          color: #141E33;
          font-weight: 600;
          text-decoration: none;
        }

        .auth-link:hover {
          text-decoration: underline;
        }

        .card-grounding-tag {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 6px;
          font-size: 12px;
          color: #64748B;
          margin-top: 14px;
        }

        /* ── Responsive Mobile/Tablet Breakpoint ─────────────────────── */
        @media (max-width: 900px) {
          .auth-split-layout {
            flex-direction: column;
          }

          .auth-intro-panel {
            padding: 36px 20px 24px 20px;
            border-right: none;
            border-bottom: 1px solid rgba(212, 175, 55, 0.2);
          }

          .hero-text-block h1 {
            font-size: 26px;
          }

          .auth-form-panel {
            padding: 28px 16px;
          }

          .auth-card {
            padding: 24px 20px;
          }
        }
      `}</style>
    </div>
  );
}
