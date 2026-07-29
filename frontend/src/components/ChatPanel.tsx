import { useState, useEffect, useRef } from 'react'
import AgentTracePanel from './AgentTracePanel'
import CardRenderer from './CardRenderer'
import type { AgentTrace, ResponseCard } from '../types'

interface PipelineState {
  status: 'idle' | 'connecting' | 'running' | 'done' | 'error'
  agents: AgentTrace[]
  cards: ResponseCard[]
  intent?: string
  intentConfidence?: number
  entities?: Record<string, string>
  summary?: string
  totalLatencyMs?: number
  totalTokens?: number
  error?: string
}

interface Props {
  state: PipelineState
  onQuery: (query: string) => void
  onReset: () => void
}

export default function ChatPanel({ state, onQuery, onReset }: Props) {
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [state.agents.length, state.cards.length, state.status])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim() && (state.status === 'done' || state.status === 'idle' || state.status === 'error')) {
      onQuery(input.trim())
      setInput('')
    }
  }

  const lastAgent = state.agents[state.agents.length - 1]
  const isRunning = state.status === 'running' || state.status === 'connecting'

  // Follow-up suggestions
  const suggestions = state.intent ? {
    price_compare: ['物流&关税', '推荐类似的', '合规检查'],
    logistics: ['差价多少？', '推荐类似的', '合规检查'],
    product_search: ['差价多少？', '物流&关税', '生成文案'],
    compliance: ['合规检查', '运营策略', '生成文案'],
    copywriting: ['运营策略', '合规检查', '跨平台对比'],
    strategy: ['生成文案', '合规检查', '跨平台对比'],
  }[state.intent] || ['推荐类似的', '差价多少？', '物流&关税'] : []

  return (
    <div className="px-5 py-4 space-y-3" style={{ animation: 'fadeIn 0.3s ease' }}>
      {/* User query */}
      {state.agents.length > 0 && (
        <div className="flex justify-end" style={{ animation: 'fadeIn 0.3s ease' }}>
          <div className="max-w-[80%] px-4 py-3 rounded-2xl text-sm"
            style={{ background: 'var(--primary)', color: 'white', boxShadow: '0 4px 12px rgba(37,99,235,0.2)' }}>
            {state.entities?.product
              ? `帮我分析「${state.entities.product}」`
              : '查看跨境电商分析结果'}
          </div>
        </div>
      )}

      {/* Agent execution trace */}
      {state.agents.length > 0 && (
        <AgentTracePanel agents={state.agents} isRunning={isRunning} />
      )}

      {/* Intent display */}
      {state.intent && (
        <div className="neu-card p-4 max-w-lg" style={{ animation: 'slideUp 0.4s ease forwards' }}>
          <div className="flex items-center gap-2 mb-2">
            <span className="text-xs font-semibold" style={{ color: 'var(--primary)' }}>意图识别</span>
            {state.intentConfidence != null && (
              <span className="agent-badge text-[10px]"
                style={{
                  background: state.intentConfidence > 0.8 ? '#dcfce7' : state.intentConfidence > 0.5 ? '#fef3c7' : '#fef2f2',
                  color: state.intentConfidence > 0.8 ? '#16a34a' : state.intentConfidence > 0.5 ? '#d97706' : '#dc2626',
                }}>
                {Math.round(state.intentConfidence * 100)}% 置信度
              </span>
            )}
          </div>
          <p className="text-sm" style={{ color: 'var(--text)' }}>
            <span style={{ color: 'var(--muted)' }}>类型: </span>
            <span className="font-medium">{state.intent}</span>
          </p>
          {state.entities && Object.keys(state.entities).length > 0 && (
            <div className="mt-2 flex flex-wrap gap-1.5">
              {Object.entries(state.entities).filter(([, v]) => v).map(([k, v]) => (
                <span key={k} className="neu-card px-2 py-0.5 text-[10px] font-medium" style={{ margin: 0, color: 'var(--text)' }}>
                  {k}: {v}
                </span>
              ))}
            </div>
          )}
        </div>
      )}

      {/* Response cards */}
      {state.cards.map((card, i) => (
        <div key={i} style={{ animation: `slideUp 0.4s ease ${i * 100}ms forwards`, opacity: 0 }}>
          <CardRenderer card={card} />
        </div>
      ))}

      {/* Typing indicator */}
      {isRunning && lastAgent?.status === 'running' && (
        <div className="inline-flex items-center gap-2 px-4 py-3 rounded-2xl max-w-[120px]"
          style={{ background: 'var(--card)', boxShadow: 'var(--shadow)', border: '1px solid var(--card-border)' }}>
          {[0, 1, 2].map(i => (
            <span key={i} className="w-2 h-2 rounded-full"
              style={{ background: 'var(--muted)', animation: `typingBounce 1.4s infinite ease-in-out`, animationDelay: `${i * 0.2}s` }} />
          ))}
        </div>
      )}

      {/* Error */}
      {state.status === 'error' && state.error && (
        <div className="neu-card p-4 max-w-md" style={{ borderLeft: '3px solid #dc2626', animation: 'slideUp 0.4s ease forwards' }}>
          <p className="text-sm" style={{ color: '#dc2626' }}>⚠️ {state.error}</p>
        </div>
      )}

      {/* Summary */}
      {state.status === 'done' && state.summary && (
        <div className="neu-card p-4 max-w-md" style={{ animation: 'slideUp 0.4s ease forwards' }}>
          <p className="text-xs mb-1" style={{ color: 'var(--muted)' }}>执行摘要</p>
          <p className="text-sm" style={{ color: 'var(--text)' }}>{state.summary}</p>
          {state.totalLatencyMs != null && (
            <div className="flex gap-4 mt-2">
              <span className="text-[10px]" style={{ color: 'var(--muted)' }}>延迟: {state.totalLatencyMs}ms</span>
              <span className="text-[10px]" style={{ color: 'var(--muted)' }}>Agents: {state.agents.length}</span>
            </div>
          )}
        </div>
      )}

      {/* Follow-up suggestions */}
      {state.status === 'done' && suggestions.length > 0 && (
        <div className="flex flex-wrap gap-2" style={{ animation: 'slideUp 0.4s ease forwards' }}>
          {suggestions.map(s => (
            <button
              key={s}
              onClick={() => onQuery(s)}
              className="neu-btn px-4 py-2 text-xs active:scale-[0.98]"
              style={{ color: 'var(--primary)', minHeight: '44px', fontWeight: 500 }}
            >
              {s}
            </button>
          ))}
        </div>
      )}

      <div ref={bottomRef} />

      {/* Input bar */}
      <div className="sticky bottom-0 pt-2 pb-1" style={{ background: 'var(--bg)' }}>
        <form onSubmit={handleSubmit} className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={e => setInput(e.target.value)}
            placeholder="继续提问..."
            disabled={isRunning}
            className="flex-1 px-4 py-3 rounded-[var(--radius-md)] text-sm outline-none transition-all focus:ring-2 focus:ring-brand-900/20 disabled:opacity-50"
            style={{
              background: 'var(--bg)',
              border: '1.5px solid var(--line)',
              boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.04)',
              color: 'var(--text)',
            }}
          />
          <button
            type="submit"
            disabled={!input.trim() || isRunning}
            className="px-5 py-3 rounded-[var(--radius-md)] text-sm font-semibold text-white transition-all disabled:opacity-30"
            style={{ background: 'var(--primary)', boxShadow: '0 4px 12px rgba(37,99,235,0.2)' }}
          >
            发送
          </button>
          {(state.status === 'done' || state.status === 'error') && (
            <button
              type="button"
              onClick={onReset}
              className="neu-btn px-4 py-3 text-sm active:scale-[0.98]"
              style={{ color: 'var(--muted)', minHeight: '44px' }}
            >
              重置
            </button>
          )}
        </form>
      </div>
    </div>
  )
}
