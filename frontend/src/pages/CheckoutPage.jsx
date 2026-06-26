import React, { useState } from 'react';
import { useRecommendation } from '../hooks/useRecommendation';
import { useUser } from '../context/UserContext';
import PaymentOptionCard from '../components/PaymentOptionCard';
import Spinner from '../components/Spinner';
import { Link } from 'react-router-dom';

export default function CheckoutPage() {
  const { user } = useUser();
  const { recommendation, paymentResult, loading, fetchRecommendation, executePayment, setRecommendation, setPaymentResult } = useRecommendation();
  const [amount, setAmount] = useState('');
  const [category, setCategory] = useState('electronics');

  const categories = ['electronics', 'food', 'travel', 'groceries', 'fashion', 'health', 'entertainment', 'other'];

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!amount || isNaN(amount) || amount <= 0) return;
    fetchRecommendation(parseFloat(amount), category);
  };

  const handlePay = (method) => {
    if (!user) {
      alert("IDENTIFICATION PROTOCOL REQUIRED.");
      return;
    }
    executePayment(user.id, method, parseFloat(amount), category);
  };

  return (
    <div className="w-full text-swiss-black font-inter relative z-10 max-w-[1920px] mx-auto">
      
      {/* Header */}
      <div className="mb-24 flex flex-col lg:flex-row justify-between lg:items-end">
        <div>
           <div className="inline-block px-4 py-2 border-2 border-swiss-black font-bold uppercase text-xs tracking-widest mb-6 bg-swiss-white">
              02. SIMULATION
           </div>
           <h1 className="font-black text-[6rem] md:text-[8rem] uppercase leading-[0.85] tracking-tighter text-swiss-black max-w-2xl">
             FLUID ROUTING.
           </h1>
        </div>
      </div>
      
      {/* Search Input Box */}
      <div className="border-4 border-swiss-black bg-swiss-gray p-12 mb-24 transition-colors relative group">
        
        <div className="absolute inset-0 bg-swiss-dots opacity-20 pointer-events-none mix-blend-multiply transition-opacity group-hover:opacity-5" />
        
        <form onSubmit={handleSubmit} className="relative z-10 flex flex-col md:flex-row items-end gap-12 max-w-4xl mx-auto">
          <div className="w-full md:w-5/12 mb-6">
            <label className="text-xs font-bold uppercase tracking-widest text-[#666] block mb-4 border-l-4 border-swiss-black pl-2">INPUT VECTOR (₹)</label>
            <input 
              type="number" 
              value={amount} 
              onChange={e => setAmount(e.target.value)} 
              placeholder="0.00"
              className="w-full bg-transparent text-5xl md:text-7xl font-black text-swiss-black outline-none placeholder:text-[#ccc] tracking-tighter transition-transform focus:translate-x-2 border-b-4 border-swiss-black py-4"
              required 
            />
          </div>
          
          <div className="w-full md:w-4/12 mb-6 border-b-4 border-swiss-black pb-4">
            <label className="text-xs font-bold uppercase tracking-widest text-[#666] block mb-4 border-l-4 border-swiss-black pl-2">TAXONOMY CLASS</label>
            <div className="relative h-full flex items-center bg-transparent text-swiss-black font-bold group-hover:text-swiss-red transition-colors">
              <select 
                value={category} 
                onChange={e => setCategory(e.target.value)}
                className="w-full h-full bg-transparent text-2xl uppercase tracking-widest outline-none cursor-pointer appearance-none transition-colors"
              >
                {categories.map(c => (
                  <option key={c} value={c} className="bg-swiss-white text-swiss-black">{c}</option>
                ))}
              </select>
            </div>
          </div>
          
          <div className="w-full md:w-3/12 mb-6">
            <button type="submit" className="w-full h-[88px] bg-swiss-black text-swiss-white font-bold text-lg uppercase tracking-widest border-2 border-swiss-black hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150 ease-linear rounded-none" disabled={loading}>
              {loading ? "SCANNING..." : "ANALYZE"}
            </button>
          </div>
        </form>
      </div>

      {loading && <Spinner />}

      {/* Result Display */}
      {paymentResult && (
        <div className={`mb-32 relative border-4 p-12 md:p-24 transition-colors duration-300 group
             ${paymentResult.status === 'success' ? 'bg-swiss-white border-swiss-black' : 'bg-swiss-red border-swiss-red text-swiss-white'}
             `}>
          
          <div className={`absolute inset-0 bg-swiss-diagonal opacity-20 pointer-events-none mix-blend-multiply ${paymentResult.status === 'success' ? '' : 'invert'}`} />

          <h2 className="relative z-10 font-black text-[5rem] md:text-[8rem] uppercase leading-[0.8] tracking-tighter break-words mb-16">
            {paymentResult.status === 'success' ? 'ALIGNED.' : 'FRACTURED.'}
          </h2>
          
          <div className={`relative z-10 font-bold border-l-8 pl-8 mb-24 max-w-2xl ${paymentResult.status === 'success' ? 'border-swiss-black text-swiss-black' : 'border-swiss-white text-swiss-white'}`}>
            <p className="text-xs uppercase tracking-widest mb-4 opacity-70">HASH IDENTIFIER</p>
            <p className="text-lg md:text-2xl break-all tracking-wide">{paymentResult.transaction_id || 'NULL_BUFFER_0x20F'}</p>
          </div>

          {paymentResult.status === 'success' && (
            <div className={`relative z-10 inline-flex flex-col border-4 px-12 py-8 group-hover:bg-swiss-red group-hover:text-swiss-white group-hover:border-swiss-red transition-colors duration-300
              ${paymentResult.status === 'success' ? 'bg-swiss-black text-swiss-white border-swiss-black' : ''}`}>
              <span className="opacity-70 text-xs font-bold uppercase tracking-widest mb-4">ALPHA EXTRACTED</span>
              <span className="font-black text-[4rem] md:text-[6rem] leading-none tracking-tighter">
                +₹{paymentResult.cashback_earned.toFixed(2)}
              </span>
            </div>
          )}

          <div className="mt-16 relative z-10 flex gap-6">
             <Link to="/history" className="inline-flex items-center gap-4 border-4 border-swiss-black bg-swiss-white text-swiss-black px-12 py-6 font-bold uppercase text-lg tracking-widest hover:bg-swiss-black hover:text-swiss-white transition-colors duration-150 shadow-[8px_8px_0_#000]">
               VIEW LEDGER LOGS →
             </Link>
             <button onClick={() => { setPaymentResult(null); setRecommendation(null); setAmount(''); }} className="inline-flex items-center gap-4 border-4 border-swiss-black bg-swiss-gray text-swiss-black px-12 py-6 font-bold uppercase text-lg tracking-widest hover:bg-swiss-red hover:text-swiss-white hover:border-swiss-red transition-colors duration-150">
               NEW CHECKOUT
             </button>
          </div>
        </div>
      )}

      {/* Recommendation Blocks */}
      {recommendation && !paymentResult && !loading && (
        <div className="animate-fade-in-up mt-16 font-inter">
          
          {/* Analysis Reasoning Block */}
          <div className="mb-24 border-4 border-swiss-black bg-swiss-white p-12 lg:p-24 relative overflow-hidden group">
            <div className="absolute inset-0 bg-swiss-grid opacity-10 pointer-events-none mix-blend-multiply" />
            
            <div className="absolute top-0 right-0 border-l-4 border-b-4 border-swiss-black bg-swiss-red text-swiss-white px-8 py-4 font-bold uppercase text-xs tracking-widest transition-colors duration-300 group-hover:bg-swiss-black">
              LOGIC DUMP
            </div>
            
            <h3 className="relative z-10 font-black text-5xl md:text-7xl uppercase tracking-tighter text-swiss-black mb-12 flex items-center gap-8">
              ANALYSIS
              <span className="w-12 h-12 bg-swiss-red rounded-full hidden md:block"></span>
            </h3>
            
            <p className="relative z-10 font-medium text-xl md:text-3xl border-l-8 border-swiss-red pl-8 md:pl-12 text-[#333] leading-relaxed max-w-5xl">
               "{recommendation.reasoning}"
            </p>
          </div>
          
          {/* Output Gateway List Header */}
          <div className="flex border-b-4 border-swiss-black font-bold uppercase tracking-widest text-xs md:text-sm mb-16 pb-6 text-[#666]">
             VALID GATEWAYS
          </div>

          {/* Cards Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 pb-32">
            {recommendation.all_options.map((opt, idx) => (
              <PaymentOptionCard 
                key={opt.method}
                option={opt} 
                isRecommended={opt.method === recommendation.recommended_payment}
                onSelect={handlePay}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
