import React from 'react';
import { useInsights } from '../hooks/useInsights';
import { useUser } from '../context/UserContext';
import Spinner from '../components/Spinner';
import { Link } from 'react-router-dom';

export default function HistoryPage() {
  const { user } = useUser();
  const { transactions, loading } = useInsights(user?.id);

  if (!user) {
    return (
      <div className="flex flex-col items-start justify-center min-h-[60vh] w-full max-w-4xl mx-auto border-l-8 border-swiss-red pl-12 h-full">
        <h2 className="font-black text-7xl md:text-9xl text-swiss-black mb-8 uppercase leading-[0.85] tracking-tighter">ACCESS<br/>RESTRICTED.</h2>
        <p className="font-bold text-lg uppercase tracking-widest mb-16 text-[#666] border-b-2 border-swiss-black pb-4">Auth token required to access system ledger</p>
        <Link to="/login" className="inline-flex border-4 border-swiss-black bg-swiss-black text-swiss-white px-12 py-6 font-bold uppercase text-lg tracking-widest hover:bg-swiss-red hover:border-swiss-red transition-colors duration-150 ease-linear">
           AUTHENTICATE
        </Link>
      </div>
    );
  }

  return (
    <div className="w-full text-swiss-black font-inter relative z-10 max-w-[1920px] mx-auto">
      <div className="mb-24 flex flex-col md:flex-row justify-between items-start md:items-end border-b-4 border-swiss-black pb-12 w-full">
        <div className="group">
           <div className="inline-block px-4 py-2 border-2 border-swiss-black bg-swiss-white font-bold uppercase text-xs tracking-widest mb-6">
              04. IMMUTABLE CHAIN 
           </div>
           <h1 className="font-black text-[6rem] md:text-[8rem] xl:text-[10rem] uppercase tracking-tighter leading-[0.85] mix-blend-multiply w-full overflow-hidden block">
             LOGS.
           </h1>
        </div>
        <div className="mt-8 md:mt-0 font-bold uppercase tracking-widest text-sm text-swiss-black border-2 border-swiss-black px-8 py-6 flex items-center gap-4 group hover:bg-swiss-black hover:text-swiss-white transition-colors duration-150">
          <span>VOLUME COUNT</span>
          <span className="font-black text-xl bg-swiss-red text-swiss-white px-3 py-1 scale-100 group-hover:scale-110 transition-transform">{transactions?.length || 0}</span>
        </div>
      </div>

      {loading ? <Spinner /> : (
        <div className="relative border-4 border-swiss-black p-0 md:p-12 xl:p-24 bg-swiss-white overflow-hidden text-swiss-black group">
          
          <div className="absolute inset-0 bg-swiss-grid opacity-10 mix-blend-multiply pointer-events-none transition-opacity group-hover:opacity-20" />

          <div className="overflow-x-auto overflow-y-hidden custom-scrollbar relative z-10 w-full mb-32">
            <table className="w-full text-left font-bold border-collapse min-w-[1000px]">
              <thead className="border-b-4 border-swiss-black text-xs uppercase tracking-widest text-[#666] bg-swiss-gray">
                <tr>
                  <th className="px-8 py-8 w-[20%]">TIMESTAMP</th>
                  <th className="px-8 py-8 border-l-2 border-swiss-black w-[15%]">VECTOR</th>
                  <th className="px-8 py-8 border-l-2 border-swiss-black w-[15%]">CLASS</th>
                  <th className="px-8 py-8 border-l-2 border-swiss-black w-[20%] text-right">MASS</th>
                  <th className="px-8 py-8 border-l-2 border-swiss-black w-[15%] text-right text-swiss-red">ECHO</th>
                  <th className="px-8 py-8 border-l-2 border-swiss-black w-[15%] text-center">STATE</th>
                </tr>
              </thead>
              <tbody className="divide-y-2 divide-swiss-black bg-swiss-white">
                {transactions.length === 0 ? (
                  <tr>
                    <td colSpan="6" className="px-8 py-32 text-center text-[3rem] md:text-[5rem] uppercase font-black text-[#ccc] tracking-tighter">
                      NULL DATA
                    </td>
                  </tr>
                ) : (
                  transactions.map(t => (
                    <tr key={t.id} className="transition-colors hover:bg-swiss-black hover:text-swiss-white group/row relative overflow-hidden">
                      <td className="px-8 py-6 text-sm whitespace-nowrap opacity-80 font-medium">
                        {new Date(t.created_at).toLocaleDateString('en-GB', { 
                          day: '2-digit', month: 'short', year: 'numeric',
                          hour: '2-digit', minute:'2-digit'
                        })}
                      </td>
                      <td className="px-8 py-6 whitespace-nowrap border-l-2 border-swiss-black group-hover/row:border-swiss-white">
                        <span className="border-2 border-swiss-black text-swiss-black px-3 py-1 text-xs uppercase tracking-widest bg-swiss-white group-hover/row:bg-swiss-white">
                          {t.payment_method}
                        </span>
                      </td>
                      <td className="px-8 py-6 uppercase text-xs tracking-widest whitespace-nowrap border-l-2 border-swiss-black group-hover/row:border-swiss-white opacity-60">
                        {t.category ? t.category : '—'}
                      </td>
                      <td className="px-8 py-6 text-right text-3xl whitespace-nowrap font-black tracking-tighter border-l-2 border-swiss-black group-hover/row:border-swiss-white">
                        ₹{t.amount.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-8 py-6 text-right text-2xl whitespace-nowrap font-black border-l-2 border-swiss-black group-hover/row:border-swiss-white text-swiss-red">
                        {t.cashback_earned > 0 ? '+' : ''}₹{t.cashback_earned.toLocaleString('en-IN', { minimumFractionDigits: 2 })}
                      </td>
                      <td className="px-8 py-6 text-center whitespace-nowrap border-l-2 border-swiss-black group-hover/row:border-swiss-white">
                        <span className={`inline-block border-2 px-4 py-2 text-xs uppercase tracking-widest transition-colors duration-150 ${
                          t.status === 'success' 
                            ? 'bg-swiss-white border-swiss-black text-swiss-black group-hover/row:bg-swiss-red group-hover/row:border-swiss-red group-hover/row:text-swiss-white' 
                            : 'bg-swiss-black border-swiss-black text-swiss-white group-hover/row:bg-swiss-white group-hover/row:text-swiss-black'
                        }`}>
                          {t.status === 'success' ? 'ALIGNED' : 'FRACTURE'}
                        </span>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        </div>
      )}
    </div>
  );
}
