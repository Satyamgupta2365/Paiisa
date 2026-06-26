import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useUser } from '../context/UserContext';
import { getUser, createUser } from '../services/api';
import toast from 'react-hot-toast';

export default function LoginPage() {
  const [tab, setTab] = useState('login');
  const [loading, setLoading] = useState(false);
  const { setUser } = useUser();
  const navigate = useNavigate();

  // Login form
  const [userId, setUserId] = useState('2305062005');

  // Reg form
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [phone, setPhone] = useState('');
  const [prefMethod, setPrefMethod] = useState('');

  const handleLogin = async (e) => {
    e.preventDefault();
    if (!userId) return;
    setLoading(true);
    try {
      let idToUse = userId.trim();
      if (idToUse === '2305062005') {
        idToUse = '23050620-0500-0000-0000-000000000000';
      }
      
      const res = await getUser(idToUse);
      setUser(res.data);
      toast.success(`IDENTIFICATION CONFIRMED`);
      navigate('/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || "INVALID UUID");
    } finally {
      setLoading(false);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    if (!name || !email) return;
    setLoading(true);

    const payload = { name, email };
    if (phone) payload.phone = phone;
    if (prefMethod) payload.preferred_payment_method = prefMethod;

    try {
      const res = await createUser(payload);
      setUser(res.data);
      toast.success("PROFILE CREATED");
      navigate('/dashboard');
    } catch (err) {
      toast.error(err.response?.data?.detail || "CREATION REJECTED");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex w-full min-h-[70vh] items-center justify-center p-4 xl:p-0 relative z-10 font-inter">
      <div className="w-full max-w-4xl bg-swiss-white border-4 border-swiss-black grid grid-cols-1 md:grid-cols-2 shadow-none transition-shadow hover:shadow-[12px_12px_0_#FF3000]">
        
        {/* Visual / Decorative Sidebar */}
        <div className="hidden md:flex flex-col border-r-4 border-swiss-black bg-swiss-gray p-12 relative overflow-hidden group">
          <div className="absolute inset-0 bg-swiss-dots opacity-40 mix-blend-multiply" />
          
          <div className="relative z-10 flex-col h-full flex justify-between">
            <h2 className="font-black text-7xl uppercase tracking-tighter text-swiss-black leading-none group-hover:text-swiss-red transition-colors duration-150">
              ID.<br/>REQ.
            </h2>
            
            <div className="font-bold text-xs uppercase tracking-widest text-[#666]">
              Swiss Objective <br/> Verification Protocol
            </div>
          </div>
        </div>

        {/* Action Panel */}
        <div className="p-8 md:p-12 relative bg-swiss-white">
          <div className="flex border-2 border-swiss-black font-bold uppercase tracking-widest text-xs mb-12">
             <button 
               className={`w-1/2 py-4 transition-colors duration-150 ease-linear ${tab === 'login' ? 'bg-swiss-black text-swiss-white' : 'bg-swiss-white text-swiss-black hover:bg-swiss-red hover:text-swiss-white border-r-2 border-swiss-black'}`}
               onClick={() => setTab('login')}
             >
               CONNECT
             </button>
             <button 
               className={`w-1/2 py-4 transition-colors duration-150 ease-linear ${tab === 'register' ? 'bg-swiss-black text-swiss-white' : 'bg-swiss-white text-swiss-black hover:bg-swiss-red hover:text-swiss-white border-l-2 border-swiss-black'}`}
               onClick={() => setTab('register')}
             >
               CREATE
             </button>
          </div>

          <div className="relative text-left">
            {tab === 'login' ? (
              <form onSubmit={handleLogin} className="flex flex-col gap-8 font-medium">
                <div className="relative">
                   <label className="mb-2 block uppercase text-swiss-black font-bold text-xs tracking-widest pl-2 border-l-4 border-swiss-red">UUID IDENTIFIER</label>
                   <input 
                     type="text" 
                     value={userId} 
                     onChange={e => setUserId(e.target.value)} 
                     className="w-full bg-transparent border-b-4 border-swiss-black px-0 py-4 text-swiss-black text-xl rounded-none focus:outline-none focus:border-swiss-red transition-colors placeholder:text-[#999] font-medium"
                     required 
                   />
                </div>
                
                <button type="submit" disabled={loading} className="w-full mt-4 bg-swiss-black text-swiss-white px-6 py-6 font-bold uppercase text-lg tracking-widest border-2 border-swiss-black hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150 ease-linear rounded-none disabled:opacity-50">
                  {loading ? "SEARCHING..." : "AUTHENTICATE"}
                </button>
              </form>
            ) : (
              <form onSubmit={handleRegister} className="flex flex-col gap-8 font-medium">
                
                <div className="relative">
                  <label className="mb-2 block uppercase text-swiss-black font-bold text-xs tracking-widest pl-2 border-l-4 border-swiss-red">NAME</label>
                  <input type="text" value={name} onChange={e => setName(e.target.value)} className="w-full bg-transparent border-b-4 border-swiss-black px-0 py-4 text-swiss-black text-xl rounded-none focus:outline-none focus:border-swiss-red transition-colors placeholder:text-[#999]" required />
                </div>
                
                <div className="relative">
                  <label className="mb-2 block uppercase text-swiss-black font-bold text-xs tracking-widest pl-2 border-l-4 border-swiss-red">EMAIL</label>
                  <input type="email" value={email} onChange={e => setEmail(e.target.value)} className="w-full bg-transparent border-b-4 border-swiss-black px-0 py-4 text-swiss-black text-xl rounded-none focus:outline-none focus:border-swiss-red transition-colors placeholder:text-[#999]" required />
                </div>
                
                <div className="grid grid-cols-1 sm:grid-cols-2 gap-8">
                  <div>
                    <label className="mb-2 block uppercase text-swiss-black font-bold text-xs tracking-widest pl-2 border-l-4 border-swiss-black">PHONE</label>
                    <input type="text" value={phone} onChange={e => setPhone(e.target.value)} className="w-full bg-transparent border-b-4 border-swiss-black px-0 py-4 text-swiss-black text-lg rounded-none focus:outline-none focus:border-swiss-red transition-colors placeholder:text-[#999]" />
                  </div>
                  <div>
                    <label className="mb-2 block uppercase text-swiss-black font-bold text-xs tracking-widest pl-2 border-l-4 border-swiss-black">DEFAULT NODE</label>
                    <select value={prefMethod} onChange={e => setPrefMethod(e.target.value)} className="w-full bg-transparent border-b-4 border-swiss-black px-0 py-4 text-swiss-black text-lg rounded-none focus:outline-none focus:border-swiss-red transition-colors appearance-none cursor-pointer">
                      <option value="">AUTO.SELECT</option>
                      <option value="UPI">UPI PROTOCOL</option>
                      <option value="Credit Card">CREDIT_VEC</option>
                      <option value="Debit Card">DEBIT_VEC</option>
                      <option value="Wallet">VAULT</option>
                      <option value="Net Banking">BANKING</option>
                    </select>
                  </div>
                </div>

                <button type="submit" disabled={loading} className="w-full mt-4 bg-swiss-black text-swiss-white px-6 py-6 font-bold uppercase text-lg tracking-widest border-2 border-swiss-black hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150 ease-linear rounded-none disabled:opacity-50">
                  {loading ? "INITIALIZING..." : "REGISTER DATA"}
                </button>
              </form>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
