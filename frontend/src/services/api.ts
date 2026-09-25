import axios from 'axios';
import type {
  AuthResponse,
  LoginRequest,
  RegisterRequest,
  ChatRequest,
  ChatResponse,
  Conversation,
  FeedbackRequest,
} from '../types';

// Dynamically detect server host (e.g., 5.175.234.133 or localhost)
const getApiBaseUrl = () => {
  if (import.meta.env.VITE_API_URL) return import.meta.env.VITE_API_URL;
  if (typeof window !== 'undefined' && window.location.hostname) {
    return `${window.location.protocol}//${window.location.hostname}:8080/api`;
  }
  return 'http://localhost:8080/api';
};

const API_BASE_URL = getApiBaseUrl();

// ── Startup: clear expired tokens before any request fires ───────────────────
(function clearExpiredToken() {
  const token = localStorage.getItem('token');
  if (!token) return;
  try {
    const base64Url = token.split('.')[1];
    if (!base64Url) return;
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const payload = JSON.parse(window.atob(base64));
    if (payload && payload.exp && Date.now() / 1000 > payload.exp) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
    }
  } catch {
    // If decoding fails, don't eagerly wipe localStorage
  }
})();

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Only redirect on 401 (expired or invalid token), NOT on 403 (insufficient permissions)
    const status = error.response?.status;
    const isAuthPage = window.location.pathname.includes('/login') || window.location.pathname.includes('/register');
    if (status === 401 && !isAuthPage) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  register: async (data: RegisterRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/register', data);
    return response.data;
  },

  login: async (data: LoginRequest): Promise<AuthResponse> => {
    const response = await api.post<AuthResponse>('/auth/login', data);
    return response.data;
  },
};

export const chatAPI = {
  sendMessage: async (data: ChatRequest): Promise<ChatResponse> => {
    const response = await api.post<ChatResponse>('/chat', data);
    return response.data;
  },

  getConversations: async (): Promise<Conversation[]> => {
    const response = await api.get<Conversation[]>('/chat/conversations');
    return response.data;
  },

  getConversationHistory: async (conversationId: string): Promise<any[]> => {
    const response = await api.get(`/chat/history/${conversationId}`);
    return response.data;
  },

  deleteConversation: async (conversationId: string): Promise<void> => {
    await api.delete(`/chat/conversations/${conversationId}`);
  },
};

export const feedbackAPI = {
  submitFeedback: async (data: FeedbackRequest): Promise<void> => {
    await api.post('/feedback', data);
  },
};

export interface StandardResult {
  standard_number: string;
  title: string;
  revision: string;
  relevance: number;
  document_type: string;
}

export interface AdminStats {
  totalChunks: number;
  uniqueStandards: number;
  industries: string[];
  sampleStandards: string[];
}

export interface FeedbackStats {
  totalFeedback: number;
  positiveCount: number;
  negativeCount: number;
  positiveRate: number;
}

export const finderAPI = {
  searchStandards: async (product: string, industry?: string): Promise<StandardResult[]> => {
    const params = new URLSearchParams({ product });
    if (industry && industry !== 'All') params.append('industry', industry.toLowerCase().replace(' & ', '_').replace(' ', '_'));
    const response = await api.get<StandardResult[]>(`/chat/rag/standards?${params.toString()}`);
    return response.data;
  },
};

export const adminAPI = {
  getFeedbackStats: async (): Promise<FeedbackStats> => {
    const response = await api.get<FeedbackStats>('/feedback/stats');
    return response.data;
  },
  getRagStats: async (): Promise<AdminStats> => {
    const response = await api.get<AdminStats>('/admin/stats');
    return response.data;
  },
};

export default api;
