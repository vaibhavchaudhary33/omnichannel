import React from 'react'
import { BarChart3, Users, GitBranch, UserPlus, Play, Database } from 'lucide-react'

const Sidebar = ({ activeScreen, onScreenChange }) => {
  const navItems = [
    { id: 'overview',     label: 'Overview',     icon: BarChart3  },
    { id: 'customers',    label: 'Customers',    icon: Users      },
    { id: 'pipeline',     label: 'Pipeline',     icon: GitBranch  },
    { id: 'add-customer', label: 'Add Customer', icon: UserPlus   },
  ]

  return (
    <div className="w-64 flex-shrink-0 flex flex-col" style={{background:'#0D0D14', borderRight:'0.5px solid rgba(0,212,255,0.15)'}}>
      <div className="p-6" style={{borderBottom:'0.5px solid rgba(0,212,255,0.15)'}}>
        <div className="flex items-center space-x-3">
          <div className="w-10 h-10 rounded-lg flex items-center justify-center" style={{background:'linear-gradient(135deg,#00D4FF22,#7B2FFF22)', border:'0.5px solid rgba(0,212,255,0.3)'}}>
            <Database className="w-5 h-5" style={{color:'#00D4FF'}} />
          </div>
          <div>
            <h1 className="text-base font-bold" style={{color:'#00D4FF'}}>OMNI CDP</h1>
            <p className="text-xs" style={{color:'#4A5060'}}>Data ingestion engine</p>
          </div>
        </div>
      </div>

      <nav className="flex-1 p-4">
        <p className="text-xs mb-3 px-2" style={{color:'#4A5060', textTransform:'uppercase', letterSpacing:'0.08em'}}>Main</p>
        <ul className="space-y-1">
          {navItems.map((item) => {
            const Icon = item.icon
            const isActive = activeScreen === item.id
            return (
              <li key={item.id}>
                <button
                  onClick={() => onScreenChange(item.id)}
                  className="w-full flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 text-left"
                  style={{
                    background: isActive ? 'rgba(0,212,255,0.1)' : 'transparent',
                    borderLeft: isActive ? '2px solid #00D4FF' : '2px solid transparent',
                    color: isActive ? '#00D4FF' : '#8890AA',
                  }}
                >
                  <Icon className="w-4 h-4" />
                  <span className="text-sm font-medium">{item.label}</span>
                </button>
              </li>
            )
          })}
        </ul>
      </nav>

      <div className="p-4" style={{borderTop:'0.5px solid rgba(0,212,255,0.15)'}}>
        <button className="btn-primary w-full flex items-center justify-center space-x-2">
          <Play className="w-4 h-4" />
          <span>Run Pipeline</span>
        </button>
      </div>
    </div>
  )
}

export default Sidebar
