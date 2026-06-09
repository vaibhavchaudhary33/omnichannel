import React from 'react'
import ReactDOM from 'react-dom/client'

const App = () => {
  return (
    <div style={{color:'#00D4FF', padding:'40px', background:'#0A0A0F', minHeight:'100vh'}}>
      <h1>OMNI CDP Works!</h1>
    </div>
  )
}

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
