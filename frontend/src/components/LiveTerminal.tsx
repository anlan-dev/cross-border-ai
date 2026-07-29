import { useRef, useEffect, useState } from 'react'
import type { AgentTrace } from '../types'

interface Props {
  agents: AgentTrace[]
  status: string
}

interface LogLine {
  id: number
  ts: string
  text: string
  type: 'info' | 'agent-dispatch' | 'tool-call' | 'tool-result' | 'route-decision' | 'highlight' | 'error'
  icon: string
}

const TYPE_COLORS: Record<string, string> = {
  'info': '#94a3b8',
  'agent-dispatch': '#60a5fa',
  'tool-call': '#a78bfa',
  'tool-result': '#4ade80',
  'route-decision': '#fbbf24',
  'highlight': '#e2e8f0',
  'error': '#f87171',
}

export default function LiveTerminal({ agents, status }: Props) {
  const [lines, setLines] = useState<LogLine[]>([])
  const bodyRef = useRef<HTMLDivElement>(null)
  const idRef = useRef(0)
  const prevAgentCountRef = useRef(0)

  const addLine = (text: string, type: LogLine['type'], icon: string) => {
    const now = new Date()
    const ts = `${String(now.getHours()).padStart(2, '0')}:${String(now.getMinutes()).padStart(2, '0')}:${String(now.getSeconds()).padStart(2, '0')}.${String(now.getMilliseconds()).padStart(3, '0')}`
    setLines(prev => [...prev.slice(-49), { id: ++idRef.current, ts, text, type, icon }])
  }

  // React to agent state changes
  useEffect(() => {
    if (agents.length === 0) return

    const newAgents = agents.slice(prevAgentCountRef.current)
    prevAgentCountRef.current = agents.length

    for (const agent of newAgents) {
      if (agent.status === 'running') {
        const agentNames: Record<string, string> = {
          intent_parser: '需求解析',
          market_analyst: '市场调研',
          product_scout: '选品分析',
          compliance: '合规审核',
          copywriter: '文案生成',
          strategy: '运营策略',
          compiler: '结果汇总',
        }
        const name = agentNames[agent.agent] || agent.agent
        addLine(`Agent[${name}] 启动 · 正在调用工具...`, 'agent-dispatch', '⚡')
      } else if (agent.status === 'success') {
        const agentNames: Record<string, string> = {
          intent_parser: '需求解析',
          market_analyst: '市场调研',
          product_scout: '选品分析',
          compliance: '合规审核',
          copywriter: '文案生成',
          strategy: '运营策略',
          compiler: '结果汇总',
        }
        const name = agentNames[agent.agent] || agent.agent
        addLine(`Agent[${name}] 完成 · ${agent.latency_ms}ms`, 'tool-result', '✅')
      }
    }
  }, [agents])

  // Status change messages
  useEffect(() => {
    if (status === 'connecting') {
      addLine('WebSocket 连接建立 · 等待任务...', 'info', '🔗')
    } else if (status === 'running') {
      addLine('Orchestrator 启动 · 分析意图中...', 'route-decision', '🎯')
    } else if (status === 'done') {
      addLine('任务完成 · Agent 状态已重置', 'highlight', '🏁')
      prevAgentCountRef.current = 0
    } else if (status === 'error') {
      addLine('执行异常 · 请检查后重试', 'error', '❌')
    }
  }, [status])

  // Auto-scroll
  useEffect(() => {
    bodyRef.current?.scrollTo({ top: bodyRef.current.scrollHeight, behavior: 'smooth' })
  }, [lines])

  const isLive = status === 'running' || status === 'connecting'

  return (
    <div className="neu-card p-0 overflow-hidden" style={{ animation: 'fadeInUp 0.5s ease forwards' }}>
      <div className="live-terminal">
        {/* Header */}
        <div className="flex items-center gap-2 px-3.5 py-2.5" style={{ background: 'rgba(255,255,255,0.03)', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
          <div className="flex gap-1.5">
            <span className="w-2.5 h-2.5 rounded-full" style={{ background: '#ef4444' }} />
            <span className="w-2.5 h-2.5 rounded-full" style={{ background: '#f59e0b' }} />
            <span className="w-2.5 h-2.5 rounded-full" style={{ background: '#22c55e' }} />
          </div>
          <span className="flex-1 text-center text-[11px] font-medium" style={{ color: '#64748b' }}>
            agent-runtime · GlobalFUN Multi-Agent System
          </span>
          <span
            className="text-[10px] px-2 py-0.5 rounded font-semibold"
            style={{
              background: isLive ? 'rgba(34,197,94,0.15)' : 'rgba(148,163,184,0.15)',
              color: isLive ? '#4ade80' : '#94a3b8',
              animation: isLive ? 'badgePulse 2s infinite' : 'none',
            }}
          >
            {isLive ? '● LIVE' : status === 'done' ? '● DONE' : '● IDLE'}
          </span>
        </div>

        {/* Body */}
        <div ref={bodyRef} className="px-3.5 py-3 max-h-[280px] overflow-y-auto" style={{ scrollbarWidth: 'thin', scrollbarColor: '#334155 transparent' }}>
          {lines.length === 0 && (
            <div className="flex items-center gap-2 py-1" style={{ color: '#475569' }}>
              <span className="text-[11px] font-mono">00:00:00.000</span>
              <span className="w-4 text-center">⚙️</span>
              <span>系统初始化完成 · MCP Protocol v2.1 · 6 Agent 就绪</span>
            </div>
          )}
          {lines.map(line => (
            <div
              key={line.id}
              className="flex items-start gap-2 py-0.5"
              style={{ opacity: 0, transform: 'translateY(4px)', animation: 'lineAppear 0.3s ease forwards', color: TYPE_COLORS[line.type] || '#94a3b8' }}
            >
              <span className="text-[11px] font-mono shrink-0 select-none" style={{ color: '#475569' }}>{line.ts}</span>
              <span className="w-4 text-center shrink-0">{line.icon}</span>
              <span className="flex-1 break-all">{line.text}</span>
            </div>
          ))}
          {isLive && (
            <span className="inline-block w-[7px] h-[14px] ml-6 align-middle" style={{ background: '#60a5fa', animation: 'blink 1s step-end infinite' }} />
          )}
        </div>
      </div>
    </div>
  )
}
