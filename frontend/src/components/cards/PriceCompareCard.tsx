import type { PriceCard } from '../../types'

interface Props { card: PriceCard }

export default function PriceCompareCard({ card }: Props) {
  const { data } = card

  return (
    <div className="ai-card-wrap">
      <div className="flex items-center gap-2 px-3.5 py-3" style={{ borderBottom: '1px solid var(--line)' }}>
        <div className="w-7 h-7 rounded-[10px] flex items-center justify-center text-sm" style={{ background: '#fef3c7' }}>💰</div>
        <span className="text-[13px] font-bold" style={{ color: 'var(--text)' }}>{card.title}</span>
        <span className="ml-auto text-[11px] px-2 py-0.5 rounded-md font-semibold" style={{ background: '#dcfce7', color: '#16a34a' }}>最低价</span>
      </div>
      <div className="px-3.5 py-3">
        {data.prices.map((p) => {
          const isLowest = p.platform === data.lowest_platform
          return (
            <div key={p.platform}
              className="flex items-center justify-between py-2 px-2.5 rounded-[10px] mb-1"
              style={{
                background: isLowest ? 'var(--primary-soft)' : 'transparent',
                border: isLowest ? '1.5px solid var(--primary)' : 'none',
              }}>
              <div className="flex items-center gap-2">
                <span className="text-base">{p.icon}</span>
                <span className="text-[13px] font-medium" style={{ color: 'var(--text)', fontWeight: isLowest ? 700 : 500 }}>{p.platform}</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-sm font-bold" style={{ color: isLowest ? 'var(--primary)' : 'var(--muted)', textDecoration: isLowest ? 'none' : 'line-through' }}>
                  ¥{p.price.toFixed(0)}
                </span>
                {isLowest && (
                  <span className="text-[11px] px-1.5 py-0.5 rounded font-semibold text-white" style={{ background: 'var(--primary)' }}>
                    省¥{data.price_range.spread.toFixed(0)}
                  </span>
                )}
              </div>
            </div>
          )
        })}
        <div className="mt-2 px-2.5 py-2 rounded-[10px]" style={{ background: 'var(--primary-soft)' }}>
          <div className="text-[13px] font-semibold" style={{ color: 'var(--primary)' }}>
            💰 比最低价再省 ¥{data.price_range.spread.toFixed(0)} · 近30天降幅 {(data.price_range.spread / data.price_range.max * 100).toFixed(0)}%
          </div>
        </div>
      </div>
    </div>
  )
}
