import type { ComplianceCard as ComplianceCardType } from '../../types'

interface Props { card: ComplianceCardType }

export default function ComplianceCard({ card }: Props) {
  const { data } = card

  return (
    <div className="ai-card-wrap">
      <div className="flex items-center gap-2 px-3.5 py-3" style={{ borderBottom: '1px solid var(--line)' }}>
        <div className="w-7 h-7 rounded-[10px] flex items-center justify-center text-sm" style={{ background: '#fef2f2' }}>🛡️</div>
        <span className="text-[13px] font-bold" style={{ color: 'var(--text)' }}>{card.title}</span>
        <span className="ml-auto text-[11px] px-2 py-0.5 rounded-md font-semibold"
          style={{ background: data.overall_pass ? '#dcfce7' : '#fef2f2', color: data.overall_pass ? '#16a34a' : '#dc2626' }}>
          {data.overall_pass ? '已通过' : '未通过'}
        </span>
      </div>
      <div className="px-3.5 py-3">
        {data.overall_pass && (
          <div className="flex items-center gap-2 px-2.5 py-2.5 rounded-[10px] mb-3" style={{ background: '#dcfce7' }}>
            <span className="text-base">✅</span>
            <span className="text-[13px] font-semibold" style={{ color: '#16a34a' }}>该商品符合目标市场法规要求</span>
          </div>
        )}
        <div className="text-[13px] font-semibold mb-2" style={{ color: 'var(--text)' }}>📋 检查项目</div>
        <div className="space-y-1.5">
          {data.checks.map(check => (
            <div key={check.id} className="flex items-center gap-2 px-2.5 py-2 rounded-lg text-xs"
              style={{ background: 'var(--bg)' }}>
              <span>{check.icon}</span>
              <span style={{ color: 'var(--text)' }}>{check.label}</span>
              <span className="ml-auto text-[11px] px-2 py-0.5 rounded-md font-medium"
                style={{
                  background: check.status === 'pass' ? '#dcfce7' : check.status === 'warning' ? '#fef3c7' : '#fef2f2',
                  color: check.status === 'pass' ? '#16a34a' : check.status === 'warning' ? '#d97706' : '#dc2626',
                }}>
                {check.regulation}
              </span>
            </div>
          ))}
        </div>
        {data.applicable_markets && (
          <div className="text-xs mt-3" style={{ color: 'var(--muted)' }}>
            🌐 适用市场：{data.applicable_markets.join(' · ')}
          </div>
        )}
      </div>
    </div>
  )
}
