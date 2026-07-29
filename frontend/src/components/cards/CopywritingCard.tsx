import type { CopywritingCard as CopywritingCardType } from '../../types'

interface Props { card: CopywritingCardType }

export default function CopywritingCard({ card }: Props) {
  const { data } = card

  const handleCopy = async (text: string) => {
    try { await navigator.clipboard.writeText(text) } catch { /* fallback */ }
  }

  return (
    <div className="ai-card-wrap">
      <div className="flex items-center gap-2 px-3.5 py-3" style={{ borderBottom: '1px solid var(--line)' }}>
        <div className="w-7 h-7 rounded-[10px] flex items-center justify-center text-sm" style={{ background: '#f3e8ff' }}>✍️</div>
        <span className="text-[13px] font-bold" style={{ color: 'var(--text)' }}>{card.title}</span>
      </div>
      <div className="px-3.5 py-3">
        {/* Language tabs */}
        <div className="flex gap-1.5 mb-3 flex-wrap">
          {['🇨🇳 中文', '🇺🇸 English', '🇯🇵 日本語'].map((l, i) => (
            <span key={l} className="text-[11px] px-2.5 py-1 rounded-md font-semibold cursor-pointer"
              style={{ background: i === 0 ? 'var(--primary-soft)' : 'var(--bg)', color: i === 0 ? 'var(--primary)' : 'var(--muted)' }}>
              {l}
            </span>
          ))}
        </div>

        {/* Title */}
        <div className="p-3 rounded-xl mb-2.5 cursor-pointer hover:shadow-md transition-shadow" style={{ background: 'var(--bg)', boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.04)' }}
          onClick={() => handleCopy(data.title)}>
          <div className="text-[11px] mb-1.5" style={{ color: 'var(--muted)' }}>📝 商品标题</div>
          <div className="text-sm font-semibold" style={{ color: 'var(--text)' }}>{data.title}</div>
        </div>

        {/* Social copy */}
        <div className="p-3 rounded-xl mb-2.5 cursor-pointer hover:shadow-md transition-shadow" style={{ background: 'var(--bg)', boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.04)' }}
          onClick={() => handleCopy(data.social_copy)}>
          <div className="text-[11px] mb-1.5" style={{ color: 'var(--muted)' }}>📱 社交媒体文案</div>
          <div className="text-[13px] leading-relaxed" style={{ color: 'var(--text)' }}>{data.social_copy}</div>
        </div>

        {/* Email subjects */}
        {data.email_subjects && data.email_subjects.length > 0 && (
          <div className="p-3 rounded-xl" style={{ background: 'var(--bg)', boxShadow: 'inset 2px 2px 4px rgba(0,0,0,0.04)' }}>
            <div className="text-[11px] mb-1.5" style={{ color: 'var(--muted)' }}>📧 EDM邮件标题（A/B测试）</div>
            {data.email_subjects.map((s, i) => (
              <div key={i} className="text-[13px] mb-1" style={{ color: 'var(--text)' }}>
                {String.fromCharCode(65 + i)}: {s}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}
