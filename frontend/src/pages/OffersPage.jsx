import React, { useState, useEffect } from 'react';
import { getOffers, createOffer, deleteOffer } from '../services/api';
import toast from 'react-hot-toast';
import Spinner from '../components/Spinner';

export default function OffersPage() {
  const [offers, setOffers] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);

  // Form State
  const [method, setMethod] = useState('UPI');
  const [percentage, setPercentage] = useState('');
  const [maxCashback, setMaxCashback] = useState('');
  const [minAmount, setMinAmount] = useState('0');
  const [category, setCategory] = useState('');
  const [validUntil, setValidUntil] = useState('');

  const fetchOffers = async () => {
    setLoading(true);
    try {
      const res = await getOffers();
      setOffers(res.data);
    } catch (err) {
      toast.error('SYNC ERROR');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchOffers();
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!percentage) return;

    const payload = {
      payment_method: method,
      cashback_percentage: parseFloat(percentage),
      min_amount: parseFloat(minAmount) || 0,
    };

    if (maxCashback) payload.max_cashback = parseFloat(maxCashback);
    if (category) payload.category = category;
    if (validUntil) payload.valid_until = new Date(validUntil).toISOString();

    try {
      await createOffer(payload);
      toast.success('ALGORITHM INJECTED');
      setShowForm(false);
      fetchOffers();
    } catch (err) {
      toast.error(err.response?.data?.detail || 'INJECTION REFUSED');
    }
  };

  const handleDelete = async (id) => {
    try {
      await deleteOffer(id);
      toast.success('DATA PURGED');
      fetchOffers();
    } catch (err) {
      toast.error('PURGE FAILED');
    }
  };

  return (
    <div className="w-full text-swiss-black font-inter relative z-10 max-w-[1920px] mx-auto">
      
      {/* Header Area */}
      <div className="mb-24 flex flex-col lg:flex-row justify-between lg:items-end">
        <div>
           <div className="inline-block px-4 py-2 border-2 border-swiss-black font-bold uppercase text-xs tracking-widest mb-6 bg-swiss-white">
              03. ENGINES 
           </div>
           <h1 className="font-black text-[6rem] md:text-[8rem] uppercase leading-[0.85] tracking-tighter text-swiss-black max-w-3xl block">
             RULES<br/>
             <span className="text-swiss-red">MATRIX.</span>
           </h1>
        </div>
        <button 
          className="mt-12 lg:mt-0 font-bold uppercase text-xs tracking-widest bg-swiss-black text-swiss-white border-2 border-swiss-black h-16 px-12 hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150 ease-linear rounded-none"
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "ABORT INJECTION" : "INJECT CODE"}
        </button>
      </div>

      {/* Form Injection Area */}
      {showForm && (
        <div className="mb-32 relative bg-swiss-white border-4 border-swiss-black p-12 md:p-16 lg:p-24 shadow-none">
          
          <div className="absolute inset-0 bg-swiss-diagonal opacity-[0.03] pointer-events-none mix-blend-multiply" />

          <h3 className="relative z-10 font-black text-4xl sm:text-5xl uppercase tracking-tighter text-swiss-black mb-16 pb-8 border-b-4 border-swiss-black flex justify-between items-end">
             VARIABLE COMPILATION
             <span className="font-bold text-xs tracking-widest text-[#999]">DATA IN</span>
          </h3>

          <form onSubmit={handleSubmit} className="relative z-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-12 font-bold text-xs tracking-widest uppercase items-start text-swiss-black">
            
            <div className="flex flex-col gap-4 border-l-4 border-swiss-black pl-6 group">
              <label className="text-[#666] transition-colors group-hover:text-swiss-red font-bold">TARGET VECTOR</label>
              <select value={method} onChange={e => setMethod(e.target.value)} className="w-full bg-transparent text-xl font-medium text-swiss-black outline-none cursor-pointer appearance-none border-b-4 border-swiss-black pb-4 pt-2 transition-colors group-hover:border-swiss-red hover:bg-swiss-gray">
                <option value="UPI">UPI PROTOCOL</option>
                <option value="Credit Card">CREDIT_LINK</option>
                <option value="Debit Card">DEBIT_LINK</option>
                <option value="Wallet">VAULT_X</option>
                <option value="Net Banking">LEGACY_BANK</option>
              </select>
            </div>
            
            <div className="flex flex-col gap-4 border-l-4 border-swiss-black pl-6 group">
              <label className="text-[#666] transition-colors group-hover:text-swiss-red font-bold">YIELD QUOTIENT (%)</label>
              <input type="number" step="0.1" value={percentage} onChange={e => setPercentage(e.target.value)} required className="w-full text-4xl font-black text-swiss-black outline-none placeholder:font-medium placeholder:text-[#ccc] border-b-4 border-swiss-black pb-2 transition-colors group-hover:border-swiss-red bg-transparent tracking-tighter" placeholder="0.0" />
            </div>

            <div className="flex flex-col gap-4 border-l-4 border-swiss-black pl-6 group">
              <label className="text-[#666] transition-colors group-hover:text-swiss-red font-bold">MAX CAP (₹)</label>
              <input type="number" value={maxCashback} onChange={e => setMaxCashback(e.target.value)} className="w-full text-3xl font-black text-swiss-black outline-none placeholder:font-medium placeholder:text-[#ccc] border-b-4 border-swiss-black pb-2 transition-colors group-hover:border-swiss-red bg-transparent" placeholder="INF" />
            </div>

            <div className="flex flex-col gap-4 border-l-4 border-swiss-black pl-6 group">
              <label className="text-[#666] transition-colors group-hover:text-swiss-red font-bold">MIN VOLUME (₹)</label>
              <input type="number" value={minAmount} onChange={e => setMinAmount(e.target.value)} className="w-full text-3xl font-black text-swiss-black outline-none placeholder:font-medium placeholder:text-[#ccc] border-b-4 border-swiss-black pb-2 transition-colors group-hover:border-swiss-red bg-transparent" placeholder="0" />
            </div>

            <div className="flex flex-col gap-4 border-l-4 border-swiss-black pl-6 group">
              <label className="text-[#666] transition-colors group-hover:text-swiss-red font-bold">TOPOLOGY CLASS</label>
              <input type="text" value={category} onChange={e => setCategory(e.target.value)} className="w-full text-2xl font-bold text-swiss-black outline-none placeholder:font-medium placeholder:text-[#ccc] border-b-4 border-swiss-black pb-4 transition-colors group-hover:border-swiss-red bg-transparent" placeholder="ANY_NODE" />
            </div>

            <div className="flex flex-col pt-8 lg:pt-0 justify-end h-full">
               <button type="submit" className="w-full bg-swiss-black text-swiss-white font-bold text-lg uppercase h-[72px] hover:bg-swiss-red transition-colors duration-150 ease-linear rounded-none hover:border-swiss-red border-2 border-swiss-black tracking-widest mt-auto">
                 OVERRIDE
               </button>
            </div>
          </form>
        </div>
      )}

      {loading ? <Spinner /> : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 xl:grid-cols-3 gap-8 mt-16 z-20 pb-32">
          {offers.length === 0 ? (
            <div className="col-span-full py-32 text-center font-black text-[5rem] md:text-[8rem] uppercase text-[#ccc] border-4 border-[#ccc] tracking-tighter leading-none bg-swiss-gray">
              NULL STATE
            </div>
          ) : (
            offers.map((o, idx) => (
              <div key={o.id} className="relative bg-swiss-white border-4 border-swiss-black p-10 group hover:bg-swiss-gray transition-colors duration-300 flex flex-col justify-between min-h-[450px]">
                
                <div className="absolute inset-0 bg-swiss-dots opacity-[0] pointer-events-none group-hover:opacity-[0.05] mix-blend-multiply transition-opacity duration-300" />
                
                {/* Header percentage abstract */}
                <div className="absolute top-0 right-0 border-b-4 border-l-4 border-swiss-black bg-swiss-white group-hover:bg-swiss-black transition-colors duration-300 z-10 font-bold px-6 py-4">
                  <span className="font-black text-4xl text-swiss-black group-hover:text-swiss-white tracking-tighter">
                    {o.cashback_percentage}% 
                  </span>
                </div>

                <div className="mb-12 border-b-4 border-swiss-black pb-8 relative z-10 w-3/4">
                   <span className="font-bold text-xs tracking-widest uppercase border-2 border-swiss-black px-4 py-2 block w-fit">
                     {o.payment_method}
                   </span>
                </div>

                <div className="flex-1 font-bold text-sm space-y-8 mb-16 uppercase text-swiss-black tracking-widest pt-4 relative z-10">
                  <div className="flex justify-between items-end border-b-2 border-swiss-black border-dashed pb-4">
                    <span className="text-[#666] text-xs">LIMIT</span>
                    <span className="text-xl font-black tracking-tighter">{o.max_cashback ? `₹${o.max_cashback}` : 'INF'}</span>
                  </div>
                  <div className="flex justify-between items-end border-b-2 border-swiss-black border-dashed pb-4">
                    <span className="text-[#666] text-xs">MIN_VOL</span>
                    <span className="text-xl font-black tracking-tighter">{o.min_amount ? `₹${o.min_amount}` : 'NULL'}</span>
                  </div>
                  <div className="flex justify-between items-end border-b-2 border-swiss-black border-dashed pb-4">
                    <span className="text-[#666] text-xs">CLASS</span>
                    <span className="border-2 border-swiss-black px-2 py-1 bg-swiss-black text-swiss-white">{o.category || 'GLOBAL'}</span>
                  </div>
                </div>

                <div className="relative z-10">
                  <button 
                    onClick={() => handleDelete(o.id)} 
                    className="w-full border-2 border-swiss-black bg-swiss-white text-swiss-black font-bold text-sm uppercase h-16 hover:bg-swiss-red hover:border-swiss-red hover:text-swiss-white transition-colors duration-150 tracking-widest flex items-center justify-between px-8"
                  >
                    <span>PURGE LINK</span>
                    <span className="font-black">×</span>
                  </button>
                </div>
              </div>
            ))
          )}
        </div>
      )}
    </div>
  );
}
