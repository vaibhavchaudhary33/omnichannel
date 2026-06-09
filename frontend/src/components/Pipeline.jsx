import React from 'react'
import { CheckCircle, Clock, AlertCircle, Play } from 'lucide-react'

const Pipeline = () => {
  const stages = [
    { name:'Shopify Ingestor',     desc:'Fetched 50 customers + 144 orders via REST API', records:194, status:'completed' },
    { name:'PoS CSV Ingestor',     desc:'Parsed 200 transactions from pos_transactions.csv', records:200, status:'completed' },
    { name:'Loyalty API Ingestor', desc:'Fetched 45 members from loyalty program API', records:45, status:'completed' },
    { name:'Transformation Layer', desc:'Cleaned emails, phones, dates, names — schema normalised', records:395, status:'completed' },
    { name:'Deduplicator',         desc:'395 raw records → 66 unified profiles', records:66, status:'completed' },
    { name:'Output Layer',         desc:'Written to data/processed/ · CSV + JSON · S3 + MySQL ready', records:66, status:'completed' },
  ]

  const statusStyle = { completed:{color:'#00FF88', bg:'rgba(0,255,136,0.1)', border:'rgba(0,255,136,0.3)'}, 'in-progress':{color:'#FAC775', bg:'rgba(250,199,117,0.1)', border:'rgba(250,199,117,0.3)'}, pending:{color:'#8890AA', bg:'rgba(136,144,170,0.1)', border:'rgba(136,144,170,0.2)'} }

  return (
    <div className="p-6 space-y-5 overflow-y-auto h-full">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold" style={{color:'#00D4FF'}}>Pipeline</h1>
        <button className="btn-primary flex items-center space-x-2">
          <Play className="w-4 h-4" /><span>Run Pipeline</span>
        </button>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {[
          {label:'Last Run',   value:'19:02 UTC'},
          {label:'Processed',  value:'395'},
          {label:'Unified',    value:'66'},
          {label:'Duplicates Removed', value:'329'},
        ].map((m,i)=>(
          <div key={i} className="card-dark p-4 glow-border">
            <div className="text-xs mb-1" style={{color:'#4A5060', textTransform:'uppercase'}}>{m.label}</div>
            <div className="text-xl font-bold" style={{color:'#00D4FF'}}>{m.value}</div>
          </div>
        ))}
      </div>

      <div className="card-dark p-6 glow-border space-y-4">
        <h3 className="text-sm font-medium" style={{color:'#F0F4FF'}}>Pipeline Stages</h3>
        {stages.map((s, i) => {
          const st = statusStyle[s.status] || statusStyle.pending
          return (
            <div key={i}>
              <div className="flex items-center gap-4 p-4 rounded-lg" style={{background:'rgba(0,212,255,0.03)', border:'0.5px solid rgba(0,212,255,0.08)'}}>
                <div className="w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0" style={{background:st.bg, border:`0.5px solid ${st.border}`}}>
                  <CheckCircle className="w-4 h-4" style={{color:st.color}} />
                </div>
                <div className="flex-1">
                  <div className="font-medium text-sm" style={{color:'#F0F4FF'}}>{s.name}</div>
                  <div className="text-xs mt-0.5" style={{color:'#8890AA'}}>{s.desc}</div>
                </div>
                <div className="text-right">
                  <div className="font-bold" style={{color:'#00D4FF'}}>{s.records.toLocaleString()}</div>
                  <div className="text-xs" style={{color:'#4A5060'}}>records</div>
                </div>
                <span style={{background:st.bg, color:st.color, border:`0.5px solid ${st.border}`, padding:'2px 8px', borderRadius:'99px', fontSize:'11px'}}>{s.status}</span>
              </div>
              {i < stages.length-1 && <div className="ml-8 w-0.5 h-3" style={{background:'rgba(0,212,255,0.1)'}}></div>}
            </div>
          )
        })}
      </div>
    </div>
  )
}

export default Pipeline
