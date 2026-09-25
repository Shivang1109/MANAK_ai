export interface User {
  id: string;
  username: string;
  email: string;
  role: string;
}

export interface AuthResponse {
  token: string;
  userId: string;
  username: string;
  email: string;
  role: string;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface Source {
  standardNumber: string;
  title: string;
  clause: string;
  page: number;
  documentType: string;
  sourceUrl?: string;
  contentPreview: string;
  relevanceScore?: number; // ADD THIS for "Why this answer?" demo
}

export interface ChatMessage {
  id?: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  confidence?: string;
  confidenceScore?: number;
  timestamp?: string;
}

export interface ChatRequest {
  query: string;
  conversationId: string | null;
}

export interface ChatResponse {
  conversationId: string;
  answer: string;
  sources: Source[];
  confidence: string;
  confidenceScore: number;
  processingTimeMs: number;
  timestamp: string;
}

export interface Conversation {
  id: string;
  title: string;
  createdAt: string;
  lastMessageAt: string;
}

export interface FeedbackRequest {
  messageId: string;
  rating: number;
  comment?: string;
  feedbackType: 'positive' | 'negative' | 'neutral';
}
