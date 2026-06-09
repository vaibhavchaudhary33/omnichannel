import React, { useState } from 'react'
import { Search, Eye } from 'lucide-react'
import { useCustomers } from '../context/CustomerContext'

const Customers = ({ onCustomerSelect }) => {
  const { customers } = useCustomers()
  const [search, setSearch]     = useState('')
  const [tierFilter, setTierFilter]     = useState('')
  const [sourceFilter, setSourceFilter] = useState('')

  const filtered = customers.filter(c => {
    const matchSearch = `${c.firstName} ${c.lastName} ${c.email}`.toLowerCase().includes(search.toLowerCase())
    const matchTier   = !tierFilter   || c.loyaltyTier === tierFilter
    const matchSource = !sourceFilter || c.sources.includes(sourceFilter)
    return matchSearch && matchTier && matchSource
  })

  const tierStyle = { Platinum:{bg:'rgba(123,47,255,0.25)',color:'#BFA8FF'}, Gold:{bg:'rgba(186,117,23,0.25)',color:'#FAC775'}, Silver:{bg:'rgba(136,135,128,0.25)',color:'#C8C6BE'}, Bronze:{bg:'rgba(216,90,48,0.25)',color:'#F0997B'} }
  const srcStyle  = { Shopify:{bg:'rgba(0,212,255,0.15)',color:'#00D4FF'}, PoS:{bg:'rgba(123,47,255,0.15)',color:'#BFA8FF'}, Loyalty:{bg:'rgba(0,255,136,0.1)',color:'#00FF88'} }

  return (
    <div className="p-6 space-y-5 overflow-y-auto h-full">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold" style={{color:'#00D4FF'}}>Customers</h1>
        <span className="text-xs" style={{color:'#4A5060'}}>{filtered.length} of {customers.length} profiles</span>
      </div>

      <div className="card-dark p-4 glow-border flex gap-3">
        <div className="flex-1 relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4" style={{color:'#4A5060'}} />
          <input className="input-dark w-full pl-9" placeholder="Search name or email..." value={search} onChange={e=>setSearch(e.target.value)} />
        </div>
        <select className="input-dark" value={tierFilter} onChange={e=>setTierFilter(e.target.value)}>
          <option value="">All Tiers</option>
          {['Platinum','Gold','Silver','Bronze'].map(t=><option key={t}>{t}</option>)}
        </select>
        <select className="input-dark" value={sourceFilter} onChange={e=>setSourceFilter(e.target.value)}>
          <option value="">All Sources</option>
          {['Shopify','PoS','Loyalty'].map(s=><option key={s}>{s}</option>)}
        </select>
      </div>

      <div className="card-dark glow-border overflow-hidden">
        <table className="w-full" style={{fontSize:'13px'}}>
          <thead>
            <tr style={{background:'rgba(0,212,255,0.05)', borderBottom:'0.5px solid rgba(0,212,255,0.1)'}}>
              {['Customer','Tier','Points','Sources','Total Spent','Actions'].map(h=>(
                <th key={h} className="text-left py-3 px-4" style={{color:'#4A5060', fontSize:'11px', textTransform:'uppercase'}}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filtered.map(c => (
              <tr key={c.id} style={{borderBottom:'0.5px solid rgba(0,212,255,0.05)'}} className="hover:bg-white/5 transition-colors">
                <td className="py-3 px-4">
                  <div style={{color:'#F0F4FF', fontWeight:500}}>{c.firstName} {c.lastName}</div>
                  <div style={{color:'#8890AA', fontSize:'11px'}}>{c.email}</div>
                </td>
                <td className="py-3 px-4">
                  <span style={{background:tierStyle[c.loyaltyTier]?.bg, color:tierStyle[c.loyaltyTier]?.color, padding:'2px 8px', borderRadius:'99px', fontSize:'11px'}}>{c.loyaltyTier}</span>
                </td>
                <td className="py-3 px-4" style={{color:'#F0F4FF'}}>{c.loyaltyPoints?.toLocaleString()}</td>
                <td className="py-3 px-4">
                  <div className="flex gap-1 flex-wrap">
                    {c.sources.map(s=>(
                      <span key={s} style={{background:srcStyle[s]?.bg, color:srcStyle[s]?.color, padding:'1px 6px', borderRadius:'4px', fontSize:'10px'}}>{s}</span>
                    ))}
                  </div>
                </td>
                <td className="py-3 px-4" style={{color:'#00D4FF'}}>${c.totalSpent?.toLocaleString()}</td>
                <td className="py-3 px-4">
                  <button onClick={()=>onCustomerSelect(c)} className="btn-secondary flex items-center space-x-1">
                    <Eye className="w-3 h-3" /><span>View</span>
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {filtered.length === 0 && (
          <div className="text-center py-12" style={{color:'#4A5060'}}>No customers found</div>
        )}
      </div>
    </div>
  )
}

export default Customers
