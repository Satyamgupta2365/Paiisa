import React from 'react';
import { useNavigate } from 'react-router-dom';

const SwissButton = ({ children, onClick, variant = 'primary', className = '' }) => {
  const base = "inline-flex items-center justify-center font-bold uppercase tracking-widest text-sm transition-colors duration-150 ease-linear h-16 px-12 border-2 border-swiss-black rounded-none";
  let variants = {
    primary: "bg-swiss-black text-swiss-white hover:bg-swiss-red hover:border-swiss-red",
    secondary: "bg-swiss-white text-swiss-black hover:bg-swiss-black hover:text-swiss-white",
    outline: "bg-transparent text-swiss-black hover:bg-swiss-black hover:text-swiss-white"
  };
  return (
    <button onClick={onClick} className={`${base} ${variants[variant]} ${className}`}>
      {children}
    </button>
  );
};

const SectionHeader = ({ index, title, subtitle }) => (
  <div className="w-full border-t-4 border-b-4 border-swiss-black py-4 mb-20 flex justify-between items-center text-xs font-bold uppercase tracking-widest">
     <span>{index}. SYSTEM</span>
     <span className="text-swiss-red hidden md:inline-block">{title} / {subtitle}</span>
  </div>
);

export default function DemoOne() {
  const navigate = useNavigate();

  return (
    <div className="relative w-full bg-swiss-white text-swiss-black font-inter selection:bg-swiss-red selection:text-swiss-white min-h-screen">
      
      {/* Grid Pattern Background */}
      <div className="fixed inset-0 pointer-events-none z-0 bg-swiss-grid mix-blend-multiply opacity-50" />

      <main className="relative z-10 w-full flex flex-col pt-32 pb-48 px-8 xl:px-16 max-w-[1920px] mx-auto">
        
        {/* HERO SECTION */}
        <SectionHeader index="01" title="PAISA" subtitle="THE RBI ACCOUNT AGGREGATOR GATEWAY" />

        <div className="grid grid-cols-1 lg:grid-cols-12 gap-16 items-start mb-48">
          <div className="col-span-1 lg:col-span-8">
            <h1 className="font-black text-[5rem] sm:text-[7rem] lg:text-[10rem] xl:text-[12rem] leading-[0.85] uppercase tracking-tighter mix-blend-multiply mb-12">
              INTENT-DRIVEN<br/>
              <span className="text-swiss-red">PAYMENTS.</span>
            </h1>

            <p className="font-medium text-2xl md:text-3xl max-w-4xl leading-tight mb-16 border-l-8 border-swiss-black pl-8 ml-2">
              Smart Flow Architecture intersecting the RBI AA Framework with Multi-Agent Routing via AWS Bedrock & Pine Labs.
            </p>

            <div className="flex flex-col sm:flex-row gap-6">
              <SwissButton onClick={() => navigate('/login')}>LINK RBI AA</SwissButton>
              <SwissButton onClick={() => window.scrollTo({top: 1000, behavior: 'smooth'})} variant="outline">READ MANIFESTO</SwissButton>
            </div>
          </div>

          <div className="col-span-1 lg:col-span-4 flex flex-col gap-8 h-full">
            <div className="border-4 border-swiss-black bg-swiss-gray p-8 aspect-square relative overflow-hidden group">
               <div className="absolute inset-0 bg-swiss-dots opacity-50 transition-opacity duration-300 group-hover:opacity-100" />
               <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[80%] h-[80%] bg-swiss-black rounded-full transition-transform duration-500 group-hover:bg-swiss-red group-hover:scale-[0.6] flex items-center justify-center">
                 <span className="text-swiss-white font-black text-4xl text-center uppercase tracking-widest opacity-0 group-hover:opacity-100 transition-opacity delay-150">GROQ<br/>AWS</span>
               </div>
            </div>
            
            <div className="border-4 border-swiss-black bg-swiss-red p-8 text-swiss-white flex flex-col justify-end min-h-[250px] transition-colors duration-300 hover:bg-swiss-black shadow-[16px_16px_0px_0px_#000]">
               <span className="font-black text-6xl uppercase tracking-tighter">PINE</span>
               <span className="font-bold text-xs uppercase tracking-widest mt-4 opacity-80">PLURAL API / OAUTH</span>
            </div>
          </div>
        </div>

        {/* CORE FEATURES GRID */}
        <SectionHeader index="02" title="INFRASTRUCTURE" subtitle="ROUTING & INTELLIGENCE" />
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 border-t-4 border-l-4 border-swiss-black mb-48">
           
           <div className="border-b-4 border-r-4 border-swiss-black p-12 bg-swiss-white hover:bg-swiss-gray transition-colors group">
              <div className="text-swiss-red font-bold text-sm uppercase tracking-widest mb-8">COMPUTE PIPELINE</div>
              <h3 className="font-black text-5xl uppercase tracking-tighter mb-6">AI SMART ROUTING</h3>
              <p className="font-medium text-lg leading-relaxed text-[#333]">Extracts financial signals from raw statements using Llama 3 (Groq) with AWS Bedrock Nova Lite fallback. Recommends optimal payment instruments instantly based on liquidity.</p>
           </div>

           <div className="border-b-4 border-r-4 border-swiss-black p-12 bg-swiss-white hover:bg-swiss-black hover:text-swiss-white transition-colors group">
              <div className="text-swiss-red font-bold text-sm uppercase tracking-widest mb-8">DATA ISOLATION</div>
              <h3 className="font-black text-5xl uppercase tracking-tighter mb-6">AA SIMULATION</h3>
              <p className="font-medium text-lg leading-relaxed text-inherit opacity-80">Mimics the RBI Account Aggregator consent-and-fetch flow — pulling snapshots while maintaining strict data compliance. Zero raw credential exposure.</p>
           </div>

           <div className="border-b-4 border-r-4 border-swiss-black p-12 bg-swiss-gray relative overflow-hidden group">
              <div className="absolute inset-0 bg-swiss-diagonal opacity-50 transition-opacity group-hover:opacity-10" />
              <div className="relative z-10 text-swiss-black h-full flex flex-col justify-end">
                 <div className="text-swiss-red font-bold text-sm uppercase tracking-widest mb-8">RECORD KEEPING</div>
                 <h3 className="font-black text-7xl uppercase tracking-tighter leading-none mb-4">IMMUTABLE</h3>
                 <p className="font-bold text-xs uppercase tracking-widest mt-4">Append-only PG Logs / Asyncpg</p>
              </div>
           </div>
        </div>

        {/* ARCHITECTURE FLOW */}
        <SectionHeader index="03" title="ARCHITECTURE" subtitle="TRANSACTION LIFECYCLE" />
        
        <div className="border-4 border-swiss-black p-16 bg-swiss-white mb-48 shadow-[24px_24px_0px_0px_#FF3000]">
           <h2 className="font-black text-6xl uppercase tracking-tighter mb-12">THE PAISA PROTOCOL</h2>
           <div className="flex flex-col md:flex-row justify-between items-center gap-8">
             <div className="flex-1 text-center border-2 border-swiss-black p-8 px-4 bg-swiss-gray">
               <span className="font-bold uppercase tracking-widest text-swiss-red text-sm block mb-4">STEP 01</span>
               <span className="font-black text-2xl uppercase">RBI AA AUTH</span>
               <p className="text-sm mt-4 font-medium">User consent initiated. 128-bit encrypted handshake.</p>
             </div>
             <div className="font-black text-4xl hidden md:block">→</div>
             <div className="flex-1 text-center border-2 border-swiss-black p-8 px-4 bg-swiss-black text-swiss-white">
               <span className="font-bold uppercase tracking-widest text-swiss-red text-sm block mb-4">STEP 02</span>
               <span className="font-black text-2xl uppercase">LLM PARSING</span>
               <p className="text-sm mt-4 font-medium opacity-80">Groq / AWS Bedrock extracts balance & limits.</p>
             </div>
             <div className="font-black text-4xl hidden md:block">→</div>
             <div className="flex-1 text-center border-2 border-swiss-black p-8 px-4 bg-swiss-white border-b-8 border-swiss-red">
               <span className="font-bold uppercase tracking-widest text-swiss-red text-sm block mb-4">STEP 03</span>
               <span className="font-black text-2xl uppercase">PINE LABS UAT</span>
               <p className="text-sm mt-4 font-medium">OAuth bearer token request & Plural order creation.</p>
             </div>
           </div>
        </div>

        {/* PRICING & TIERS */}
        <SectionHeader index="04" title="ECONOMICS" subtitle="ENTERPRISE LICENSING" />
        
        <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-48">
          <div className="border-4 border-swiss-black p-12 bg-swiss-white flex flex-col justify-between">
            <div>
              <h3 className="font-black text-4xl uppercase tracking-tighter mb-2">DEVELOPER / SANDBOX</h3>
              <p className="text-xl font-bold text-swiss-red mb-8">FREE / OSS</p>
              <ul className="space-y-4 mb-12 font-medium">
                <li className="flex items-center gap-4"><span className="text-swiss-red leading-none">■</span> SQLite Fallback Engine</li>
                <li className="flex items-center gap-4"><span className="text-swiss-red leading-none">■</span> Mock Local Account Aggregator</li>
                <li className="flex items-center gap-4"><span className="text-swiss-red leading-none">■</span> Pine Labs Plural UAT Sandbox</li>
                <li className="flex items-center gap-4"><span className="text-swiss-red leading-none">■</span> 100 LLM Inferences / month</li>
              </ul>
            </div>
            <SwissButton variant="outline" className="w-full">CLONE REPO</SwissButton>
          </div>

          <div className="border-4 border-swiss-black p-12 bg-swiss-black text-swiss-white flex flex-col justify-between shadow-[24px_24px_0px_0px_#FF3000]">
            <div>
              <h3 className="font-black text-4xl uppercase tracking-tighter mb-2">ENTERPRISE NODE</h3>
              <p className="text-xl font-bold text-swiss-red mb-8">CUSTOM / SLA</p>
              <ul className="space-y-4 mb-12 font-medium opacity-90">
                <li className="flex items-center gap-4"><span className="text-swiss-red shadow-[0_0_10px_#FF3000]">■</span> Async PostgreSQL Cluster</li>
                <li className="flex items-center gap-4"><span className="text-swiss-red shadow-[0_0_10px_#FF3000]">■</span> Live RBI AA Production Keys</li>
                <li className="flex items-center gap-4"><span className="text-swiss-red shadow-[0_0_10px_#FF3000]">■</span> Pine Labs Plural Production MID</li>
                <li className="flex items-center gap-4"><span className="text-swiss-red shadow-[0_0_10px_#FF3000]">■</span> Unlimited AWS Bedrock Fallback</li>
              </ul>
            </div>
            <SwissButton variant="primary" className="w-full bg-swiss-red hover:bg-swiss-white hover:text-swiss-black border-swiss-red">CONTACT SALES</SwissButton>
          </div>
        </div>

        {/* CALL TO ACTION */}
        <div className="border-4 border-swiss-black bg-swiss-gray p-16 text-center">
           <h2 className="font-black text-6xl md:text-8xl uppercase tracking-tighter mb-8">INITIATE SEQUENCE.</h2>
           <p className="font-medium text-2xl mb-12">Experience the intelligence overlay for modern payments.</p>
           <SwissButton onClick={() => navigate('/login')} className="h-20 px-16 text-xl">LAUNCH TERMINAL</SwissButton>
        </div>

      </main>
      
    </div>
  );
}
