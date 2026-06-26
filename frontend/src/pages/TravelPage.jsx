import React, { useState, useRef, useEffect, useCallback } from 'react';
import { analyzeStatement, analyzeStatementFile, analyzeStatementDemo, getStatementHistory, getStatementById } from '../services/api';
import Spinner from '../components/Spinner';
import toast from 'react-hot-toast';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer, Cell, PieChart, Pie, Legend,
} from 'recharts';

// ── Colour helpers ─────────────────────────────────────────────────────────────
const INCOME_COLORS  = ['#000000', '#333333', '#555555', '#888888'];
const EXPENSE_COLORS = ['#FF3000', '#FF6633', '#FF9966', '#FFCC99', '#FFE5CC'];
const HEALTH_COLOR   = { EXCELLENT: '#000', GOOD: '#000', FAIR: '#b45309', POOR: '#FF3000' };
const VERDICT_STYLE  = { ELIGIBLE: 'bg-swiss-black text-swiss-white', INELIGIBLE: 'bg-swiss-red text-swiss-white', REVIEW: 'bg-amber-500 text-swiss-white' };

const fmt = (n) => `₹${Number(n).toLocaleString('en-IN')}`;

// ── Custom Tooltip ─────────────────────────────────────────────────────────────
const ChartTip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div className="border-4 border-swiss-black bg-swiss-white px-5 py-3 shadow-[4px_4px_0_#000]">
      <p className="font-black text-xs uppercase tracking-widest mb-1">{label}</p>
      {payload.map((p, i) => (
        <p key={i} className="font-black text-xl" style={{ color: p.color }}>{fmt(p.value)}</p>
      ))}
    </div>
  );
};

