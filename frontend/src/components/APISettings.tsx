import { useState, useEffect } from 'react'

interface APIKey {
  id: string
  name: string
  provider: string
  masked_key: string
  base_url?: string
  model?: string
  is_active: boolean
  created_at: string
  last_used?: string
}

interface Provider {
  id: string
  name: string
  default_model: string
  default_base_url: string
}

interface Props {
  isOpen: boolean
  onClose: () => void
  lang: string
}

export default function APISettings({ isOpen, onClose, lang }: Props) {
  const [keys, setKeys] = useState<APIKey[]>([])
  const [providers, setProviders] = useState<Provider[]>([])
  const [loading, setLoading] = useState(false)
  const [testResult, setTestResult] = useState<{ id: string; status: string; message: string } | null>(null)
  
  // Form state
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    name: '',
    provider: 'openai',
    api_key: '',
    base_url: '',
    model: '',
  })

  useEffect(() => {
    if (isOpen) {
      fetchKeys()
      fetchProviders()
    }
  }, [isOpen])

  const fetchKeys = async () => {
    try {
      const res = await fetch('/api/keys/list')
      const data = await res.json()
      setKeys(data.keys || [])
    } catch (e) {
      console.error('Failed to fetch API keys:', e)
    }
  }

  const fetchProviders = async () => {
    try {
      const res = await fetch('/api/keys/providers')
      const data = await res.json()
      setProviders(data.providers || [])
    } catch (e) {
      console.error('Failed to fetch providers:', e)
    }
  }

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    try {
      const res = await fetch('/api/keys/create', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      if (res.ok) {
        setShowForm(false)
        setFormData({ name: '', provider: 'openai', api_key: '', base_url: '', model: '' })
        fetchKeys()
      }
    } catch (e) {
      console.error('Failed to create API key:', e)
    }
    setLoading(false)
  }

  const handleDelete = async (id: string) => {
    if (!confirm(lang === 'zh' ? '确定删除此API密钥？' : lang === 'en' ? 'Delete this API key?' : 'このAPIキーを削除しますか？')) return
    try {
      await fetch(`/api/keys/${id}`, { method: 'DELETE' })
      fetchKeys()
    } catch (e) {
      console.error('Failed to delete API key:', e)
    }
  }

  const handleTest = async (id: string) => {
    setTestResult(null)
    try {
      const res = await fetch(`/api/keys/${id}/test`, { method: 'POST' })
      const data = await res.json()
      setTestResult({ id, ...data })
    } catch (e) {
      setTestResult({ id, status: 'error', message: String(e) })
    }
  }

  const handleToggle = async (id: string, isActive: boolean) => {
    try {
      await fetch(`/api/keys/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ is_active: !isActive }),
      })
      fetchKeys()
    } catch (e) {
      console.error('Failed to toggle API key:', e)
    }
  }

  const handleProviderChange = (provider: string) => {
    const p = providers.find(p => p.id === provider)
    setFormData(prev => ({
      ...prev,
      provider,
      base_url: p?.default_base_url || '',
      model: p?.default_model || '',
    }))
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4" style={{ background: 'rgba(0,0,0,0.5)' }}>
      <div className="w-full max-w-2xl max-h-[90vh] overflow-hidden rounded-2xl flex flex-col" 
        style={{ background: 'var(--card)', boxShadow: '0 20px 60px rgba(0,0,0,0.3)' }}>
        
        {/* Header */}
        <div className="flex items-center justify-between px-5 py-4 shrink-0" style={{ borderBottom: '1px solid var(--line)' }}>
          <div>
            <h2 className="text-lg font-bold" style={{ color: 'var(--text)' }}>
              {lang === 'zh' ? '🔑 API 设置' : lang === 'en' ? '🔑 API Settings' : '🔑 API設定'}
            </h2>
            <p className="text-xs mt-0.5" style={{ color: 'var(--muted)' }}>
              {lang === 'zh' ? '接入您自己的API密钥以使用AI功能' : 
               lang === 'en' ? 'Connect your own API keys to use AI features' : 
               'AI機能を使用するために独自のAPIキーを接続'}
            </p>
          </div>
          <button onClick={onClose} className="p-2.5 rounded-lg hover:bg-gray-100 active:bg-gray-200 transition-colors active:scale-95" style={{ minWidth: '44px', minHeight: '44px' }}>
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" style={{ color: 'var(--muted)' }}>
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto p-5">
          {/* Add new key button */}
          {!showForm && (
            <button
              onClick={() => setShowForm(true)}
              className="w-full neu-btn py-3 text-sm font-medium mb-4 active:scale-[0.98]"
              style={{ color: 'var(--primary)', minHeight: '48px' }}
            >
              + {lang === 'zh' ? '添加新的 API 密钥' : lang === 'en' ? 'Add New API Key' : '新しいAPIキーを追加'}
            </button>
          )}

          {/* Add form */}
          {showForm && (
            <form onSubmit={handleCreate} className="neu-card p-4 mb-4" style={{ margin: 0 }}>
              <h3 className="text-sm font-semibold mb-3" style={{ color: 'var(--text)' }}>
                {lang === 'zh' ? '添加 API 密钥' : lang === 'en' ? 'Add API Key' : 'APIキーを追加'}
              </h3>
              
              <div className="space-y-3">
                <div>
                  <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--muted)' }}>
                    {lang === 'zh' ? '名称' : 'Name'}
                  </label>
                  <input
                    type="text"
                    value={formData.name}
                    onChange={e => setFormData(prev => ({ ...prev, name: e.target.value }))}
                    placeholder={lang === 'zh' ? '例如：我的OpenAI密钥' : 'e.g. My OpenAI Key'}
                    className="w-full px-3 py-2.5 rounded-lg text-sm outline-none"
                    style={{ background: 'var(--bg)', border: '1.5px solid var(--line)', color: 'var(--text)' }}
                    required
                  />
                </div>

                <div>
                  <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--muted)' }}>
                    {lang === 'zh' ? '提供商' : 'Provider'}
                  </label>
                  <select
                    value={formData.provider}
                    onChange={e => handleProviderChange(e.target.value)}
                    className="w-full px-3 py-2.5 rounded-lg text-sm outline-none"
                    style={{ background: 'var(--bg)', border: '1.5px solid var(--line)', color: 'var(--text)' }}
                  >
                    {providers.map(p => (
                      <option key={p.id} value={p.id}>{p.name}</option>
                    ))}
                  </select>
                </div>

                <div>
                  <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--muted)' }}>
                    API Key
                  </label>
                  <input
                    type="password"
                    value={formData.api_key}
                    onChange={e => setFormData(prev => ({ ...prev, api_key: e.target.value }))}
                    placeholder="sk-..."
                    className="w-full px-3 py-2.5 rounded-lg text-sm outline-none font-mono"
                    style={{ background: 'var(--bg)', border: '1.5px solid var(--line)', color: 'var(--text)' }}
                    required
                  />
                </div>

                <div>
                  <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--muted)' }}>
                    Base URL ({lang === 'zh' ? '可选' : 'optional'})
                  </label>
                  <input
                    type="text"
                    value={formData.base_url}
                    onChange={e => setFormData(prev => ({ ...prev, base_url: e.target.value }))}
                    placeholder="https://api.openai.com/v1"
                    className="w-full px-3 py-2.5 rounded-lg text-sm outline-none font-mono"
                    style={{ background: 'var(--bg)', border: '1.5px solid var(--line)', color: 'var(--text)' }}
                  />
                </div>

                <div>
                  <label className="text-xs font-medium mb-1 block" style={{ color: 'var(--muted)' }}>
                    {lang === 'zh' ? '默认模型' : 'Default Model'} ({lang === 'zh' ? '可选' : 'optional'})
                  </label>
                  <input
                    type="text"
                    value={formData.model}
                    onChange={e => setFormData(prev => ({ ...prev, model: e.target.value }))}
                    placeholder="gpt-4o-mini"
                    className="w-full px-3 py-2.5 rounded-lg text-sm outline-none font-mono"
                    style={{ background: 'var(--bg)', border: '1.5px solid var(--line)', color: 'var(--text)' }}
                  />
                </div>
              </div>

              <div className="flex gap-2 mt-4">
                <button
                  type="submit"
                  disabled={loading}
                  className="flex-1 py-3 rounded-lg text-sm font-semibold text-white transition-all active:scale-[0.98]"
                  style={{ background: 'var(--primary)', opacity: loading ? 0.6 : 1, minHeight: '48px' }}
                >
                  {loading ? '...' : (lang === 'zh' ? '保存' : lang === 'en' ? 'Save' : '保存')}
                </button>
                <button
                  type="button"
                  onClick={() => setShowForm(false)}
                  className="px-4 py-3 rounded-lg text-sm font-medium neu-btn active:scale-[0.98]"
                  style={{ color: 'var(--muted)', minHeight: '48px' }}
                >
                  {lang === 'zh' ? '取消' : 'Cancel'}
                </button>
              </div>
            </form>
          )}

          {/* Keys list */}
          <div className="space-y-2">
            {keys.length === 0 && !showForm && (
              <div className="text-center py-8" style={{ color: 'var(--muted)' }}>
                <p className="text-3xl mb-2">🔐</p>
                <p className="text-sm">
                  {lang === 'zh' ? '尚未配置任何API密钥' : 
                   lang === 'en' ? 'No API keys configured yet' : 
                   'APIキーはまだ設定されていません'}
                </p>
                <p className="text-xs mt-1">
                  {lang === 'zh' ? '添加密钥后即可使用AI分析功能' : 
                   lang === 'en' ? 'Add a key to use AI analysis features' : 
                   'キーを追加するとAI分析機能が使用できます'}
                </p>
              </div>
            )}
            
            {keys.map(key => (
              <div key={key.id} className="neu-card p-3.5" style={{ margin: 0 }}>
                <div className="flex items-start gap-3">
                  <div className="w-9 h-9 rounded-lg flex items-center justify-center text-base shrink-0"
                    style={{ background: key.is_active ? 'var(--primary-soft)' : '#f3f4f6' }}>
                    {key.provider === 'openai' ? '🤖' : 
                     key.provider === 'anthropic' ? '🧠' : 
                     key.provider === 'google' ? '🔍' : 
                     key.provider === 'deepseek' ? '🐋' : '⚙️'}
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-semibold truncate" style={{ color: 'var(--text)' }}>{key.name}</span>
                      {!key.is_active && (
                        <span className="text-[10px] px-1.5 py-0.5 rounded font-medium" style={{ background: '#f3f4f6', color: 'var(--muted)' }}>
                          {lang === 'zh' ? '已禁用' : 'Disabled'}
                        </span>
                      )}
                    </div>
                    <div className="text-xs font-mono mt-0.5" style={{ color: 'var(--muted)' }}>{key.masked_key}</div>
                    {key.last_used && (
                      <div className="text-[10px] mt-1" style={{ color: 'var(--muted)' }}>
                        {lang === 'zh' ? '上次使用' : 'Last used'}: {new Date(key.last_used).toLocaleString()}
                      </div>
                    )}
                    {testResult?.id === key.id && (
                      <div className={`text-xs mt-1.5 px-2 py-1 rounded ${
                        testResult.status === 'valid' ? 'bg-emerald-50 text-emerald-600' :
                        testResult.status === 'assumed_valid' ? 'bg-blue-50 text-blue-600' :
                        'bg-red-50 text-red-600'
                      }`}>
                        {testResult.message}
                      </div>
                    )}
                  </div>
                </div>
                
                <div className="flex gap-2 mt-3 pl-12">
                  <button
                    onClick={() => handleTest(key.id)}
                    className="neu-btn px-3 py-2 text-[11px] font-medium active:scale-95"
                    style={{ color: 'var(--primary)', minHeight: '40px', minWidth: '60px' }}
                  >
                    {lang === 'zh' ? '测试' : 'Test'}
                  </button>
                  <button
                    onClick={() => handleToggle(key.id, key.is_active)}
                    className="neu-btn px-3 py-2 text-[11px] font-medium active:scale-95"
                    style={{ color: key.is_active ? '#d97706' : '#16a34a', minHeight: '40px', minWidth: '60px' }}
                  >
                    {key.is_active ? (lang === 'zh' ? '禁用' : 'Disable') : (lang === 'zh' ? '启用' : 'Enable')}
                  </button>
                  <button
                    onClick={() => handleDelete(key.id)}
                    className="neu-btn px-3 py-2 text-[11px] font-medium active:scale-95"
                    style={{ color: '#dc2626', minHeight: '40px', minWidth: '60px' }}
                  >
                    {lang === 'zh' ? '删除' : 'Delete'}
                  </button>
                </div>
              </div>
            ))}
          </div>

          {/* Usage guide */}
          <div className="mt-6 p-4 rounded-xl" style={{ background: 'var(--bg)', border: '1px solid var(--line)' }}>
            <h4 className="text-xs font-semibold mb-2" style={{ color: 'var(--text)' }}>
              {lang === 'zh' ? '📖 使用说明' : '📖 How to Use'}
            </h4>
            <ul className="text-[11px] space-y-1.5" style={{ color: 'var(--muted)' }}>
              <li>• {lang === 'zh' ? '支持 OpenAI、Anthropic、Google、DeepSeek 等主流提供商' : 'Supports OpenAI, Anthropic, Google, DeepSeek and more'}</li>
              <li>• {lang === 'zh' ? '可配置自定义 Base URL 以使用代理或私有部署' : 'Configure custom Base URL for proxies or private deployments'}</li>
              <li>• {lang === 'zh' ? 'API 密钥仅存储在本地服务器，不会上传到任何第三方' : 'API keys are stored locally on your server only'}</li>
              <li>• {lang === 'zh' ? '建议使用环境变量方式配置生产环境密钥' : 'Use environment variables for production key configuration'}</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}
