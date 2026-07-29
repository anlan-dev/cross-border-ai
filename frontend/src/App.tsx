import { useState, useCallback, useEffect } from 'react'
import Sidebar from './components/Sidebar'
import ChatPanel from './components/ChatPanel'
import Welcome from './components/Welcome'
import LiveTerminal from './components/LiveTerminal'
import MCPArchPanel from './components/MCPArchPanel'
import APISettings from './components/APISettings'
import { useWebSocket } from './hooks/useWebSocket'

export default function App() {
  const { state, run, reset } = useWebSocket()
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [lang, setLang] = useState<'zh' | 'en' | 'ja'>('zh')
  const [apiSettingsOpen, setApiSettingsOpen] = useState(false)

  const handleQuery = useCallback((query: string) => {
    run(query)
  }, [run])

  // Listen for sidebar demo query events
  useEffect(() => {
    const handler = (e: Event) => {
      const query = (e as CustomEvent).detail
      handleQuery(query)
    }
    window.addEventListener('demo-query', handler)
    return () => window.removeEventListener('demo-query', handler)
  }, [handleQuery])

  const hasResults = state.agents.length > 0 || state.cards.length > 0

  return (
    <div className="flex h-screen overflow-hidden" style={{ background: 'var(--bg)' }}>
      {/* Sidebar */}
      <Sidebar open={sidebarOpen} onClose={() => setSidebarOpen(false)} onReset={reset} lang={lang} />

      {/* Main content */}
      <div className="flex-1 flex flex-col min-w-0">
        {/* Top bar */}
        <header className="flex items-center justify-between px-5 h-14 shrink-0" style={{ background: 'var(--bg)' }}>
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-lg hover:bg-gray-100 transition-colors"
              style={{ color: 'var(--text)' }}
            >
              <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
            <div className="flex items-center gap-2.5">
              <div className="w-9 h-9 rounded-[var(--radius-md)] flex items-center justify-center text-lg font-bold text-white"
                style={{ background: 'var(--primary)', boxShadow: '0 4px 12px rgba(37,99,235,0.2)' }}>
                🌍
              </div>
              <div>
                <h1 className="text-sm font-bold" style={{ color: 'var(--text)' }}>GlobalFUN</h1>
                <p className="text-[10px]" style={{ color: 'var(--muted)' }}>Multi-Agent System</p>
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <button
              onClick={() => setApiSettingsOpen(true)}
              className="neu-btn px-3 py-2 text-xs font-medium active:scale-95"
              style={{ color: 'var(--primary)', minHeight: '44px', minWidth: '44px' }}
              title={lang === 'zh' ? 'API设置' : lang === 'en' ? 'API Settings' : 'API設定'}
            >
              🔑
            </button>
            <button
              onClick={() => setLang(l => l === 'zh' ? 'en' : l === 'en' ? 'ja' : 'zh')}
              className="neu-btn px-3 py-2 text-xs font-medium active:scale-95"
              style={{ color: 'var(--text)', minHeight: '44px' }}
            >
              {lang === 'zh' ? '🇨🇳 中文' : lang === 'en' ? '🇺🇸 English' : '🇯🇵 日本語'}
            </button>
            <span className="agent-badge" style={{ background: 'var(--primary-soft)', color: 'var(--primary)' }}>
              ¥ CNY
            </span>
            <span className={`inline-block w-2 h-2 rounded-full ${
              state.status === 'running' ? 'bg-emerald-500 animate-pulse' :
              state.status === 'error' ? 'bg-red-500' :
              state.status === 'done' ? 'bg-emerald-500' : 'bg-gray-400'
            }`} />
          </div>
        </header>

        {/* Main area */}
        <main className="flex-1 overflow-hidden">
          {!hasResults && state.status === 'idle' ? (
            <Welcome onQuery={handleQuery} lang={lang} />
          ) : (
            <div className="flex flex-col h-full">
              <div className="flex-1 overflow-y-auto">
                {/* Live Terminal */}
                <div className="px-5 pt-4">
                  <LiveTerminal agents={state.agents} status={state.status} />
                </div>

                {/* MCP Architecture Panel */}
                <div className="px-5 pt-3">
                  <MCPArchPanel agents={state.agents} status={state.status} />
                </div>

                {/* Chat results */}
                <ChatPanel state={state} onQuery={handleQuery} onReset={reset} />
              </div>
            </div>
          )}
        </main>
      </div>

      {/* API Settings Modal */}
      <APISettings isOpen={apiSettingsOpen} onClose={() => setApiSettingsOpen(false)} lang={lang} />
    </div>
  )
}
