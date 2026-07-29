import { useState } from 'react'

const DEMO_QUERIES = [
  { id: 'price_compare', query: '帮我比价SK-II神仙水，看看哪个平台最便宜', icon: '💰', category: '比价' },
  { id: 'logistics', query: '日本直邮到中国要多久？关税怎么算？', icon: '🚢', category: '物流' },
  { id: 'product_search', query: '推荐一些跨境好物', icon: '🛍️', category: '选品' },
  { id: 'compliance', query: '这款商品合规吗？能寄到中国吗？', icon: '🛡️', category: '合规' },
  { id: 'copywriting', query: '帮我写一段推广文案', icon: '✍️', category: '文案' },
  { id: 'strategy', query: '给我一些运营策略建议', icon: '📈', category: '策略' },
]

const AI_RECOMMENDS = [
  { emoji: '🧴', name: 'SK-II 神仙水', price: '¥899 · 比专柜省¥400', reason: '⭐ 跨境热销TOP1' },
  { emoji: '🐟', name: 'Swisse 鱼油胶囊', price: '¥159 · 澳洲直邮', reason: '⭐ 好评率98%' },
  { emoji: '🌸', name: 'Chanel N°5 香水', price: '¥699 · 免税价', reason: '⭐ 限时拼团中' },
  { emoji: '💆', name: 'Mediheal 面膜10片', price: '¥69 · 首单包邮', reason: '⭐ 新人专享价' },
]

interface Props {
  onQuery: (query: string) => void
  lang: string
}

