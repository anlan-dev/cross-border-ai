import type { ProductAnalysisCard as ProductAnalysisCardType } from '../../types'

interface Props { card: ProductAnalysisCardType }

export default function ProductAnalysisCard({ card }: Props) {
  const { data } = card

  return (
    <div className="ai-card-wrap">
      <div className="flex items-center gap-2 px-3.5 py-3" style={{ borderBottom: '1px solid var(--line)' }}>
        <div className="w-7 h-7 rounded-[10px] flex items-center justify-center text-sm" style={{ background: '#dbeafe' }}>🛍️</div>
        <span className="text-[13px] font-bold" style={{ color: 'var(--text)' }}>{card.title}</span>
      </div>
      <div className="px-3.5 py-3">
        <div className="p-3 rounded-xl mb-3" style={{ background: 'var(--bg)', boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.04)' }}>
          <div className="text-sm font-semibold mb-2" style={{ color: 'var(--text)' }}>{data.product}</div>
          <div className="grid grid-cols-2 gap-3">
            <div>
              <div className="text-[11px]" style={{ color: 'var(--muted)' }}>最低价</div>
              <div className="text-lg font-bold" style={{ color: 'var(--primary)' }}>¥{data.lowest_price?.toFixed(0) ?? 'N/A'}</div>
              <div className="text-[10px]" style={{ color: 'var(--muted)' }}>{data.lowest_platform}</div>
            </div>
            <div>
              <div className="text-[11px]" style={{ color: 'var(--muted)' }}>好评率</div>
              <div className="text-lg font-bold" style={{ color: '#16a34a' }}>{data.review_score ?? 'N/A'}%</div>
              <div className="text-[10px]" style={{ color: 'var(--muted)' }}>{data.total_reviews ?? 0} 条评价</div>
            </div>
          </div>
        </div>

        {data.price_spread != null && (
          <div className="flex items-center gap-2 px-2.5 py-2 rounded-lg mb-2 text-xs"
            style={{ background: 'var(--bg)' }}>
            <span style={{ color: 'var(--muted)' }}>跨平台价差</span>
            <span className="ml-auto font-semibold" style={{ color: '#d97706' }}>¥{data.price_spread.toFixed(0)}</span>
          </div>
        )}

        <div className="flex items-center gap-2 px-2.5 py-2.5 rounded-lg"
          style={{ background: data.recommendation === '推荐购买' ? '#dcfce7' : '#fef3c7' }}>
          <span>{data.recommendation === '推荐购买' ? '✅' : '⚠️'}</span>
          <span className="text-sm font-semibold"
            style={{ color: data.recommendation === '推荐购买' ? '#16a34a' : '#d97706' }}>
            {data.recommendation}
          </span>
        </div>
      </div>
    </div>
  )
}
