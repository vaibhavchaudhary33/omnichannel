import React, { useState } from 'react'
import { CustomerProvider } from './context/CustomerContext'
import Sidebar        from './components/Sidebar'
import Overview       from './components/Overview'
import Customers      from './components/Customers'
import Pipeline       from './components/Pipeline'
import ProfileDetail  from './components/ProfileDetail'
import AddCustomer    from './components/AddCustomer'

const App = () => {
  const [screen,           setScreen]           = useState('overview')
  const [selectedCustomer, setSelectedCustomer] = useState(null)

  const handleCustomerSelect = (customer) => {
    setSelectedCustomer(customer)
    setScreen('profile')
  }

  const renderScreen = () => {
    switch (screen) {
      case 'overview':     return <Overview />
      case 'customers':    return <Customers onCustomerSelect={handleCustomerSelect} />
      case 'pipeline':     return <Pipeline />
      case 'profile':      return <ProfileDetail customer={selectedCustomer} onBack={()=>setScreen('customers')} />
      case 'add-customer': return <AddCustomer onSuccess={()=>setScreen('customers')} />
      default:             return <Overview />
    }
  }

  return (
    <CustomerProvider>
      <div className="flex h-screen overflow-hidden" style={{background:'#0A0A0F'}}>
        <Sidebar activeScreen={screen} onScreenChange={setScreen} />
        <main className="flex-1 overflow-hidden">
          {renderScreen()}
        </main>
      </div>
    </CustomerProvider>
  )
}

export default App
