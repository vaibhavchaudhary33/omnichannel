import React, { useEffect, useRef } from 'react'
import { Users, DollarSign, TrendingUp, Award, ArrowUp, ArrowDown } from 'lucide-react'
import { useCustomers } from '../context/CustomerContext'
import { Chart, ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend } from 'chart.js'

Chart.register(ArcElement, BarElement, CategoryScale, LinearScale, Tooltip, Legend)

const Overview = () => {
  const { customers } = useCustomers()
  const tierChartRef  = useRef(null)
  const revenueChartRef = useRef(null)
  const tierInstance  = useRef(null)
  const revenueInstance = useRef(null)

  const totalRevenue = customers.reduce((s, c) => s + (c.totalSpent || 0), 0)
  const avgSpend     = Math.round(totalRevenue / customers.length)
  const loyaltyCount = customers.filter(c => c.sources.includes('Loyalty')).length

  const metrics = [
    { title:'Total Customers',  value: customers.length, change:'+12%', trend:'up',   icon: Users,      color:'#00D4FF' },
    { title:'Total Revenue',    value:`$${totalRevenue.toLocaleString()}`, change:'+8.2%', trend:'up', icon: DollarSign, color:'#00FF88' },
    { title:'Avg Spend',        value:`$${avgSpend}`,    change:'-2.1%', trend:'down', icon: TrendingUp, color:'#FAC775' },
    { title:'Loyalty Members',  value: loyaltyCount,     change:'+15%',  trend:'up',   icon: Award,      color:'#7B2FFF' },
  ]

  useEffect(() => {
    if (tierInstance.current)    tierInstance.current.destroy()
    if (revenueInstance.current) revenueInstance.current.destroy()

    tierInstance.current = new Chart(tierChartRef.current, {
      type: 'doughnut',
      data: {
        labels: ['Platinum','Gold','Silver','Bronze'],
        datasets: [{
          data: [
            customers.filter(c=>c.loyaltyTier==='Platinum').length,
            customers.filter(c=>c.loyaltyTier==='Gold').length,
            customers.filter(c=>c.loyaltyTier==='Silver').length,
            customers.filter(c=>c.loyaltyTier==='Bronze').length,
          ],
          backgroundColor: ['#7B2FFF','#BA7517','#888780','#D85A30'],
          borderColor: '#111118', borderWidth: 2,
        }],
      },
      options: { responsive:true, maintainAspectRatio:false, cutout:'65%', plugins:{ legend:{ position:'bottom', labels:{ color:'#8890AA', font:{size:11} } } } }
    })

    revenueInstance.current = new Chart(revenueChartRef.current, {
      type: 'bar',
      data: {
        labels: ['Jan','Feb','Mar','Apr','May','Jun'],
        datasets: [{ label:'Revenue', data:[12000,19000,15000,25000,22000,30000], backgroundColor:'rgba(0,212,255,0.7)', borderRadius:4 }],
      },
      options: { responsive:true, maintainAspectRatio:false, plugins:{ legend:{ display:false } }, scales:{ y:{ ticks:{ color:'#8890AA', callback: v=>'$'+Math.round(v/1000)+'K' }, grid:{ color:'rgba(0,212,255,0.06)' } }, x:{ ticks:{ color:'#8890AA' }, grid:{ display:false } } } }
    })

    return () => {
      tierInstance.current?.destroy()
      revenueInstance.current?.destroy()
    }
  }, [customers])

  const topCustomers = [...customers].sort((a,b)=>(b.totalSpent||0)-(a.totalSpent||0)).slice(0,5)

  const tierBadge = (tier) => {
    const styles = { Platinum:'rgba(123,47,255,0.25)', Gold:'rgba(186,117,23,0.25)', Silver:'rgba(136,135,128,0.25)', Bronze:'rgba(216,90,48,0.25)' }
    const colors  = { Platinum:'#BFA8FF', Gold:'#FAC775', Silver:'#C8C6BE', Bronze:'#F0997B' }
    return <span style={{ background:styles[tier], color:colors[tier], padding:'2px 8px', borderRadius:'99px', fontSize:'11px' }}>{tier}</span>
  }

  return (
    <div className="p-6 space-y-6 overflow-y-auto h-full">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold" style={{color:'#00D4FF'}}>Overview</h1>
        <span className="text-xs" style={{color:'#4A5060'}}>Last updated: {new Date().toLocaleString()}</span>
      </div>

      <div className="grid grid-cols-4 gap-4">
        {metrics.map((m, i) => {
          const Icon = m.icon
          return (
            <div key={i} className="card-dark p-5 glow-border-hover">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-xs mb-1" style={{color:'#4A5060'}}>{m.title}</p>
                  <p className="text-xl font-bold" style={{color:'#F0F4FF'}}>{m.value}</p>
                  <div className="flex items-center mt-2 space-x-1">
                    {m.trend==='up' ? <ArrowUp className="w-3 h-3" style={{color:'#00FF88'}}/> : <ArrowDown className="w-3 h-3" style={{color:'#FF4444'}}/>}
                    <span className="text-xs" style={{color: m.trend==='up'?'#00FF88':'#FF4444'}}>{m.change}</span>
                  </div>
                </div>
                <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{background:`${m.color}22`}}>
                  <Icon className="w-5 h-5" style={{color: m.color}} />
                </div>
              </div>
            </div>
          )
        })}
      </div>

      <div className="grid grid-cols-2 gap-4">
        <div className="card-dark p-5 glow-border">
          <h3 className="text-sm font-medium mb-4" style={{color:'#F0F4FF'}}>Loyalty Tier Distribution</h3>
          <div style={{height:'200px'}}><canvas ref={tierChartRef} /></div>
        </div>
        <div className="card-dark p-5 glow-border">
          <h3 className="text-sm font-medium mb-4" style={{color:'#F0F4FF'}}>Monthly Revenue</h3>
          <div style={{height:'200px'}}><canvas ref={revenueChartRef} /></div>
        </div>
      </div>

      <div className="card-dark p-5 glow-border">
        <h3 className="text-sm font-medium mb-4" style={{color:'#F0F4FF'}}>Top Customers by Spend</h3>
        <table className="w-full" style={{fontSize:'13px'}}>
          <thead>
            <tr style={{borderBottom:'0.5px solid rgba(0,212,255,0.1)'}}>
              {['Customer','Email','Tier','Spend','Last Purchase'].map(h => (
                <th key={h} className="text-left py-2 px-3" style={{color:'#4A5060', fontSize:'11px', textTransform:'uppercase'}}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {topCustomers.map(c => (
              <tr key={c.id} style={{borderBottom:'0.5px solid rgba(0,212,255,0.05)'}}>
                <td className="py-3 px-3" style={{color:'#F0F4FF'}}>{c.firstName} {c.lastName}</td>
                <td className="py-3 px-3" style={{color:'#8890AA'}}>{c.email}</td>
                <td className="py-3 px-3">{tierBadge(c.loyaltyTier)}</td>
                <td className="py-3 px-3" style={{color:'#00D4FF'}}>${c.totalSpent?.toLocaleString()}</td>
                <td className="py-3 px-3" style={{color:'#8890AA'}}>{c.lastPurchase || 'Never'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default Overview
