import { useCallback, useRef, useState } from 'react'
import type { AgentTrace, ResponseCard, WsEvent } from '../types'

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

export function useWebSocket() {
  const [state, setState] = useState<PipelineState>({
    status: 'idle',
    agents: [],
    cards: [],
  })
  const wsRef = useRef<WebSocket | null>(null)

  const run = useCallback((query: string) => {
    // Reset
    setState({
      status: 'connecting',
      agents: [],
      cards: [],
    })

    const protocol = window.location.protocol === 'https:' ? 'wss' : 'ws'
    const host = window.location.host
    const ws = new WebSocket(`${protocol}://${host}/ws/query`)
    wsRef.current = ws

    ws.onopen = () => {
      setState(prev => ({ ...prev, status: 'running' }))
      ws.send(JSON.stringify({
        query,
        user_locale: 'zh-CN',
        target_market: 'CN',
      }))
    }

    ws.onmessage = (ev) => {
      const event: WsEvent = JSON.parse(ev.data)

      setState(prev => {
        switch (event.type) {
          case 'start':
            return { ...prev, status: 'running' }

          case 'agent_start':
            return {
              ...prev,
              agents: [
                ...prev.agents,
                {
                  agent: event.agent!,
                  role: event.role!,
                  icon: event.icon!,
                  status: 'running',
                  latency_ms: 0,
                },
              ],
            }

          case 'agent_done':
            return {
              ...prev,
              agents: prev.agents.map(a =>
                a.agent === event.agent
                  ? {
                      ...a,
                      status: 'success',
                      latency_ms: event.latency_ms ?? 0,
                      output: event.output,
                    }
                  : a
              ),
              intent: event.agent === 'intent_parser'
                ? (event.output?.intent as string) ?? prev.intent
                : prev.intent,
              intentConfidence: event.agent === 'intent_parser'
                ? (event.output?.confidence as number) ?? prev.intentConfidence
                : prev.intentConfidence,
              entities: event.agent === 'intent_parser'
                ? (event.output?.entities as Record<string, string>) ?? prev.entities
                : prev.entities,
            }

          case 'card':
            return {
              ...prev,
              cards: [...prev.cards, event.card!],
            }

          case 'summary':
            return {
              ...prev,
              summary: event.summary,
              totalLatencyMs: event.total_latency_ms,
              totalTokens: event.total_tokens,
            }

          case 'done':
            return { ...prev, status: 'done' }

          case 'error':
            return { ...prev, status: 'error', error: event.message }

          default:
            return prev
        }
      })
    }

    ws.onerror = () => {
      setState(prev => ({ ...prev, status: 'error', error: 'WebSocket connection failed' }))
    }

    ws.onclose = () => {
      setState(prev => {
        if (prev.status === 'running') {
          return { ...prev, status: 'done' }
        }
        return prev
      })
    }
  }, [])

  const stop = useCallback(() => {
    wsRef.current?.close()
    setState(prev => ({ ...prev, status: 'idle' }))
  }, [])

  const reset = useCallback(() => {
    wsRef.current?.close()
    setState({ status: 'idle', agents: [], cards: [] })
  }, [])

  return { state, run, stop, reset }
}
