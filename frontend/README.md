# ManakAI Frontend

React + TypeScript + Vite frontend for ManakAI BIS Standards Assistant.

## Features

- 🔐 **Authentication** - Login & Register
- 💬 **Chat Interface** - Clean, modern UI
- 📚 **Citation Display** - Show sources with standard number, clause, page
- 🎯 **Confidence Scores** - Visual confidence indicators
- 👍 **Feedback** - Thumbs up/down for responses
- 📱 **Responsive** - Works on all devices

## Quick Start

```bash
# Install dependencies
npm install

# Create environment file
cp .env.example .env

# Start development server
npm run dev

# Open http://localhost:3000
```

## Build

```bash
# Production build
npm run build

# Preview production build
npm run preview
```

## Environment Variables

Create `.env` file:

```
VITE_API_URL=http://localhost:8080/api
```

## Tech Stack

- **React 18** - UI library
- **TypeScript** - Type safety
- **Vite** - Build tool (fast!)
- **Tailwind CSS** - Styling
- **React Router** - Routing
- **Axios** - HTTP client
- **Lucide React** - Icons

## Project Structure

```
frontend/
├── src/
│   ├── pages/
│   │   ├── Login.tsx          # Login page
│   │   ├── Register.tsx       # Registration page
│   │   └── Chat.tsx           # Main chat interface
│   ├── hooks/
│   │   └── useAuth.tsx        # Authentication hook
│   ├── services/
│   │   └── api.ts             # API client
│   ├── types/
│   │   └── index.ts           # TypeScript types
│   ├── App.tsx                # Main app + routing
│   ├── main.tsx               # Entry point
│   └── index.css              # Global styles
├── package.json
├── vite.config.ts
├── tailwind.config.js
└── tsconfig.json
```

## API Integration

Frontend connects to Spring Boot backend at `http://localhost:8080/api`:

```
POST /api/auth/register
POST /api/auth/login
POST /api/chat
GET  /api/chat/conversations
GET  /api/chat/history/{id}
POST /api/feedback
```

## Features

### Authentication
- JWT-based authentication
- Token stored in localStorage
- Auto-redirect on auth state change
- Protected routes

### Chat Interface
- Send queries to AI
- Receive answers with citations
- Display confidence scores
- Show source documents
- Submit feedback (thumbs up/down)

### Citation Display
- Standard number
- Title
- Clause number
- Page number
- Document type
- Link to source (if available)

## Development

```bash
# Start dev server
npm run dev

# Type checking
npm run build

# Lint
npm run lint
```

## Monday Demo Ready! 🚀

This frontend is optimized for quick demo:
- Clean, professional UI
- Evidence-first design
- Works with backend API
- Mobile responsive