export default function Welcome({ onQuery, lang }: Props) {
  const [input, setInput] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (input.trim()) onQuery(input.trim())
  }

  return (
    <div className="h-full overflow-y-auto" style={{ background: 'var(--bg)' }}>
      <div className="max-w-2xl mx-auto px-5 py-6 space-y-3.5" style={{ animation: 'fadeIn 0.3s ease' }}>

        {/* AI Recommendation Card */}
        <div className="neu-card p-5" style={{ background: 'var(--text)', color: 'white', border: 'none' }}>
          <div className="flex items-center gap-2.5 mb-4">
            <div className="w-9 h-9 rounded-[var(--radius-md)] flex items-center justify-center text-lg"
              style={{ background: 'var(--primary)', boxShadow: '0 4px 12px rgba(37,99,235,0.2)' }}>
              🤖
            </div>
            <span className="text-sm font-semibold">AI 跨境选品 · 为你推荐</span>
            <span className="ml-auto text-xs cursor-pointer" style={{ color: '#94a3b8' }}>⟳ 换一批</span>
          </div>
          <div className="grid grid-cols-2 gap-2.5">
            {AI_RECOMMENDS.map(item => (
              <button
                key={item.name}
                onClick={() => onQuery(`帮我找${item.name}`)}
                className="p-3.5 rounded-[var(--radius-md)] text-left transition-all hover:-translate-y-0.5"
                style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.08)' }}
              >
                <div className="text-xl mb-2">{item.emoji}</div>
                <div className="text-sm font-semibold">{item.name}</div>
                <div className="text-xs mt-1" style={{ color: '#93c5fd' }}>{item.price}</div>
                <div className="text-[11px] mt-1" style={{ color: '#94a3b8' }}>{item.reason}</div>
              </button>
            ))}
          </div>
        </div>

        {/* Input */}
        <form onSubmit={handleSubmit}>
          <div className="relative">
            <input
              type="text"
              value={input}
              onChange={e => setInput(e.target.value)}
              placeholder="输入您的跨境电商问题..."
              className="w-full px-4 py-3.5 rounded-[var(--radius-md)] text-sm outline-none transition-all focus:ring-2 focus:ring-brand-900/20"
              style={{
                background: 'var(--bg)',
                border: '1.5px solid var(--line)',
                boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.04)',
                color: 'var(--text)',
              }}
            />
            <button
              type="submit"
              disabled={!input.trim()}
              className="absolute right-2 top-1/2 -translate-y-1/2 w-11 h-11 rounded-full flex items-center justify-center text-white text-sm transition-all disabled:opacity-30"
              style={{ background: 'var(--primary)', boxShadow: '0 4px 12px rgba(37,99,235,0.2)', minWidth: '44px', minHeight: '44px' }}
            >
              ➤
            </button>
          </div>
        </form>

        {/* Agent pipeline visualization */}
        <div className="flex items-center gap-1.5 flex-wrap justify-center py-2">
          {[
            { icon: '🔍', label: '意图识别' },
            { icon: '📊', label: '市场调研' },
            { icon: '🛍️', label: '选品分析' },
            { icon: '🛡️', label: '合规审核' },
            { icon: '✍️', label: '文案生成' },
            { icon: '📈', label: '运营策略' },
          ].map((a, i) => (
            <div key={a.label} className="flex items-center gap-1.5">
              <div className="neu-card px-2.5 py-1.5 flex items-center gap-1.5 text-xs" style={{ color: 'var(--text)', margin: 0 }}>
                <span>{a.icon}</span>
                <span className="font-medium">{a.label}</span>
              </div>
              {i < 5 && <span className="text-xs hidden sm:inline" style={{ color: 'var(--muted)' }}>→</span>}
            </div>
          ))}
        </div>

        {/* Demo queries grid */}
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-3">
          {DEMO_QUERIES.map(q => (
            <button
              key={q.id}
              onClick={() => onQuery(q.query)}
              className="neu-card p-4 text-left transition-all hover:-translate-y-0.5 group active:scale-[0.98]"
              style={{ margin: 0, minHeight: '72px' }}
            >
              <div className="flex items-start gap-3">
                <span className="text-xl shrink-0 mt-0.5">{q.icon}</span>
                <div className="flex-1 min-w-0">
                  <span className="text-[10px] font-semibold uppercase tracking-wider" style={{ color: 'var(--primary)' }}>{q.category}</span>
                  <p className="text-sm mt-0.5 line-clamp-2 transition-colors" style={{ color: 'var(--muted)' }}>
                    {q.query}
                  </p>
                </div>
              </div>
            </button>
          ))}
        </div>

        {/* Product card preview */}
        <div className="neu-card p-5">
          <div className="rounded-[var(--radius-md)] h-48 flex items-center justify-center relative mb-4"
            style={{ background: 'var(--bg)', boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.04)', border: '1px solid var(--line)' }}>
            <span className="text-6xl">🍑</span>
            <div className="absolute top-3.5 left-3.5 flex gap-1.5">
              <span className="agent-badge text-xs" style={{ background: 'var(--bg)', color: 'var(--text)' }}>🔥 全球爆款</span>
              <span className="agent-badge text-xs" style={{ background: 'var(--bg)', color: 'var(--text)' }}>🌏 日本直邮</span>
            </div>
          </div>
          <div className="flex items-center gap-2 text-xs mb-2" style={{ color: 'var(--muted)' }}>
            <span>🇯🇵 日本 · 大阪直发</span>
            <span className="ml-auto font-medium" style={{ color: 'var(--primary)' }}>已售 8,342 件</span>
          </div>
          <h3 className="text-xl font-extrabold mb-1" style={{ color: 'var(--text)', letterSpacing: '-0.5px' }}>
            Yamanashi 白桃水润精华 200ml
          </h3>
          <p className="text-xs mb-2" style={{ color: 'var(--muted)' }}>Yamanashi Peach Moisture Essence</p>
          <div className="flex items-baseline gap-2.5 flex-wrap">
            <span className="text-3xl font-black" style={{ color: 'var(--primary)', letterSpacing: '-1px' }}>
              ¥268<small className="text-xs" style={{ color: 'var(--muted)' }}> 拼团价</small>
            </span>
            <span className="text-sm line-through" style={{ color: 'var(--muted)' }}>¥599</span>
            <span className="agent-badge text-xs" style={{ background: '#fef2f2', color: '#dc2626' }}>🔥 比国内省¥331</span>
          </div>
          <div className="flex gap-1.5 mt-3 flex-wrap">
            {['✈️ 国际直邮', '📋 关税已含', '🛡️ 正品承保'].map(t => (
              <span key={t} className="neu-card px-3 py-1.5 text-xs font-medium" style={{ margin: 0, color: 'var(--text)' }}>{t}</span>
            ))}
          </div>
        </div>

        {/* Footer */}
        <footer className="text-center py-4 text-[11px]" style={{ color: '#94a3b8' }}>
          <div className="font-semibold mb-1">GlobalFUN · 6-Agent Multi-Agent Collaboration · MCP Protocol</div>
          <div>需求解析 → 市场调研 → 选品分析 → 文案生成 → 合规审核 → 运营策略</div>
        </footer>
      </div>
    </div>
  )
}
