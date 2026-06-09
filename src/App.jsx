import React, { useState } from 'react'
import { CustomerProvider } from './context/CustomerContext'

const App = () => {
  return (
    <CustomerProvider>
      <div style={{color:'#00D4FF', padding:'40px', background:'#0A0A0F', minHeight:'100vh'}}>
        <h1>OMNI CDP — Context Works!</h1>
      </div>
    </CustomerProvider>
  )
}

export default App
