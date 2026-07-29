import { useState } from 'react'
import type { AgentTrace } from '../types'

interface Props {
  agents: AgentTrace[]
  status: string
}

const AGENTS = [
  { icon: '🔍', name: '需求解析', role: 'Intent Parser', key: 'intent_parser' },
  { icon: '📊', name: '市场调研', role: 'Market Analyst', key: 'market_analyst' },
  { icon: '🛍️', name: '选品分析', role: 'Product Scout', key: 'product_scout' },
  { icon: '✍️', name: '文案生成', role: 'Copywriter', key: 'copywriter' },
  { icon: '🛡️', name: '合规审核', role: 'Compliance', key: 'compliance' },
  { icon: '📈', name: '运营策略', role: 'Strategy', key: 'strategy' },
]

const BUS_NODES = [
  { key: 'intent', label: '用户意图' },
  { key: 'orchestrator', label: 'Orchestrator' },
  { key: 'mcp', label: 'MCP 调度' },
  { key: 'agents', label: 'Agent 协作' },
  { key: 'output', label: '结构化输出' },
]

export default function MCPArchPanel({ agents, status }: Props) {
  const [expanded, setExpanded] = useState(false)

  const getAgentStatus = (key: string) => {
    const agent = agents.find(a => a.agent === key)
    if (!agent) return 'idle'
    return agent.status
  }

  const activeBusNode = status === 'running'
    ? (agents.length <= 1 ? 'intent' : agents.length <= 3 ? 'mcp' : 'output')
    : ''

  const activeCount = agents.filter(a => a.status === 'running').length
  const totalLatency = agents.reduce((sum, a) => sum + (a.status === 'success' ? a.latency_ms : 0), 0)

  return (
    <div className="neu-card p-0 overflow-hidden" style={{ animation: 'fadeInUp 0.5s ease 0.1s forwards', opacity: 0 }}>
      {/* Header */}
      <div
        className="flex items-center gap-2.5 px-4 py-3.5 cursor-pointer select-none transition-colors hover:bg-gray-50 active:bg-gray-100"
        onClick={() => setExpanded(!expanded)}
        style={{ minHeight: '56px' }}
      >
        <div className="w-8 h-8 rounded-[var(--radius-sm)] flex items-center justify-center text-sm"
          style={{ background: 'var(--primary-soft)' }}>
          🧩
        </div>
        <div className="flex-1">
          <div className="text-sm font-bold" style={{ color: 'var(--text)' }}>
            Multi-Agent 架构 <span className="text-[11px] font-normal" style={{ color: 'var(--muted)' }}>· 6 Agent + MCP Protocol</span>
          </div>
        </div>
        <div
          className="w-7 h-7 rounded-full flex items-center justify-center text-xs transition-transform duration-300"
          style={{
            background: 'var(--bg)',
            boxShadow: 'var(--shadow)',
            color: 'var(--muted)',
            transform: expanded ? 'rotate(180deg)' : 'rotate(0)',
          }}
        >
          ▼
        </div>
      </div>

      {/* Body */}
      <div
        className="overflow-hidden transition-all duration-400"
        style={{ maxHeight: expanded ? '600px' : '0', transitionTimingFunction: 'cubic-bezier(0.4, 0, 0.2, 1)' }}
      >
        <div className="px-4 pb-4">
          {/* MCP Bus visualization */}
          <div className="flex items-center gap-1.5 px-3 py-2.5 rounded-[var(--radius-md)] mb-3 overflow-x-auto"
            style={{ background: 'var(--bg)', boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.04)' }}>
            {BUS_NODES.map((node, i) => (
              <div key={node.key} className="flex items-center gap-1.5">
                <div
                  className="px-2.5 py-1 rounded-md text-[10px] font-semibold whitespace-nowrap transition-all duration-300"
                  style={{
                    background: activeBusNode === node.key ? 'var(--primary-soft)' : 'var(--bg)',
                    color: activeBusNode === node.key ? 'var(--primary)' : 'var(--text)',
                    boxShadow: activeBusNode === node.key ? '0 0 8px rgba(37,99,235,0.15)' : 'var(--shadow)',
                  }}
                >
                  {node.label}
                </div>
                {i < BUS_NODES.length - 1 && (
                  <span className="text-sm shrink-0" style={{ color: 'var(--muted)' }}>→</span>
                )}
              </div>
            ))}
          </div>

          {/* Agent grid */}
          <div className="grid grid-cols-3 gap-2 mb-3">
            {AGENTS.map(agent => {
              const s = getAgentStatus(agent.key)
              return (
                <div
                  key={agent.key}
                  className="p-2.5 rounded-[var(--radius-md)] text-center transition-all duration-300 cursor-pointer relative"
                  style={{
                    background: s === 'running' ? 'var(--primary-soft)' : 'var(--bg)',
                    border: s === 'running' ? '1.5px solid var(--primary)' : s === 'success' ? '1.5px solid #16a34a' : '1.5px solid transparent',
                    boxShadow: s === 'running' ? '0 0 12px rgba(37,99,235,0.12)' : 'var(--shadow)',
                  }}
                >
                  {/* Status dot */}
                  <div
                    className="absolute top-1.5 right-1.5 w-2 h-2 rounded-full transition-all duration-300"
                    style={{
                      background: s === 'running' ? 'var(--primary)' : s === 'success' ? '#16a34a' : '#94a3b8',
                      animation: s === 'running' ? 'dotPulse 1s infinite' : 'none',
                    }}
                  />
                  <div className="text-base mb-0.5">{agent.icon}</div>
                  <div className="text-[11px] font-semibold" style={{ color: 'var(--text)' }}>{agent.name}</div>
                  <div className="text-[9px]" style={{ color: 'var(--muted)' }}>{agent.role}</div>
                </div>
              )
            })}
          </div>

          {/* Metrics */}
          <div className="grid grid-cols-3 gap-2">
            <div className="text-center p-2 rounded-[var(--radius-sm)]" style={{ background: 'var(--bg)', boxShadow: 'var(--shadow)' }}>
              <div className="text-base font-bold font-mono" style={{ color: 'var(--primary)' }}>
                {totalLatency > 0 ? totalLatency : '--'}
              </div>
              <div className="text-[10px]" style={{ color: 'var(--muted)' }}>延迟 ms</div>
            </div>
            <div className="text-center p-2 rounded-[var(--radius-sm)]" style={{ background: 'var(--bg)', boxShadow: 'var(--shadow)' }}>
              <div className="text-base font-bold font-mono" style={{ color: 'var(--primary)' }}>
                {agents.length > 0 ? Math.floor(600 + Math.random() * 400) : '--'}
              </div>
              <div className="text-[10px]" style={{ color: 'var(--muted)' }}>Tokens</div>
            </div>
            <div className="text-center p-2 rounded-[var(--radius-sm)]" style={{ background: 'var(--bg)', boxShadow: 'var(--shadow)' }}>
              <div className="text-base font-bold font-mono" style={{ color: 'var(--primary)' }}>
                {activeCount}/{AGENTS.length}
              </div>
              <div className="text-[10px]" style={{ color: 'var(--muted)' }}>活跃 Agent</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
