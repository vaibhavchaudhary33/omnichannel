import React from 'react'
import { ArrowLeft, Mail, Phone, Calendar, Award, ShoppingBag, Tag, ExternalLink } from 'lucide-react'

const ProfileDetail = ({ customer, onBack }) => {
  if (!customer) return (
    <div className="p-6 flex items-center justify-center h-full">
      <div className="text-center">
        <div className="mb-2" style={{color:'#4A5060'}}>No customer selected</div>
        <button onClick={onBack} className="btn-primary">Back to Customers</button>
      </div>
    </div>
  )

  const tierStyle = { Platinum:{bg:'rgba(123,47,255,0.25)',color:'#BFA8FF'}, Gold:{bg:'rgba(186,117,23,0.25)',color:'#FAC775'}, Silver:{bg:'rgba(136,135,128,0.25)',color:'#C8C6BE'}, Bronze:{bg:'rgba(216,90,48,0.25)',color:'#F0997B'} }
  const srcStyle  = { Shopify:{bg:'rgba(0,212,255,0.15)',color:'#00D4FF'}, PoS:{bg:'rgba(123,47,255,0.15)',color:'#BFA8FF'}, Loyalty:{bg:'rgba(0,255,136,0.1)',color:'#00FF88'} }
  const initials  = `${customer.firstName[0]}${customer.lastName[0]}`

  return (
    <div className="p-6 space-y-5 overflow-y-auto h-full">
      <div className="flex items-center space-x-4">
        <button onClick={onBack} className="btn-secondary flex items-center space-x-2">
          <ArrowLeft className="w-4 h-4" /><span>Back</span>
        </button>
        <h1 className="text-2xl font-bold" style={{color:'#00D4FF'}}>Customer Profile</h1>
      </div>

      <div className="card-dark p-6 glow-border">
        <div className="flex items-center gap-6 mb-6">
          <div className="w-14 h-14 rounded-full flex items-center justify-center text-lg font-bold flex-shrink-0" style={{background:'linear-gradient(135deg,rgba(0,212,255,0.2),rgba(123,47,255,0.2))', border:'1px solid rgba(123,47,255,0.3)', color:'#BFA8FF'}}>
            {initials}
          </div>
          <div>
            <div className="text-lg font-bold" style={{color:'#F0F4FF'}}>{customer.firstName} {customer.lastName}</div>
            <div className="text-sm mt-0.5" style={{color:'#8890AA'}}>{customer.email}</div>
            <span className="inline-block mt-2" style={{background:tierStyle[customer.loyaltyTier]?.bg, color:tierStyle[customer.loyaltyTier]?.color, padding:'2px 8px', borderRadius:'99px', fontSize:'11px'}}>{customer.loyaltyTier}</span>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-4 mb-6">
          {[
            {label:'Total Orders',    value: customer.totalOrders || 'N/A'},
            {label:'Total Spent',     value:`$${customer.totalSpent?.toLocaleString()}`},
            {label:'Loyalty Points',  value: customer.loyaltyPoints?.toLocaleString()},
          ].map((s,i)=>(
            <div key={i} className="text-center p-4 rounded-lg" style={{background:'rgba(0,212,255,0.04)', border:'0.5px solid rgba(0,212,255,0.1)'}}>
              <div className="text-lg font-bold" style={{color:'#00D4FF'}}>{s.value}</div>
              <div className="text-xs mt-1" style={{color:'#4A5060'}}>{s.label}</div>
            </div>
          ))}
        </div>

        <div className="grid grid-cols-2 gap-4">
          {[
            {icon: Mail,     label:'Email',         value: customer.email},
            {icon: Phone,    label:'Phone',         value: customer.phone || 'N/A'},
            {icon: Calendar, label:'Date of Birth',  value: customer.dateOfBirth || 'N/A'},
            {icon: Calendar, label:'Last Purchase',  value: customer.lastPurchase || 'Never'},
          ].map((item, i) => {
            const Icon = item.icon
            return (
              <div key={i} className="flex items-center gap-3">
                <Icon className="w-4 h-4 flex-shrink-0" style={{color:'#00D4FF'}} />
                <div>
                  <div className="text-xs" style={{color:'#4A5060'}}>{item.label}</div>
                  <div className="text-sm" style={{color:'#F0F4FF'}}>{item.value}</div>
                </div>
              </div>
            )
          })}
        </div>
      </div>

      <div className="card-dark p-5 glow-border">
        <h3 className="text-sm font-medium mb-3 flex items-center gap-2" style={{color:'#F0F4FF'}}><ExternalLink className="w-4 h-4" style={{color:'#00D4FF'}} />Source Systems</h3>
        {[
          {label:'Shopify ID',  value: customer.shopifyId  || '—'},
          {label:'Loyalty ID',  value: customer.loyaltyId  || '—'},
        ].map((r,i)=>(
          <div key={i} className="flex justify-between py-2" style={{borderBottom:'0.5px solid rgba(0,212,255,0.06)', fontSize:'13px'}}>
            <span style={{color:'#8890AA'}}>{r.label}</span>
            <span style={{color:'#00D4FF', fontFamily:'monospace'}}>{r.value}</span>
          </div>
        ))}
        <div className="flex justify-between py-2" style={{fontSize:'13px'}}>
          <span style={{color:'#8890AA'}}>Sources</span>
          <div className="flex gap-1">
            {customer.sources.map(s=>(
              <span key={s} style={{background:srcStyle[s]?.bg, color:srcStyle[s]?.color, padding:'1px 6px', borderRadius:'4px', fontSize:'10px'}}>{s}</span>
            ))}
          </div>
        </div>
      </div>

      {customer.tags?.length > 0 && (
        <div className="card-dark p-5 glow-border">
          <h3 className="text-sm font-medium mb-3 flex items-center gap-2" style={{color:'#F0F4FF'}}><Tag className="w-4 h-4" style={{color:'#00D4FF'}} />Tags</h3>
          <div className="flex flex-wrap gap-2">
            {customer.tags.map((t,i)=>(
              <span key={i} style={{background:'rgba(0,212,255,0.1)', color:'#00D4FF', border:'0.5px solid rgba(0,212,255,0.3)', padding:'2px 10px', borderRadius:'99px', fontSize:'12px'}}>{t}</span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}

export default ProfileDetail
