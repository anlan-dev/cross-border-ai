export interface AgentMeta {
  agent: string
  role: string
  icon: string
}

export interface AgentTrace {
  agent: string
  role: string
  icon: string
  status: 'running' | 'success' | 'error'
  latency_ms: number
  output?: Record<string, unknown>
}

export interface PriceItem {
  platform: string
  icon: string
  price: number
  currency: string
}

export interface PriceCard {
  type: 'price_compare'
  title: string
  data: {
    product: string
    lowest_price: number
    lowest_platform: string
    prices: PriceItem[]
    price_range: { min: number; max: number; spread: number }
  }
}

export interface ComplianceCheck {
  id: string
  label: string
  regulation: string
  status: string
  icon: string
}

export interface ComplianceCard {
  type: 'compliance'
  title: string
  data: {
    product: string
    target_market: string
    overall_pass: boolean
    checks: ComplianceCheck[]
    applicable_markets: string[]
  }
}

export interface CopywritingCard {
  type: 'copywriting'
  title: string
  data: {
    title: string
    social_copy: string
    email_subjects: string[]
  }
}

export interface StrategyInsight {
  metric: string
  value: string
  insight: string
}

export interface StrategyItem {
  priority: number
  action: string
  expected_roi: string
}

export interface StrategyCard {
  type: 'strategy'
  title: string
  data: {
    market_insights: StrategyInsight[]
    strategies: StrategyItem[]
    risk_alerts: string[]
  }
}

export interface ProductAnalysisCard {
  type: 'product_analysis'
  title: string
  data: {
    product: string
    lowest_price: number
    lowest_platform: string
    price_spread: number
    review_score: number
    total_reviews: number
    recommendation: string
  }
}

export type ResponseCard = PriceCard | ComplianceCard | CopywritingCard | StrategyCard | ProductAnalysisCard

export interface QueryResult {
  intent?: string
  intent_confidence?: number
  entities?: Record<string, string>
  response_cards?: ResponseCard[]
  agent_trace?: AgentTrace[]
  summary?: string
  total_latency_ms?: number
  total_tokens?: number
}

export interface DemoQuery {
  id: string
  query: string
  icon: string
  category: string
}

export interface WsEvent {
  type: 'start' | 'agent_start' | 'agent_done' | 'card' | 'summary' | 'done' | 'error'
  query?: string
  agent?: string
  role?: string
  icon?: string
  latency_ms?: number
  status?: string
  output?: Record<string, unknown>
  card?: ResponseCard
  summary?: string
  total_latency_ms?: number
  total_tokens?: number
  result?: Record<string, unknown>
  message?: string
}
