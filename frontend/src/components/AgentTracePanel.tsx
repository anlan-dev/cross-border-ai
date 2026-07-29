import type { AgentTrace } from '../types'

interface Props {
  agents: AgentTrace[]
  isRunning: boolean
}

export default function AgentTracePanel({ agents, isRunning }: Props) {
  return (
    <div className="neu-card p-4 max-w-2xl" style={{ animation: 'slideUp 0.4s ease forwards' }}>
      <div className="flex items-center gap-2 mb-3">
        <svg className="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: 'var(--primary)' }}>
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
        <span className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--primary)' }}>Agent 执行链路</span>
        {isRunning && (
          <span className="ml-auto text-[10px] animate-pulse" style={{ color: 'var(--muted)' }}>执行中...</span>
        )}
      </div>

      <div className="flex items-center gap-1 flex-wrap">
        {agents.map((agent, i) => (
          <div key={agent.agent} className="flex items-center gap-1">
            <div
              className="relative flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg text-xs font-medium transition-all duration-300"
              style={{
                background: agent.status === 'running' ? 'var(--primary-soft)' : agent.status === 'success' ? '#dcfce7' : '#fef2f2',
                color: agent.status === 'running' ? 'var(--primary)' : agent.status === 'success' ? '#16a34a' : '#dc2626',
                border: agent.status === 'running' ? '1.5px solid var(--primary)' : agent.status === 'success' ? '1.5px solid #16a34a' : '1.5px solid #dc2626',
                boxShadow: agent.status === 'running' ? '0 0 12px rgba(37,99,235,0.12)' : 'var(--shadow)',
              }}
            >
              {agent.status === 'running' && (
                <svg className="w-3 h-3 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z" />
                </svg>
              )}
              {agent.status === 'success' && (
                <svg className="w-3 h-3" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                </svg>
              )}
              <span>{agent.icon}</span>
              <span>{agent.role}</span>
              {agent.status === 'success' && agent.latency_ms > 0 && (
                <span className="text-[9px] ml-0.5" style={{ color: 'var(--muted)' }}>{agent.latency_ms}ms</span>
              )}
            </div>
            {i < agents.length - 1 && (
              <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: 'var(--muted)' }}>
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
              </svg>
            )}
          </div>
        ))}

        {isRunning && (
          <>
            <svg className="w-4 h-4 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: 'var(--muted)' }}>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
            </svg>
            <div className="flex gap-1">
              {[0, 1, 2].map(i => (
                <span key={i} className="w-1.5 h-1.5 rounded-full"
                  style={{ background: 'var(--muted)', animation: 'typingBounce 1.4s infinite ease-in-out', animationDelay: `${i * 0.16}s` }} />
              ))}
            </div>
          </>
        )}
      </div>
    </div>
  )
}
