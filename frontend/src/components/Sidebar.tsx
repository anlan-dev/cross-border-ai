const DEMO_QUERIES = [
  { id: 'price_compare', query: '帮我比价SK-II神仙水，看看哪个平台最便宜', icon: '💰', category: '比价' },
  { id: 'logistics', query: '日本直邮到中国要多久？关税怎么算？', icon: '🚢', category: '物流' },
  { id: 'product_search', query: '推荐一些跨境好物', icon: '🛍️', category: '选品' },
  { id: 'compliance', query: '这款商品合规吗？能寄到中国吗？', icon: '🛡️', category: '合规' },
  { id: 'copywriting', query: '帮我写一段推广文案', icon: '✍️', category: '文案' },
  { id: 'strategy', query: '给我一些运营策略建议', icon: '📈', category: '策略' },
]

interface Props {
  open: boolean
  onClose: () => void
  onReset: () => void
  lang: string
}

export default function Sidebar({ open, onClose, onReset, lang }: Props) {
  return (
    <>
      {/* Mobile overlay */}
      {open && (
        <div className="fixed inset-0 bg-black/30 z-40 lg:hidden" onClick={onClose} />
      )}

      {/* Sidebar */}
      <aside
        className={`
          fixed lg:static inset-y-0 left-0 z-50
          w-72 flex flex-col
          transform transition-transform duration-300 ease-in-out
          ${open ? 'translate-x-0' : '-translate-x-full lg:translate-x-0'}
        `}
        style={{ background: 'var(--card)', borderRight: '1px solid var(--line)' }}
      >
        {/* Header */}
        <div className="flex items-center gap-2.5 px-5 h-14 shrink-0" style={{ borderBottom: '1px solid var(--line)' }}>
          <div className="w-9 h-9 rounded-[var(--radius-md)] flex items-center justify-center text-lg font-bold text-white"
            style={{ background: 'var(--primary)', boxShadow: '0 4px 12px rgba(37,99,235,0.2)' }}>
            🌍
          </div>
          <div>
            <h2 className="text-sm font-bold" style={{ color: 'var(--text)' }}>GlobalFUN</h2>
            <p className="text-[10px]" style={{ color: 'var(--muted)' }}>Cross-Border Group Buy</p>
          </div>
          <button onClick={onClose} className="ml-auto lg:hidden p-2.5 rounded-lg hover:bg-gray-100 transition-colors active:scale-95" style={{ minWidth: '44px', minHeight: '44px' }}>
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: 'var(--muted)' }}>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Tech stack */}
        <div className="px-4 py-3" style={{ borderBottom: '1px solid var(--line)' }}>
          <p className="text-[11px] font-medium uppercase tracking-wider mb-2" style={{ color: 'var(--muted)' }}>技术栈</p>
          <div className="flex flex-wrap gap-1.5">
            {['LangGraph', 'MCP Protocol', 'FastAPI', 'React'].map(t => (
              <span key={t} className="neu-card px-2 py-0.5 text-[10px] font-medium" style={{ margin: 0, color: 'var(--text)' }}>
                {t}
              </span>
            ))}
          </div>
        </div>

        {/* Agent list */}
        <div className="px-4 py-3" style={{ borderBottom: '1px solid var(--line)' }}>
          <p className="text-[11px] font-medium uppercase tracking-wider mb-2" style={{ color: 'var(--muted)' }}>智能体</p>
          <div className="space-y-0.5">
            {[
              { icon: '🔍', name: 'Intent Parser', role: '需求解析' },
              { icon: '📊', name: 'Market Analyst', role: '市场调研' },
              { icon: '🛍️', name: 'Product Scout', role: '选品分析' },
              { icon: '✍️', name: 'Copywriter', role: '文案生成' },
              { icon: '🛡️', name: 'Compliance', role: '合规审核' },
              { icon: '📈', name: 'Strategy', role: '运营策略' },
            ].map(a => (
              <div key={a.name} className="flex items-center gap-2 py-1.5 px-2 rounded-lg hover:bg-gray-50 transition-colors cursor-pointer">
                <span className="text-sm">{a.icon}</span>
                <div>
                  <span className="text-xs font-medium" style={{ color: 'var(--text)' }}>{a.role}</span>
                  <span className="text-[10px] ml-1.5" style={{ color: 'var(--muted)' }}>{a.name}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Demo queries */}
        <div className="flex-1 overflow-y-auto px-4 py-3">
          <p className="text-[11px] font-medium uppercase tracking-wider mb-2" style={{ color: 'var(--muted)' }}>示例查询</p>
          <div className="space-y-1.5">
            {DEMO_QUERIES.map(q => (
              <button
                key={q.id}
                onClick={() => {
                  onReset()
                  window.dispatchEvent(new CustomEvent('demo-query', { detail: q.query }))
                  onClose()
                }}
                className="w-full text-left px-3 py-3 rounded-lg hover:bg-gray-50 active:bg-gray-100 transition-colors group"
                style={{ minHeight: '48px' }}
              >
                <div className="flex items-center gap-2.5">
                  <span className="text-base shrink-0">{q.icon}</span>
                  <span className="text-xs line-clamp-2 transition-colors flex-1" style={{ color: 'var(--muted)' }}>
                    {q.query}
                  </span>
                </div>
              </button>
            ))}
          </div>
        </div>

        {/* Footer */}
        <div className="px-4 py-3 text-center" style={{ borderTop: '1px solid var(--line)' }}>
          <p className="text-[10px]" style={{ color: 'var(--muted)' }}>LangGraph + MCP Protocol</p>
        </div>
      </aside>
    </>
  )
}
