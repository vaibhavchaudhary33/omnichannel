import React, { createContext, useContext, useState } from 'react'

const CustomerContext = createContext()

const initialCustomers = [
  { id:"a3f2", firstName:"Danielle", lastName:"Johnson", email:"john21@example.net", phone:"+11043321819", dateOfBirth:"1981-02-08", loyaltyTier:"Platinum", loyaltyPoints:37395, totalSpent:1104.55, lastPurchase:"2026-05-19", tags:["vip","returning"], sources:["Shopify","PoS","Loyalty"], shopifyId:"SHP-00001", loyaltyId:"LYL-000001" },
  { id:"ffc5", firstName:"Jesse", lastName:"Guzman", email:"jennifermiles@example.com", phone:"", dateOfBirth:"", loyaltyTier:"Gold", loyaltyPoints:0, totalSpent:1660.04, lastPurchase:"2026-05-25", tags:["newsletter","vip","wholesale"], sources:["Shopify","PoS"], shopifyId:"SHP-00002", loyaltyId:"" },
  { id:"550a", firstName:"Helen", lastName:"Peterson", email:"jasongallagher@example.org", phone:"+18637940265", dateOfBirth:"2004-12-07", loyaltyTier:"Silver", loyaltyPoints:1468, totalSpent:2070.16, lastPurchase:"2026-01-23", tags:[], sources:["Shopify","PoS","Loyalty"], shopifyId:"SHP-00003", loyaltyId:"LYL-000003" },
  { id:"952c", firstName:"Jessica", lastName:"Herrera", email:"smiller@example.net", phone:"+12351161559", dateOfBirth:"2006-01-26", loyaltyTier:"Bronze", loyaltyPoints:318, totalSpent:1385.70, lastPurchase:"2026-05-14", tags:["newsletter","vip"], sources:["Shopify","PoS","Loyalty"], shopifyId:"SHP-00004", loyaltyId:"LYL-000004" },
  { id:"b21f", firstName:"Michael", lastName:"Torres", email:"michael.t@example.com", phone:"+14157890123", dateOfBirth:"1990-03-15", loyaltyTier:"Silver", loyaltyPoints:4200, totalSpent:890.20, lastPurchase:"2025-12-10", tags:["returning"], sources:["Shopify","Loyalty"], shopifyId:"SHP-00005", loyaltyId:"LYL-000005" },
  { id:"c44d", firstName:"Sarah", lastName:"Chen", email:"schen@example.org", phone:"+13109876543", dateOfBirth:"1985-07-22", loyaltyTier:"Platinum", loyaltyPoints:22100, totalSpent:3210.80, lastPurchase:"2026-05-30", tags:["vip","wholesale"], sources:["Shopify","PoS","Loyalty"], shopifyId:"SHP-00006", loyaltyId:"LYL-000006" },
  { id:"d55e", firstName:"Robert", lastName:"Kim", email:"rkim@example.net", phone:"+12125550198", dateOfBirth:"1995-11-08", loyaltyTier:"Bronze", loyaltyPoints:750, totalSpent:420.50, lastPurchase:"2025-11-20", tags:[], sources:["PoS","Loyalty"], shopifyId:"", loyaltyId:"LYL-000007" },
  { id:"e66f", firstName:"Emily", lastName:"Davis", email:"emily.d@example.com", phone:"+17025551234", dateOfBirth:"1988-04-30", loyaltyTier:"Gold", loyaltyPoints:8900, totalSpent:1780.30, lastPurchase:"2026-04-18", tags:["newsletter","returning"], sources:["Shopify","PoS","Loyalty"], shopifyId:"SHP-00008", loyaltyId:"LYL-000008" },
  { id:"f77a", firstName:"James", lastName:"Wilson", email:"jwilson@example.org", phone:"", dateOfBirth:"2001-09-14", loyaltyTier:"Bronze", loyaltyPoints:200, totalSpent:195.40, lastPurchase:"2025-10-05", tags:[], sources:["PoS"], shopifyId:"", loyaltyId:"" },
  { id:"g88b", firstName:"Priya", lastName:"Sharma", email:"priya.s@example.net", phone:"+19841234567", dateOfBirth:"1981-02-08", loyaltyTier:"Platinum", loyaltyPoints:31200, totalSpent:4230.60, lastPurchase:"2026-05-19", tags:["vip","returning","newsletter"], sources:["Shopify","PoS","Loyalty"], shopifyId:"SHP-00010", loyaltyId:"LYL-000010" },
  { id:"h99c", firstName:"Carlos", lastName:"Mendez", email:"cmendez@example.com", phone:"+13055559876", dateOfBirth:"1993-06-25", loyaltyTier:"Silver", loyaltyPoints:1900, totalSpent:990.10, lastPurchase:"2026-02-14", tags:["newsletter"], sources:["Shopify","Loyalty"], shopifyId:"SHP-00011", loyaltyId:"LYL-000011" },
  { id:"i00d", firstName:"Lisa", lastName:"Park", email:"lpark@example.org", phone:"+14085553456", dateOfBirth:"1997-12-03", loyaltyTier:"Gold", loyaltyPoints:5600, totalSpent:640.75, lastPurchase:"2026-03-28", tags:["vip"], sources:["Shopify","PoS","Loyalty"], shopifyId:"SHP-00012", loyaltyId:"LYL-000012" },
]

export const CustomerProvider = ({ children }) => {
  const [customers, setCustomers] = useState(initialCustomers)

  const addCustomer = (data) => {
    const newCustomer = {
      ...data,
      id: Math.random().toString(36).substr(2, 9),
      totalSpent: 0,
      lastPurchase: null,
    }
    setCustomers(prev => [newCustomer, ...prev])
  }

  return (
    <CustomerContext.Provider value={{ customers, addCustomer }}>
      {children}
    </CustomerContext.Provider>
  )
}

export const useCustomers = () => useContext(CustomerContext)
