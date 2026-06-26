import React, { useState, useEffect } from 'react';
import { useTap } from '../hooks/useTap';
import { useUser } from '../context/UserContext';
import Spinner from '../components/Spinner';
import { Link } from 'react-router-dom';

const DEMO_AGENTS = ['claude-v3', 'gemini-1.5', 'gpt-4o', 'paisa-autopilot', 'mcp-external-bot'];
const DEMO_CATEGORIES = ['food', 'transport', 'shopping', 'utilities', 'travel', 'healthcare'];

export default function AgentPage() {
  const { user } = useUser();
  const { rules, logs, loading, fetchRules, saveRules, simulatePing, fetchLogs } = useTap(user?.id);

  const [dailyCap, setDailyCap] = useState('5000');
  const [allowlist, setAllowlist] = useState('food, transport, utilities');
  const [blacklist, setBlacklist] = useState('');
  const [otpThreshold, setOtpThreshold] = useState('1000');

  useEffect(() => {
    if (user?.id) {
      fetchRules();
      fetchLogs();
    }
  }, [user?.id]);

  // Sync form with fetched rules
  useEffect(() => {
    if (rules) {
      setDailyCap(String(rules.daily_cap));
      setAllowlist(rules.category_allowlist?.join(', ') || '');
      setBlacklist(rules.merchant_blacklist?.join(', ') || '');
      setOtpThreshold(String(rules.require_otp_above));
    }
  }, [rules]);

  const handleSave = (e) => {
    e.preventDefault();
    saveRules({
      daily_cap: parseFloat(dailyCap),
      category_allowlist: allowlist.split(',').map(s => s.trim()).filter(Boolean),
      merchant_blacklist: blacklist.split(',').map(s => s.trim()).filter(Boolean),
      require_otp_above: parseFloat(otpThreshold),
    });
  };

  const handleSimulate = async () => {
    const agent = DEMO_AGENTS[Math.floor(Math.random() * DEMO_AGENTS.length)];
    const amount = Math.floor(Math.random() * 12000) + 300;
    const cat = DEMO_CATEGORIES[Math.floor(Math.random() * DEMO_CATEGORIES.length)];
    const result = await simulatePing(agent, amount, cat);
    // Refresh logs
    fetchLogs();
  };

  if (!user) {
    return (
      <div className="flex flex-col items-start justify-center min-h-[60vh] w-full max-w-4xl mx-auto border-l-8 border-swiss-red pl-12">
        <h2 className="font-black text-7xl md:text-9xl text-swiss-black mb-8 uppercase leading-[0.85] tracking-tighter">TAP<br/>LOCKED.</h2>
        <p className="font-bold text-lg uppercase tracking-widest mb-16 text-[#666] border-b-2 border-swiss-black pb-4">Authentication required to manage your AI agent protocol</p>
        <Link to="/login" className="inline-flex border-4 border-swiss-black bg-swiss-black text-swiss-white px-12 py-6 font-bold uppercase text-lg tracking-widest hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150">
          LINK BANK
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full text-swiss-black font-inter relative z-10 max-w-[1920px] mx-auto min-h-[80vh]">

      {/* Header */}
      <div className="mb-24 flex flex-col md:flex-row justify-between items-start md:items-end border-b-4 border-swiss-black pb-12">
        <div>
           <div className="inline-block px-4 py-2 border-2 border-swiss-black bg-swiss-white font-bold uppercase text-xs tracking-widest mb-6">
              PILLAR 05 // TRUSTED AGENT PROTOCOL // MCP-COMPATIBLE
           </div>
           <h1 className="font-black text-[5rem] md:text-[8rem] uppercase tracking-tighter leading-[0.8] max-w-4xl">
             TAP SERVER.
           </h1>
        </div>
        <p className="mt-8 md:mt-0 font-medium text-lg max-w-lg text-[#444] border-l-4 border-swiss-black pl-6 leading-snug">
          When Claude, Gemini, or any AI agent wants to spend your money — they hit this endpoint first.
          PAISA evaluates their request against your financial constitution in under 100ms.
        </p>
      </div>

      {loading && !rules ? <Spinner /> : (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-32 items-start">
          
          {/* Rules Constitution */}
          <div className="bg-swiss-white border-4 border-swiss-black p-12 relative group">
            <div className="absolute inset-0 bg-swiss-dots opacity-10 transition-opacity group-hover:opacity-5 pointer-events-none" />
            
            <h2 className="relative z-10 font-black text-4xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-12 flex justify-between items-end">
              CONSTITUTION
              <span className="font-bold text-xs tracking-widest text-swiss-red">FINANCIAL DNS</span>
            </h2>

            <form onSubmit={handleSave} className="relative z-10 space-y-8">
              
              {[
                { label: 'MAX AUTO-CAP (₹/DAY)', value: dailyCap, setter: setDailyCap, type: 'number', desc: 'AI cannot spend more than this per day without explicit approval' },
                { label: 'CATEGORY ALLOWLIST (CSV)', value: allowlist, setter: setAllowlist, type: 'text', desc: 'Only allow AI to spend in these categories. Leave blank for all.' },
                { label: 'MERCHANT BLACKLIST (CSV)', value: blacklist, setter: setBlacklist, type: 'text', desc: 'Block specific merchants from AI spending entirely' },
                { label: 'OTP REQUIRED ABOVE (₹)', value: otpThreshold, setter: setOtpThreshold, type: 'number', desc: 'Biometric confirmation for any AI transaction above this amount' },
              ].map((field, idx) => (
                <div key={idx} className="flex border-2 border-swiss-black flex-col">
                  <div className="bg-swiss-black text-swiss-white px-6 py-3 font-bold text-xs uppercase tracking-widest flex justify-between">
                    <span>{field.label}</span>
                  </div>
                  <input
                    type={field.type}
                    value={field.value}
                    onChange={e => field.setter(e.target.value)}
                    className="flex-1 bg-transparent px-6 py-4 font-black text-2xl tracking-tighter outline-none focus:bg-swiss-red focus:text-swiss-white transition-colors border-none"
                    placeholder={field.type === 'number' ? '0' : 'enter values...'}
                  />
                  <div className="px-6 pb-3 font-medium text-xs text-[#666] uppercase tracking-widest border-t border-swiss-black pt-2">{field.desc}</div>
                </div>
              ))}

              <button type="submit" disabled={loading} className="w-full h-20 bg-swiss-black text-swiss-white font-bold text-lg uppercase tracking-widest border-4 border-swiss-black hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150 disabled:opacity-50">
                {loading ? 'ENFORCING...' : 'ENFORCE PROTOCOL'}
              </button>
            </form>
          </div>

          {/* Audit Log */}
          <div className="w-full">
            <div className="flex justify-between items-center border-b-4 border-swiss-black pb-4 mb-4">
              <h2 className="font-black text-4xl uppercase tracking-tighter">AUDIT LOG</h2>
              <button 
                onClick={handleSimulate} 
                className="font-bold text-xs uppercase tracking-widest px-6 py-3 border-2 border-swiss-black hover:bg-swiss-black hover:text-swiss-white transition-colors duration-150 bg-swiss-white"
              >
                SIMULATE AGENT PING
              </button>
            </div>
            
            <div className="border-4 border-swiss-black bg-swiss-black text-swiss-white overflow-hidden">
              {/* Table Header */}
              <div className="grid grid-cols-12 bg-[#111] text-[#666] font-bold text-xs uppercase tracking-widest px-6 py-4 border-b-2 border-[#333]">
                <span className="col-span-2">TXN.ID</span>
                <span className="col-span-3">AGENT</span>
                <span className="col-span-2 text-right">AMOUNT</span>
                <span className="col-span-2">CATEGORY</span>
                <span className="col-span-3 text-right">DECISION</span>
              </div>
              
              {logs.length === 0 ? (
                <div className="px-6 py-24 text-center font-black text-4xl uppercase tracking-tighter text-[#333]">
                  NO REQUESTS YET.<br/>
                  <span className="text-sm text-[#555] font-bold tracking-widest">SIMULATE A PING →</span>
                </div>
              ) : (
                <div className="max-h-[600px] overflow-y-auto">
                  {logs.map((log, idx) => (
                    <div key={log.id || idx} className={`grid grid-cols-12 items-center gap-2 px-6 py-5 border-b border-[#222] transition-colors hover:bg-[#111] group ${
                      log.decision === 'REJECTED' ? 'hover:bg-[#1a0000]' : ''
                    }`}>
                      <span className="col-span-2 font-bold text-[10px] opacity-40 group-hover:opacity-80 transition-opacity tracking-widest uppercase">
                        {String(log.id).split('-')[0].toUpperCase()}
                      </span>
                      <span className="col-span-3 font-black text-sm tracking-tighter truncate">{log.agent_id}</span>
                      <span className={`col-span-2 font-black text-lg text-right tracking-tighter ${log.decision === 'REJECTED' ? 'text-swiss-red' : ''}`}>
                        ₹{log.requested_amount?.toLocaleString('en-IN')}
                      </span>
                      <span className="col-span-2 font-bold text-[10px] uppercase tracking-widest text-[#666]">
                        {log.category || '—'}
                      </span>
                      <div className="col-span-3 text-right">
                        <span className={`inline-block border px-3 py-1 font-bold text-[10px] uppercase tracking-widest ${
                          log.decision === 'APPROVED' 
                            ? 'border-swiss-white text-swiss-white' 
                            : 'border-swiss-red text-swiss-red'
                        }`}>
                          {log.decision}
                        </span>
                        <div className="text-[9px] text-[#444] mt-1 uppercase tracking-widest">{log.reason}</div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
            
            <div className="mt-4 font-bold text-xs tracking-widest uppercase text-[#666] border-t-2 border-swiss-black pt-4">
              EVERY LOG IS IMMUTABLE. USER CAN DOWNLOAD FULL AUDIT TRAIL VIA DATA EXPORT.
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
