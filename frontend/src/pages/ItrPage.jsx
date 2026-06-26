import React, { useState, useEffect } from 'react';
import { useUser } from '../context/UserContext';
import { useItr } from '../hooks/useItr';
import Spinner from '../components/Spinner';
import toast from 'react-hot-toast';
import { Link } from 'react-router-dom';

const fmt = (n) => `₹${Number(n || 0).toLocaleString('en-IN')}`;

export default function ItrPage() {
  const { user } = useUser();
  const { report, advisory, loading, advisoryLoading, fetchItrReport, fetchAdvisory } = useItr(user?.id);

  // Form states for manual/custom tuning
  const [otherIncome, setOtherIncome] = useState('0');
  const [deductions80c, setDeductions80c] = useState('150000');
  const [deductions80d, setDeductions80d] = useState('25000');
  const [applyPresumptive, setApplyPresumptive] = useState(true);

  // Fetch report on load
  useEffect(() => {
    if (user?.id) {
      fetchItrReport(0, 150000, 25000, true);
    }
  }, [user?.id, fetchItrReport]);

  const handleRecalculate = (e) => {
    e.preventDefault();
    fetchItrReport(
      parseFloat(otherIncome) || 0,
      parseFloat(deductions80c) || 0,
      parseFloat(deductions80d) || 0,
      applyPresumptive
    ).then((data) => {
      if (data && data.tax_comparison) {
        toast.success('TAX COMPUTATION UPDATED');
      }
    });
  };

  const handleGenerateAdvisory = () => {
    if (!report) return;
    fetchAdvisory(report.tax_comparison);
  };

  const handleFileItr = () => {
    const id = toast.loading('Initiating Tax Filing Protocol...');
    setTimeout(() => {
      toast.dismiss(id);
      toast.success('ITR-4 DRAFT GENERATED SUCCESSFULLY!');
      toast('XML Schema generated for e-filing portal.', {
        icon: '📄',
        style: {
          background: '#000',
          color: '#fff',
          border: '2px solid #000'
        }
      });
    }, 2000);
  };

  if (!user) {
    return (
      <div className="flex flex-col items-start justify-center min-h-[60vh] w-full max-w-4xl mx-auto border-l-8 border-swiss-red pl-12">
        <h2 className="font-black text-7xl md:text-9xl text-swiss-black mb-8 uppercase leading-[0.85] tracking-tighter">TAX<br/>LOCKED.</h2>
        <p className="font-bold text-lg uppercase tracking-widest mb-16 text-[#666] border-b-2 border-swiss-black pb-4">Authentication required to access tax return computations</p>
        <Link to="/login" className="inline-flex border-4 border-swiss-black bg-swiss-black text-swiss-white px-12 py-6 font-bold uppercase text-lg tracking-widest hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150">
          LINK BANK
        </Link>
      </div>
    );
  }

  const tax = report?.tax_comparison;
  const agg = report?.aggregated_data;

  return (
    <div className="w-full text-swiss-black font-inter relative z-10 max-w-[1920px] mx-auto min-h-[80vh]">
      
      {/* Masthead */}
      <div className="mb-16 border-b-4 border-swiss-black pb-10">
        <div className="inline-block px-4 py-2 border-2 border-swiss-black bg-swiss-white font-bold uppercase text-xs tracking-widest mb-6">
          PILLAR 04 // INCOME TAX RETURNS // PRESUMPTIVE DIGITAL MERCHANT FILING (ITR-4)
        </div>
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
          <h1 className="font-black text-[4.5rem] md:text-[7rem] xl:text-[8rem] uppercase tracking-tighter leading-[0.85]">
            ITR FILING<br/><span className="text-swiss-red">COMPLIANCE.</span>
          </h1>
          <p className="max-w-md font-medium text-lg text-[#444] border-l-4 border-swiss-black pl-6 leading-snug">
            Indian Income Tax Compliance. Synthesize business sales, operating expenses, and AI agent tech billing to draft ITR reports under the New or Old regime.
          </p>
        </div>
      </div>

      {loading && !report ? <Spinner /> : (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-32 items-start">
          
          {/* Column 1: Configurator */}
          <div className="lg:col-span-1 bg-swiss-white border-4 border-swiss-black p-8 relative">
            <h2 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-6">
              TAX Slab Settings
            </h2>
            <form onSubmit={handleRecalculate} className="space-y-6">
              
              <div className="flex border-2 border-swiss-black flex-col">
                <div className="bg-swiss-black text-swiss-white px-4 py-2 font-bold text-xs uppercase tracking-widest">
                  OTHER INCOME (₹)
                </div>
                <input
                  type="number"
                  value={otherIncome}
                  onChange={e => setOtherIncome(e.target.value)}
                  className="bg-transparent px-4 py-3 font-black text-xl outline-none"
                  placeholder="Interest, rent, etc."
                />
              </div>

              <div className="flex border-2 border-swiss-black flex-col">
                <div className="bg-swiss-black text-swiss-white px-4 py-2 font-bold text-xs uppercase tracking-widest">
                  SECTION 80C DEDUCTION (₹)
                </div>
                <input
                  type="number"
                  value={deductions80c}
                  onChange={e => setDeductions80c(e.target.value)}
                  className="bg-transparent px-4 py-3 font-black text-xl outline-none"
                  placeholder="Max ₹1,50,000 (PPF, ELSS)"
                />
              </div>

              <div className="flex border-2 border-swiss-black flex-col">
                <div className="bg-swiss-black text-swiss-white px-4 py-2 font-bold text-xs uppercase tracking-widest">
                  SECTION 80D DEDUCTION (₹)
                </div>
                <input
                  type="number"
                  value={deductions80d}
                  onChange={e => setDeductions80d(e.target.value)}
                  className="bg-transparent px-4 py-3 font-black text-xl outline-none"
                  placeholder="Max ₹25,000 (Health Insurance)"
                />
              </div>

              <div className="border-2 border-swiss-black p-4 bg-swiss-gray flex items-center justify-between">
                <div>
                  <span className="font-bold text-xs uppercase tracking-widest block">PRESUMPTIVE TAXATION</span>
                  <span className="text-[10px] text-[#666] font-medium uppercase tracking-widest">Section 44AD (6% digital profit)</span>
                </div>
                <input
                  type="checkbox"
                  checked={applyPresumptive}
                  onChange={e => setApplyPresumptive(e.target.checked)}
                  className="w-6 h-6 border-2 border-swiss-black bg-swiss-white cursor-pointer accent-swiss-red"
                />
              </div>

              <button type="submit" disabled={loading} className="w-full h-14 bg-swiss-black text-swiss-white font-bold uppercase tracking-widest border-4 border-swiss-black hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150">
                {loading ? 'RE-CALCULATING...' : 'APPLY PARAMETERS'}
              </button>
            </form>
          </div>

          {/* Column 2 & 3: Results */}
          <div className="lg:col-span-2 space-y-8">
            
            {/* Business Synthesis Card */}
            {agg && (
              <div className="border-4 border-swiss-black p-8 bg-swiss-white relative group overflow-hidden">
                <div className="absolute inset-0 bg-swiss-diagonal opacity-5 pointer-events-none" />
                <h2 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-6 flex justify-between items-end">
                  FINANCIAL LEDGER SYNTHESIS
                  <span className="font-bold text-xs tracking-widest text-swiss-red">LIVE MERGE</span>
                </h2>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                  <div className="border-2 border-swiss-black p-4 bg-swiss-white">
                    <span className="font-bold text-[9px] uppercase tracking-widest text-[#666] block">GROSS TURNOVER</span>
                    <span className="font-black text-2xl tracking-tighter">{fmt(agg.gross_revenue)}</span>
                    <span className="text-[9px] text-[#999] block font-bold mt-1 uppercase tracking-widest">BANK CREDIT SUMMARY</span>
                  </div>
                  <div className="border-2 border-swiss-black p-4 bg-swiss-white">
                    <span className="font-bold text-[9px] uppercase tracking-widest text-[#666] block">OPERATING DEBITS</span>
                    <span className="font-black text-2xl tracking-tighter text-swiss-red">{fmt(agg.operating_expenses)}</span>
                    <span className="text-[9px] text-[#999] block font-bold mt-1 uppercase tracking-widest">STATEMENT WITHDRAWALS</span>
                  </div>
                  <div className="border-2 border-swiss-black p-4 bg-swiss-white">
                    <span className="font-bold text-[9px] uppercase tracking-widest text-[#666] block">AI AGENT TECH EXPENSES</span>
                    <span className="font-black text-2xl tracking-tighter text-swiss-red">{fmt(agg.ai_agent_expenses)}</span>
                    <span className="text-[9px] text-[#999] block font-bold mt-1 uppercase tracking-widest">TAP SYSTEM APPROVED</span>
                  </div>
                </div>
                <div className="border-t-2 border-dashed border-swiss-black pt-4 flex justify-between items-center text-sm font-bold uppercase tracking-widest">
                  <span>Presumptive Profit Basis (6%): {fmt(tax?.declared_business_income)}</span>
                  <span>Normal Book Profit: {fmt(tax?.normal_profit)}</span>
                </div>
              </div>
            )}

            {/* Tax regime comparison */}
            {tax && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                
                {/* New Tax Regime Slab */}
                <div className="border-4 border-swiss-black p-6 bg-swiss-white relative">
                  <div className="absolute top-0 right-0 bg-swiss-black text-swiss-white px-3 py-1 font-bold text-[9px] uppercase tracking-widest">
                    FY 2025-26 (NEW)
                  </div>
                  <h3 className="font-black text-xl uppercase tracking-tighter border-b-2 border-swiss-black pb-2 mb-4">
                    NEW REGIME SLABS
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between border-b border-swiss-gray pb-2 text-sm font-semibold">
                      <span>TAXABLE INCOME</span>
                      <span className="font-black">{fmt(tax.new_regime.taxable_income)}</span>
                    </div>
                    <div className="flex justify-between border-b border-swiss-gray pb-2 text-sm font-semibold">
                      <span>RAW SLAB TAX</span>
                      <span className="font-black">{fmt(tax.new_regime.raw_tax)}</span>
                    </div>
                    <div className="flex justify-between border-b border-swiss-gray pb-2 text-sm font-semibold">
                      <span>HEALTH & ED CESS (4%)</span>
                      <span className="font-black">{fmt(tax.new_regime.cess)}</span>
                    </div>
                    <div className="flex justify-between pt-2 text-lg font-black uppercase tracking-tight">
                      <span>TOTAL TAX DUE</span>
                      <span className="text-swiss-red">{fmt(tax.new_regime.total_tax)}</span>
                    </div>
                  </div>
                </div>

                {/* Old Tax Regime Slab */}
                <div className="border-4 border-swiss-black p-6 bg-swiss-white relative">
                  <div className="absolute top-0 right-0 border-l border-b border-swiss-black bg-swiss-gray text-swiss-black px-3 py-1 font-bold text-[9px] uppercase tracking-widest">
                    OLD REGIME (OPTIONAL)
                  </div>
                  <h3 className="font-black text-xl uppercase tracking-tighter border-b-2 border-swiss-black pb-2 mb-4">
                    OLD REGIME SLABS
                  </h3>
                  <div className="space-y-3">
                    <div className="flex justify-between border-b border-swiss-gray pb-2 text-sm font-semibold">
                      <span>CHAPTER VI-A DEDUCTIONS</span>
                      <span className="font-black text-swiss-red">-{fmt(tax.old_regime.deductions_applied)}</span>
                    </div>
                    <div className="flex justify-between border-b border-swiss-gray pb-2 text-sm font-semibold">
                      <span>TAXABLE INCOME</span>
                      <span className="font-black">{fmt(tax.old_regime.taxable_income)}</span>
                    </div>
                    <div className="flex justify-between border-b border-swiss-gray pb-2 text-sm font-semibold">
                      <span>RAW SLAB TAX</span>
                      <span className="font-black">{fmt(tax.old_regime.raw_tax)}</span>
                    </div>
                    <div className="flex justify-between pt-2 text-lg font-black uppercase tracking-tight">
                      <span>TOTAL TAX DUE</span>
                      <span className="text-swiss-red">{fmt(tax.old_regime.total_tax)}</span>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Recommendation & Advice */}
            {tax && (
              <div className="border-4 border-swiss-black p-8 bg-swiss-black text-swiss-white relative">
                <div className="font-bold text-xs uppercase tracking-widest opacity-60 mb-2">OPTIMAL FILING PATHWAY</div>
                <h3 className="font-black text-4xl uppercase tracking-tighter mb-4 text-swiss-red">
                  USE {tax.recommendation.optimal_regime.toUpperCase()} REGIME
                </h3>
                <p className="font-medium text-lg leading-relaxed mb-6 border-l-4 border-swiss-red pl-4">
                  {tax.recommendation.guidance}
                </p>
                <div className="flex flex-col sm:flex-row gap-4 border-t-2 border-swiss-red pt-6">
                  <button onClick={handleGenerateAdvisory} disabled={advisoryLoading} className="flex-1 h-14 border-4 border-swiss-red bg-swiss-red text-swiss-white hover:bg-swiss-white hover:text-swiss-black hover:border-swiss-white transition-colors font-bold uppercase text-xs tracking-widest">
                    {advisoryLoading ? 'GENERATING CA VERDICT...' : 'RUN GEMINI CA REVIEW'}
                  </button>
                  <button onClick={handleFileItr} className="flex-1 h-14 border-4 border-swiss-white bg-swiss-white text-swiss-black hover:bg-swiss-black hover:text-swiss-white transition-colors font-bold uppercase text-xs tracking-widest">
                    FILE DRAFT RETURN (ITR-4)
                  </button>
                </div>
              </div>
            )}

            {/* Gemini Advisory Verdict */}
            {(advisoryLoading || advisory) && (
              <div className="border-4 border-swiss-black p-8 bg-swiss-white">
                <div className="font-black text-xs uppercase tracking-widest mb-6 border-b-4 border-swiss-black pb-4 flex items-center gap-4">
                  <span className="w-7 h-7 bg-swiss-black text-swiss-white flex items-center justify-center text-xs font-black">AI</span>
                  GEMINI ITR ADVISORY REPORT
                  <span className="ml-auto text-[#999] font-bold text-[9px]">paisa-itr specialist agent</span>
                </div>
                {advisoryLoading ? (
                  <div className="py-12 flex justify-center"><Spinner /></div>
                ) : (
                  <div className="prose max-w-none font-medium text-sm text-[#333] leading-relaxed space-y-4">
                    {advisory.split('\n').map((para, index) => {
                      if (para.startsWith('###')) {
                        return <h4 key={index} className="font-black text-lg uppercase tracking-tight mt-6 mb-2">{para.replace('###', '')}</h4>;
                      }
                      if (para.startsWith('*') || para.startsWith('-')) {
                        return <li key={index} className="ml-4 list-disc">{para.replace(/^[\*\-]\s*/, '')}</li>;
                      }
                      return <p key={index}>{para}</p>;
                    })}
                  </div>
                )}
              </div>
            )}

          </div>
        </div>
      )}
    </div>
  );
}
