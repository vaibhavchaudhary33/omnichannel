import React, { useState } from 'react'
import { ArrowLeft, Plus, X } from 'lucide-react'
import { useCustomers } from '../context/CustomerContext'

const AddCustomer = ({ onSuccess }) => {
  const { addCustomer } = useCustomers()
  const [form, setForm] = useState({ firstName:'', lastName:'', email:'', phone:'', dateOfBirth:'', loyaltyTier:'Bronze', loyaltyPoints:0, tags:[], sources:[], shopifyId:'', loyaltyId:'' })
  const [tagInput, setTagInput] = useState('')
  const [errors, setErrors]     = useState({})
  const [submitting, setSubmitting] = useState(false)
  const [success, setSuccess]   = useState(false)

  const validate = () => {
    const e = {}
    if (!form.firstName.trim()) e.firstName = 'Required'
    if (!form.lastName.trim())  e.lastName  = 'Required'
    if (!form.email.trim())     e.email     = 'Required'
    else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) e.email = 'Invalid email'
    if (!form.phone.trim())     e.phone     = 'Required'
    if (form.sources.length===0) e.sources  = 'Select at least one source'
    setErrors(e)
    return Object.keys(e).length === 0
  }

  const handleChange = e => {
    const { name, value, type, checked } = e.target
    if (type==='checkbox' && name==='sources') {
      setForm(p=>({ ...p, sources: checked ? [...p.sources, value] : p.sources.filter(s=>s!==value) }))
    } else {
      setForm(p=>({ ...p, [name]: value }))
    }
    if (errors[name]) setErrors(p=>({ ...p, [name]:'' }))
  }

  const handleTagKey = e => {
    if (e.key==='Enter' && tagInput.trim()) {
      e.preventDefault()
      if (!form.tags.includes(tagInput.trim())) setForm(p=>({ ...p, tags:[...p.tags, tagInput.trim()] }))
      setTagInput('')
    }
  }

  const handleSubmit = async e => {
    e.preventDefault()
    if (!validate()) return
    setSubmitting(true)
    await new Promise(r=>setTimeout(r, 800))
    addCustomer({ ...form, loyaltyPoints: parseInt(form.loyaltyPoints)||0 })
    setSuccess(true)
    setTimeout(() => { onSuccess() }, 1200)
    setSubmitting(false)
  }

  const inputClass = (field) => `input-dark w-full ${errors[field] ? 'border-red-500' : ''}`

  return (
    <div className="p-6 space-y-5 overflow-y-auto h-full">
      {success && (
        <div className="fixed top-4 right-4 px-4 py-3 rounded-lg text-sm font-medium z-50" style={{background:'rgba(0,255,136,0.15)', border:'0.5px solid rgba(0,255,136,0.4)', color:'#00FF88'}}>
          ✓ Customer profile created successfully!
        </div>
      )}

      <div className="flex items-center space-x-4">
        <button onClick={onSuccess} className="btn-secondary flex items-center space-x-2">
          <ArrowLeft className="w-4 h-4" /><span>Back</span>
        </button>
        <h1 className="text-2xl font-bold" style={{color:'#00D4FF'}}>Add Customer</h1>
      </div>

      <form onSubmit={handleSubmit} className="card-dark p-6 glow-border space-y-5 max-w-3xl">

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs mb-1" style={{color:'#8890AA'}}>First Name *</label>
            <input name="firstName" value={form.firstName} onChange={handleChange} className={inputClass('firstName')} placeholder="First name" />
            {errors.firstName && <p className="text-xs mt-1" style={{color:'#FF4444'}}>{errors.firstName}</p>}
          </div>
          <div>
            <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Last Name *</label>
            <input name="lastName" value={form.lastName} onChange={handleChange} className={inputClass('lastName')} placeholder="Last name" />
            {errors.lastName && <p className="text-xs mt-1" style={{color:'#FF4444'}}>{errors.lastName}</p>}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Email *</label>
            <input name="email" type="email" value={form.email} onChange={handleChange} className={inputClass('email')} placeholder="email@example.com" />
            {errors.email && <p className="text-xs mt-1" style={{color:'#FF4444'}}>{errors.email}</p>}
          </div>
          <div>
            <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Phone *</label>
            <input name="phone" value={form.phone} onChange={handleChange} className={inputClass('phone')} placeholder="+1 (555) 000-0000" />
            {errors.phone && <p className="text-xs mt-1" style={{color:'#FF4444'}}>{errors.phone}</p>}
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Date of Birth</label>
            <input name="dateOfBirth" type="date" value={form.dateOfBirth} onChange={handleChange} className="input-dark w-full" />
          </div>
          <div>
            <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Loyalty Tier</label>
            <select name="loyaltyTier" value={form.loyaltyTier} onChange={handleChange} className="input-dark w-full">
              {['Bronze','Silver','Gold','Platinum'].map(t=><option key={t}>{t}</option>)}
            </select>
          </div>
        </div>

        <div>
          <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Loyalty Points</label>
          <input name="loyaltyPoints" type="number" min="0" value={form.loyaltyPoints} onChange={handleChange} className="input-dark w-full" />
        </div>

        <div>
          <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Tags (press Enter to add)</label>
          <input value={tagInput} onChange={e=>setTagInput(e.target.value)} onKeyDown={handleTagKey} className="input-dark w-full" placeholder="Type a tag and press Enter" />
          {form.tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-2">
              {form.tags.map((t,i)=>(
                <span key={i} className="flex items-center gap-1 text-xs px-3 py-1 rounded-full" style={{background:'rgba(0,212,255,0.1)', color:'#00D4FF', border:'0.5px solid rgba(0,212,255,0.3)'}}>
                  {t}
                  <button type="button" onClick={()=>setForm(p=>({...p, tags:p.tags.filter(x=>x!==t)}))}><X className="w-3 h-3" /></button>
                </span>
              ))}
            </div>
          )}
        </div>

        <div>
          <label className="block text-xs mb-2" style={{color:'#8890AA'}}>Data Sources *</label>
          <div className="flex gap-4">
            {['Shopify','PoS','Loyalty'].map(s=>(
              <label key={s} className="flex items-center gap-2 cursor-pointer">
                <input type="checkbox" name="sources" value={s} checked={form.sources.includes(s)} onChange={handleChange} className="w-4 h-4 accent-cyan-400" />
                <span className="text-sm" style={{color:'#8890AA'}}>{s}</span>
              </label>
            ))}
          </div>
          {errors.sources && <p className="text-xs mt-1" style={{color:'#FF4444'}}>{errors.sources}</p>}
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Shopify ID <span style={{color:'#4A5060'}}>(optional)</span></label>
            <input name="shopifyId" value={form.shopifyId} onChange={handleChange} className="input-dark w-full" placeholder="SHP-00001" />
          </div>
          <div>
            <label className="block text-xs mb-1" style={{color:'#8890AA'}}>Loyalty ID <span style={{color:'#4A5060'}}>(optional)</span></label>
            <input name="loyaltyId" value={form.loyaltyId} onChange={handleChange} className="input-dark w-full" placeholder="LYL-000001" />
          </div>
        </div>

        <div className="flex justify-end pt-2">
          <button type="submit" disabled={submitting} className="btn-primary flex items-center space-x-2">
            <Plus className="w-4 h-4" />
            <span>{submitting ? 'Adding...' : 'Add Profile'}</span>
          </button>
        </div>
      </form>
    </div>
  )
}

export default AddCustomer