// ── Main Component ─────────────────────────────────────────────────────────────
export default function MerchantAnalyzerPage() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading]   = useState(false);
  const [companyName, setCompanyName] = useState('');
  const [statementText, setStatementText] = useState('');
  const [file, setFile]         = useState(null);
  const [activeView, setActiveView] = useState('overview'); // overview | income | expense | trend | history
  const [history, setHistory]   = useState([]);
  const [historyLoading, setHistoryLoading] = useState(false);
  const fileRef = useRef();

  // Load history whenever tab opens
  const loadHistory = useCallback(async () => {
    setHistoryLoading(true);
    try {
      const res = await getStatementHistory();
      setHistory(res.data);
    } catch { /* silently ignore if no history yet */ }
    finally { setHistoryLoading(false); }
  }, []);

  useEffect(() => { loadHistory(); }, [loadHistory]);

  const run = async (fn) => {
    setLoading(true);
    try {
      const res = await fn();
      setAnalysis(res.data);
      toast.success('GROQ AI ANALYSIS COMPLETE');
    } catch (e) {
      toast.error('ANALYSIS FAILED — CHECK BACKEND');
    } finally {
      setLoading(false);
    }
  };

  const handleText    = () => run(() => analyzeStatement(statementText, companyName));
  const handleFile    = () => {
    const fd = new FormData();
    fd.append('file', file);
    fd.append('company_name', companyName);
    run(() => analyzeStatementFile(fd));
  };
  const handleDemo    = () => run(() => analyzeStatementDemo(companyName || 'My Business'));

  const a = analysis;

  return (
    <div className="w-full text-swiss-black font-inter relative z-10 max-w-[1920px] mx-auto">

      {/* ══ MASTHEAD ══════════════════════════════════════════════════════ */}
      <div className="mb-12 border-b-4 border-swiss-black pb-10">
        <div className="inline-block px-4 py-2 border-2 border-swiss-black font-bold uppercase text-xs tracking-widest mb-5">
          GROQ AI // llama-3.3-70b-versatile // MERCHANT FINANCIAL INTELLIGENCE
        </div>
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
          <h1 className="font-black text-[4rem] md:text-[7rem] xl:text-[8.5rem] uppercase tracking-tighter leading-[0.85]">
            BANK STMT<br/><span className="text-swiss-red">ANALYZER.</span>
          </h1>
          <p className="max-w-sm font-medium text-lg text-[#444] border-l-4 border-swiss-black pl-5 leading-snug">
            Upload your company bank statement. Groq AI reads every transaction, categorises your cash flow, scores your financial health, and tells you exactly what credit you qualify for.
          </p>
        </div>
      </div>

      {/* ══ INPUT PANEL ═══════════════════════════════════════════════════ */}
      {!analysis && (
        <>
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">

            {/* Left: text paste */}
            <div className="border-4 border-swiss-black bg-swiss-white p-10">
              <h2 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8">
                PASTE STATEMENT
              </h2>

              {/* Company name */}
              <div className="border-2 border-swiss-black mb-5">
                <div className="bg-swiss-black text-swiss-white px-5 py-2 font-bold text-xs uppercase tracking-widest">YOUR COMPANY NAME</div>
                <input
                  type="text" value={companyName} onChange={e => setCompanyName(e.target.value)}
                  className="w-full px-5 py-3 font-black text-xl outline-none bg-transparent"
                  placeholder="e.g. Satyam Enterprises"
                />
              </div>

              {/* Statement text */}
              <div className="border-2 border-swiss-black mb-6">
                <div className="bg-swiss-black text-swiss-white px-5 py-2 font-bold text-xs uppercase tracking-widest flex justify-between">
                  <span>BANK STATEMENT TEXT</span>
                  <span className="opacity-50">CSV / TEXT FORMAT</span>
                </div>
                <textarea
                  rows={10}
                  value={statementText}
                  onChange={e => setStatementText(e.target.value)}
                  placeholder={`Date,Description,Credit,Debit,Balance\n01/05/2026,Payment from Client,43126.54,,51317.65\n05/05/2026,Operating Expenses,-,15000.00,36317.65\n10/05/2026,Vendor Payment,-,3311.35,33006.30...`}
                  className="w-full px-5 py-3 font-medium text-xs font-mono outline-none bg-transparent resize-none text-[#333]"
                />
              </div>

              <button
                disabled={loading || !statementText}
                onClick={handleText}
                className="w-full h-14 bg-swiss-black text-swiss-white font-black uppercase tracking-widest border-4 border-swiss-black hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150 disabled:opacity-40 mb-4"
              >
                {loading ? 'GROQ AI ANALYSING...' : 'ANALYSE STATEMENT'}
              </button>
            </div>

            {/* Right: file upload + demo */}
            <div className="flex flex-col gap-6">
              {/* File upload */}
              <div className="border-4 border-swiss-black p-10 bg-swiss-white flex-1">
                <h2 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8">
                  UPLOAD FILE
                </h2>
                <div
                  onClick={() => fileRef.current?.click()}
                  className="border-4 border-dashed border-swiss-black p-10 cursor-pointer hover:bg-swiss-gray transition-colors text-center mb-6"
                >
                  <input ref={fileRef} type="file" accept=".txt,.csv,.pdf,.xlsx,.xls" className="hidden"
                    onChange={e => setFile(e.target.files[0])} />
                  <div className="font-black text-3xl text-[#ccc] mb-3">↑</div>
                  <div className="font-bold uppercase text-sm tracking-widest">
                    {file ? `✓ ${file.name}` : 'CLICK OR DRAG FILE HERE'}
                  </div>
                  <div className="font-medium text-xs text-[#999] mt-2 uppercase tracking-widest">PDF · EXCEL (.xlsx/.xls) · CSV · TXT</div>
                </div>
                {/* Company name for file upload too */}
                <div className="border-2 border-swiss-black mb-5">
                  <div className="bg-swiss-black text-swiss-white px-5 py-2 font-bold text-xs uppercase tracking-widest">COMPANY NAME</div>
                  <input type="text" value={companyName} onChange={e => setCompanyName(e.target.value)}
                    className="w-full px-5 py-3 font-black text-xl outline-none bg-transparent" />
                </div>
                <button
                  disabled={loading || !file}
                  onClick={handleFile}
                  className="w-full h-14 bg-swiss-black text-swiss-white font-black uppercase tracking-widest border-4 border-swiss-black hover:bg-swiss-red hover:border-swiss-red transition-colors disabled:opacity-40"
                >
                  {loading ? 'PROCESSING...' : 'UPLOAD & ANALYSE'}
                </button>
              </div>

              {/* Demo button */}
              <div className="border-4 border-swiss-black p-8 bg-swiss-gray">
                <div className="font-black text-base uppercase tracking-tighter mb-2">DEMO: INSTANT AI ANALYSIS</div>
                <p className="font-medium text-sm text-[#666] mb-5">
                  No bank statement? Enter your company name above then click below — Groq AI generates a realistic financial analysis for <strong>{companyName || 'Satyam'}</strong> instantly based on actual verified transaction data.
                </p>
                <button
                  disabled={loading}
                  onClick={handleDemo}
                  className="w-full h-12 bg-swiss-red text-swiss-white font-black uppercase tracking-widest border-4 border-swiss-red hover:bg-swiss-black hover:border-swiss-black transition-colors disabled:opacity-40"
                >
                  {loading ? 'GENERATING...' : `DEMO: ANALYSE ${(companyName || 'SATYAM').toUpperCase()}`}
                </button>
              </div>
            </div>
          </div>
          
          {/* Main Page History View */}
          <div className="border-4 border-swiss-black bg-swiss-white p-8 mb-16">
            <h3 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8">
              SAVED ANALYSES
            </h3>

            {historyLoading ? (
              <div className="py-12 flex justify-center"><Spinner /></div>
            ) : history.length === 0 ? (
              <div className="py-12 text-center font-bold uppercase tracking-widest text-[#999]">
                No past analyses found.
              </div>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                {history.map(item => (
                  <div key={item.id} className="border-4 border-swiss-black p-6 hover:bg-swiss-gray transition-colors cursor-pointer flex flex-col justify-between min-h-[160px]"
                       onClick={async () => {
                         try {
                           setLoading(true);
                           const res = await getStatementById(item.id);
                           setAnalysis(res.data);
                           setActiveView('overview');
                           toast.success('LOADED ' + res.data.company_name);
                         } catch (e) { toast.error("FAILED TO LOAD"); } 
                         finally { setLoading(false); }
                       }}>
                    <div>
                      <div className="font-bold text-[10px] uppercase tracking-widest text-[#666] mb-2 border-b-2 border-swiss-black pb-2">
                        {new Date(item.created_at).toLocaleDateString()} // {item.file_format?.toUpperCase() || 'TXT'}
                      </div>
                      <div className="font-black text-xl uppercase tracking-tighter mb-4 leading-none">{item.company_name}</div>
                    </div>
                    
                    <div className="flex justify-between items-end mt-4">
                      <div>
                        <div className="font-bold text-[9px] uppercase tracking-widest text-[#999]">HEALTH</div>
                        <div className="font-black text-2xl" style={{ color: item.health_score > 60 ? '#000' : '#FF3000'}}>{item.health_score}</div>
                      </div>
                      <div className={`px-2 py-1 border-2 border-swiss-black font-black text-[10px] uppercase ${item.credit_verdict === 'ELIGIBLE' ? 'bg-swiss-black text-swiss-white' : 'bg-swiss-white text-swiss-black'}`}>
                        {item.credit_verdict}
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>

      )}

      {/* ══ LOADING ════════════════════════════════════════════════════════ */}
      {loading && (
        <div className="border-4 border-swiss-black p-16 flex flex-col items-center justify-center gap-6 mb-16">
          <Spinner />
          <p className="font-black text-xl uppercase tracking-widest">llama-3.3-70b-versatile reading your statement...</p>
          <p className="font-medium text-sm text-[#666] uppercase tracking-widest">Categorising transactions · Scoring health · Generating insights</p>
        </div>
      )}

      {/* ══ RESULTS ═══════════════════════════════════════════════════════ */}
      {a && !loading && (
        <>
          {/* Results header */}
          <div className="flex flex-col md:flex-row justify-between items-start md:items-end border-b-4 border-swiss-black pb-6 mb-8 gap-4">
            <div>
              <div className="font-bold text-xs uppercase tracking-widest text-[#666] mb-1">ANALYSIS COMPLETE // {a.period}</div>
              <h2 className="font-black text-5xl md:text-7xl uppercase tracking-tighter">{a.company_name}</h2>
            </div>
            <div className="flex flex-wrap gap-3">
              {['overview', 'income', 'expense', 'trend', 'history'].map(v => (
                <button key={v} onClick={() => { setActiveView(v); if (v === 'history') loadHistory(); }}
                  className={`px-6 py-3 font-black text-xs uppercase tracking-widest border-4 transition-colors ${activeView === v ? 'bg-swiss-black text-swiss-white border-swiss-black' : 'bg-swiss-white text-swiss-black border-swiss-black hover:bg-swiss-gray'}`}>
                  {v}{v === 'history' && history.length > 0 ? ` (${history.length})` : ''}
                </button>
              ))}
              <button onClick={() => { setAnalysis(null); setStatementText(''); setFile(null); }}
                className="px-6 py-3 font-black text-xs uppercase tracking-widest border-4 border-swiss-red text-swiss-red hover:bg-swiss-red hover:text-swiss-white transition-colors">
                NEW ANALYSIS
              </button>
            </div>
          </div>

          {/* ── OVERVIEW ───────────────────────────────────────────────── */}
          {activeView === 'overview' && (
            <div className="space-y-8 mb-16">
              {/* KPI row */}
              <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                {[
                  { label: 'TOTAL CREDITS', val: fmt(a.summary.total_credits), sub: '3-month inflows', accent: false },
                  { label: 'TOTAL DEBITS',  val: fmt(a.summary.total_debits),  sub: '3-month outflows', accent: false },
                  { label: 'NET CASHFLOW',  val: fmt(a.summary.net_cashflow),  sub: 'Surplus retained',  accent: true },
                  { label: 'AVG BALANCE',   val: fmt(a.summary.avg_monthly_balance), sub: 'Monthly average', accent: false },
                ].map((k, i) => (
                  <div key={i} className={`border-4 border-swiss-black p-6 hover:scale-[1.01] transition-transform ${k.accent ? 'bg-swiss-black text-swiss-white' : 'bg-swiss-white'}`}>
                    <div className={`font-bold text-[9px] uppercase tracking-widest mb-2 ${k.accent ? 'opacity-60' : 'text-[#666]'}`}>{k.label}</div>
                    <div className="font-black text-2xl md:text-3xl tracking-tighter leading-none mb-1">{k.val}</div>
                    <div className={`font-medium text-xs uppercase tracking-widest ${k.accent ? 'opacity-50' : 'text-[#999]'}`}>{k.sub}</div>
                  </div>
                ))}
              </div>

              {/* Health + Credit verdict side by side */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Health score */}
                <div className="border-4 border-swiss-black p-8 flex items-center gap-8 bg-swiss-white">
                  <div>
                    <div className="font-bold text-xs uppercase tracking-widest text-[#666] mb-2">FINANCIAL HEALTH SCORE</div>
                    <div className="font-black text-[6rem] leading-[0.8] tracking-tighter" style={{ color: HEALTH_COLOR[a.health_label] || '#000' }}>
                      {a.health_score}
                    </div>
                    <div className="font-black text-2xl uppercase tracking-tighter mt-2">{a.health_label}</div>
                  </div>
                  {/* Score bar */}
                  <div className="flex-1">
                    <div className="h-4 bg-swiss-gray border-2 border-swiss-black relative overflow-hidden">
                      <div className="h-full bg-swiss-black transition-all duration-700"
                        style={{ width: `${a.health_score}%` }} />
                    </div>
                    <div className="flex justify-between font-bold text-[9px] mt-1 uppercase tracking-widest text-[#666]">
                      <span>0</span><span>50</span><span>100</span>
                    </div>
                  </div>
                </div>

                {/* Credit verdict */}
                <div className={`border-4 border-swiss-black p-8 ${VERDICT_STYLE[a.credit_verdict] || 'bg-swiss-black text-swiss-white'}`}>
                  <div className="font-bold text-xs uppercase tracking-widest opacity-70 mb-3">NBFC CREDIT VERDICT</div>
                  <div className="font-black text-5xl uppercase tracking-tighter mb-4">{a.credit_verdict}</div>
                  <div className="font-medium text-sm opacity-80 leading-snug">{a.credit_verdict_reason}</div>
                </div>
              </div>

              {/* Working capital */}
              <div className="border-4 border-swiss-black flex flex-col md:flex-row">
                {[
                  { label: 'CURRENT WORKING CAPITAL', val: fmt(a.working_capital.current) },
                  { label: 'CAPITAL REQUIRED', val: fmt(a.working_capital.required) },
                  { label: 'GAP', val: fmt(a.working_capital.gap) },
                  { label: 'RECOMMENDED CREDIT', val: fmt(a.working_capital.credit_recommended) },
                  { label: `EMI (${a.working_capital.tenure_months}M)`, val: fmt(a.working_capital.emi_estimate) },
                ].map((item, i) => (
                  <div key={i} className={`flex-1 px-6 py-5 border-b-4 md:border-b-0 ${i < 4 ? 'md:border-r-4' : ''} border-swiss-black ${i === 3 ? 'bg-swiss-black text-swiss-white' : 'bg-swiss-white'}`}>
                    <div className={`font-bold text-[9px] uppercase tracking-widest mb-1 ${i === 3 ? 'opacity-60' : 'text-[#666]'}`}>{item.label}</div>
                    <div className="font-black text-2xl tracking-tighter">{item.val}</div>
                  </div>
                ))}
              </div>

              {/* AI Insights */}
              <div className="border-4 border-swiss-black bg-swiss-white p-8 md:p-10">
                <div className="font-black text-xs uppercase tracking-widest mb-6 border-b-4 border-swiss-black pb-4 flex items-center gap-4">
                  <span className="w-7 h-7 bg-swiss-black text-swiss-white flex items-center justify-center text-xs font-black">AI</span>
                  GROQ AI RECOMMENDATIONS
                  <span className="ml-auto text-[#999] font-bold text-[9px]">llama-3.3-70b-versatile</span>
                </div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  {(a.ai_insights || []).map((tip, i) => (
                    <div key={i} className="flex gap-4 border-2 border-swiss-black p-5 hover:bg-swiss-gray transition-colors">
                      <span className="w-7 h-7 flex-shrink-0 border-2 border-swiss-black bg-swiss-black text-swiss-white font-black text-xs flex items-center justify-center">{i+1}</span>
                      <p className="font-medium text-sm text-[#333] leading-relaxed">{tip}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          )}

          {/* ── INCOME BREAKDOWN ────────────────────────────────────────── */}
          {activeView === 'income' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
              <div className="border-4 border-swiss-black bg-swiss-white p-8">
                <h3 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8">INCOME SOURCES</h3>
                <table className="w-full">
                  <thead><tr className="border-b-2 border-swiss-black">
                    <th className="text-left font-bold text-xs uppercase tracking-widest pb-3 text-[#666]">CATEGORY</th>
                    <th className="text-right font-bold text-xs uppercase tracking-widest pb-3 text-[#666]">AMOUNT</th>
                    <th className="text-right font-bold text-xs uppercase tracking-widest pb-3 text-[#666]">SHARE</th>
                  </tr></thead>
                  <tbody className="divide-y-2 divide-swiss-gray">
                    {(a.income_breakdown || []).map((row, i) => (
                      <tr key={i} className="hover:bg-swiss-gray transition-colors">
                        <td className="py-4 font-bold text-sm">{row.category}</td>
                        <td className="py-4 font-black text-xl text-right tracking-tighter">{fmt(row.amount)}</td>
                        <td className="py-4 font-bold text-sm text-right text-[#666]">{row.percentage}%</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot><tr className="border-t-4 border-swiss-black">
                    <td className="pt-4 font-black uppercase tracking-widest">TOTAL CREDITS</td>
                    <td className="pt-4 font-black text-2xl text-right tracking-tighter">{fmt(a.summary.total_credits)}</td>
                    <td className="pt-4 font-black text-right">100%</td>
                  </tr></tfoot>
                </table>
              </div>
              <div className="border-4 border-swiss-black bg-swiss-white p-8">
                <h3 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8">INCOME PIE</h3>
                <ResponsiveContainer width="100%" height={320}>
                  <PieChart>
                    <Pie data={a.income_breakdown} dataKey="amount" nameKey="category" cx="50%" cy="50%" outerRadius={110} label={({ category, percentage }) => `${percentage}%`}>
                      {(a.income_breakdown || []).map((_, i) => <Cell key={i} fill={INCOME_COLORS[i % INCOME_COLORS.length]} />)}
                    </Pie>
                    <Legend formatter={v => <span className="font-bold text-xs uppercase">{v}</span>} />
                    <Tooltip content={<ChartTip />} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* ── EXPENSE BREAKDOWN ───────────────────────────────────────── */}
          {activeView === 'expense' && (
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-16">
              <div className="border-4 border-swiss-black bg-swiss-white p-8">
                <h3 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8">EXPENSE CATEGORIES</h3>
                <table className="w-full">
                  <thead><tr className="border-b-2 border-swiss-black">
                    <th className="text-left font-bold text-xs uppercase tracking-widest pb-3 text-[#666]">CATEGORY</th>
                    <th className="text-right font-bold text-xs uppercase tracking-widest pb-3 text-[#666]">AMOUNT</th>
                    <th className="text-right font-bold text-xs uppercase tracking-widest pb-3 text-[#666]">SHARE</th>
                  </tr></thead>
                  <tbody className="divide-y-2 divide-swiss-gray">
                    {(a.expense_breakdown || []).map((row, i) => (
                      <tr key={i} className="hover:bg-swiss-gray transition-colors">
                        <td className="py-4 font-bold text-sm flex items-center gap-2">
                          <span className="w-3 h-3 flex-shrink-0" style={{ background: EXPENSE_COLORS[i % EXPENSE_COLORS.length] }} />
                          {row.category}
                        </td>
                        <td className="py-4 font-black text-xl text-right tracking-tighter text-swiss-red">{fmt(row.amount)}</td>
                        <td className="py-4 font-bold text-sm text-right text-[#666]">{row.percentage}%</td>
                      </tr>
                    ))}
                  </tbody>
                  <tfoot><tr className="border-t-4 border-swiss-black">
                    <td className="pt-4 font-black uppercase tracking-widest">TOTAL DEBITS</td>
                    <td className="pt-4 font-black text-2xl text-right tracking-tighter text-swiss-red">{fmt(a.summary.total_debits)}</td>
                    <td className="pt-4 font-black text-right">100%</td>
                  </tr></tfoot>
                </table>
              </div>
              <div className="border-4 border-swiss-black bg-swiss-white p-8">
                <h3 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8">EXPENSE PIE</h3>
                <ResponsiveContainer width="100%" height={320}>
                  <PieChart>
                    <Pie data={a.expense_breakdown} dataKey="amount" nameKey="category" cx="50%" cy="50%" outerRadius={110} label={({ percentage }) => `${percentage}%`}>
                      {(a.expense_breakdown || []).map((_, i) => <Cell key={i} fill={EXPENSE_COLORS[i % EXPENSE_COLORS.length]} />)}
                    </Pie>
                    <Legend formatter={v => <span className="font-bold text-xs uppercase">{v}</span>} />
                    <Tooltip content={<ChartTip />} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>
          )}

          {/* ── MONTHLY TREND ────────────────────────────────────────────── */}
          {activeView === 'trend' && (
            <div className="border-4 border-swiss-black bg-swiss-white p-8 mb-16">
              <h3 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8 flex justify-between items-end">
                MONTHLY CASH FLOW TREND
                <span className="font-bold text-xs text-[#999] uppercase tracking-widest">{a.period}</span>
              </h3>
              <div className="h-[380px]">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={a.monthly_trend} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="none" vertical={false} stroke="#e5e5e5" strokeWidth={2} />
                    <XAxis dataKey="month" tick={{ fill: '#000', fontSize: 11, fontWeight: 900 }} axisLine={{ stroke: '#000', strokeWidth: 4 }} tickLine={false} />
                    <YAxis tick={{ fill: '#000', fontSize: 11, fontWeight: 700 }} axisLine={{ stroke: '#000', strokeWidth: 4 }} tickLine={false} tickFormatter={v => `₹${(v/1000).toFixed(0)}k`} />
                    <Tooltip content={<ChartTip />} />
                    <Legend formatter={v => <span className="font-bold text-xs uppercase tracking-widest">{v}</span>} />
                    <Bar dataKey="credits" name="Credits" fill="#000000" />
                    <Bar dataKey="debits"  name="Debits"  fill="#FF3000" />
                    <Bar dataKey="net"     name="Net"     fill="#888888" />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              {/* Monthly summary table */}
              <div className="mt-8 border-t-4 border-swiss-black pt-6">
                <table className="w-full">
                  <thead><tr className="border-b-2 border-swiss-black">
                    {['MONTH', 'CREDITS', 'DEBITS', 'NET', 'STATUS'].map(h => (
                      <th key={h} className="text-left font-bold text-xs uppercase tracking-widest pb-3 text-[#666]">{h}</th>
                    ))}
                  </tr></thead>
                  <tbody className="divide-y-2 divide-swiss-gray">
                    {(a.monthly_trend || []).map((row, i) => (
                      <tr key={i} className="hover:bg-swiss-gray transition-colors">
                        <td className="py-4 font-black text-base">{row.month}</td>
                        <td className="py-4 font-bold">{fmt(row.credits)}</td>
                        <td className="py-4 font-bold text-swiss-red">{fmt(row.debits)}</td>
                        <td className={`py-4 font-black text-xl tracking-tighter ${row.net >= 0 ? '' : 'text-swiss-red'}`}>{fmt(row.net)}</td>
                        <td className="py-4">
                          <span className={`px-3 py-1 border-2 font-bold text-[10px] uppercase tracking-widest ${row.net >= 0 ? 'border-swiss-black bg-swiss-black text-swiss-white' : 'border-swiss-red text-swiss-red'}`}>
                            {row.net >= 0 ? 'SURPLUS' : 'DEFICIT'}
                          </span>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
          {/* ── HISTORY ────────────────────────────────────────────── */}
          {activeView === 'history' && (
            <div className="border-4 border-swiss-black bg-swiss-white p-8 mb-16">
              <h3 className="font-black text-2xl uppercase tracking-tighter border-b-4 border-swiss-black pb-4 mb-8">
                SAVED ANALYSES
              </h3>

              {historyLoading ? (
                <div className="py-12 flex justify-center"><Spinner /></div>
              ) : history.length === 0 ? (
                <div className="py-12 text-center font-bold uppercase tracking-widest text-[#999]">
                  No past analyses found.
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                  {history.map(item => (
                    <div key={item.id} className="border-4 border-swiss-black p-6 hover:bg-swiss-gray transition-colors cursor-pointer"
                         onClick={async () => {
                           try {
                             setLoading(true);
                             const res = await getStatementById(item.id);
                             setAnalysis(res.data);
                             setActiveView('overview');
                             toast.success('LOADED ' + res.data.company_name);
                           } catch (e) { toast.error("FAILED TO LOAD"); } 
                           finally { setLoading(false); }
                         }}>
                      <div className="font-bold text-[10px] uppercase tracking-widest text-[#666] mb-2 border-b-2 border-swiss-black pb-2">
                        {new Date(item.created_at).toLocaleDateString()} // {item.file_format?.toUpperCase() || 'TXT'}
                      </div>
                      <div className="font-black text-2xl uppercase tracking-tighter mb-4 leading-none">{item.company_name}</div>
                      
                      <div className="flex justify-between items-end">
                        <div>
                          <div className="font-bold text-[9px] uppercase tracking-widest text-[#999]">HEALTH</div>
                          <div className="font-black text-3xl" style={{ color: item.health_score > 60 ? '#000' : '#FF3000'}}>{item.health_score}</div>
                        </div>
                        <div className={`px-2 py-1 border-2 border-swiss-black font-black text-[10px] uppercase ${item.credit_verdict === 'ELIGIBLE' ? 'bg-swiss-black text-swiss-white' : 'bg-swiss-white text-swiss-black'}`}>
                          {item.credit_verdict}
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </>
      )}
    </div>
  );
}

