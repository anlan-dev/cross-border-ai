import type { StrategyCard as StrategyCardType } from '../../types'

interface Props { card: StrategyCardType }

const STRATEGY_COLORS = ['#dcfce7', '#dbeafe', '#f3e8ff', '#fef3c7']

export default function StrategyCard({ card }: Props) {
  const { data } = card

  return (
    <div className="ai-card-wrap">
      <div className="flex items-center gap-2 px-3.5 py-3" style={{ borderBottom: '1px solid var(--line)' }}>
        <div className="w-7 h-7 rounded-[10px] flex items-center justify-center text-sm" style={{ background: '#fef3c7' }}>📈</div>
        <span className="text-[13px] font-bold" style={{ color: 'var(--text)' }}>{card.title}</span>
      </div>
      <div className="px-3.5 py-3">
        {/* Market insights */}
        {data.market_insights && data.market_insights.length > 0 && (
          <div className="mb-3">
            <div className="text-[13px] font-semibold mb-2" style={{ color: 'var(--text)' }}>📊 市场洞察</div>
            <div className="grid grid-cols-2 gap-2">
              {data.market_insights.map((insight, i) => (
                <div key={i} className="p-2.5 rounded-[10px] text-center" style={{ background: 'var(--bg)' }}>
                  <div className="text-base font-bold" style={{ color: 'var(--primary)' }}>{insight.value}</div>
                  <div className="text-[11px]" style={{ color: 'var(--muted)' }}>{insight.metric}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Strategies */}
        {data.strategies && data.strategies.length > 0 && (
          <div>
            <div className="text-[13px] font-semibold mb-2" style={{ color: 'var(--text)' }}>🎯 推荐策略</div>
            <div className="space-y-1.5">
              {data.strategies.map((s, i) => (
                <div key={s.priority} className="flex items-center gap-2 px-2.5 py-2 rounded-lg text-xs"
                  style={{ background: STRATEGY_COLORS[i % STRATEGY_COLORS.length] }}>
                  <span>{i + 1}️⃣</span>
                  <span style={{ color: 'var(--text)' }}>{s.action}</span>
                  <span className="ml-auto text-[10px] px-1.5 py-0.5 rounded font-semibold" style={{ background: 'rgba(0,0,0,0.05)', color: 'var(--muted)' }}>
                    ROI {s.expected_roi}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Risk alerts */}
        {data.risk_alerts && data.risk_alerts.length > 0 && (
          <div className="mt-3 flex flex-wrap gap-1.5">
            {data.risk_alerts.map((r, i) => (
              <span key={i} className="text-[11px] px-2.5 py-0.5 rounded-md font-medium"
                style={{ background: '#fef3c7', color: '#d97706' }}>
                ⚠️ {r}
              </span>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
