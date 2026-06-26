import React from 'react';

export default function PaymentOptionCard({ option, isRecommended, onSelect }) {
  // Base structural container classes
  const containerBase = "border-4 transition-colors duration-150 ease-linear p-10 flex flex-col justify-between cursor-pointer relative min-h-[420px] group overflow-hidden ";
  
  // State-based coloring
  const stateColor = isRecommended 
    ? "bg-swiss-red border-swiss-red text-swiss-white hover:bg-swiss-black hover:border-swiss-black" 
    : "bg-swiss-gray border-swiss-black text-swiss-black hover:bg-swiss-white";

  return (
    <div 
      className={containerBase + stateColor}
      onClick={() => onSelect(option.method)}
    >
      
      {/* Texture overlay */}
      {!isRecommended && <div className="absolute inset-0 bg-swiss-diagonal opacity-20 pointer-events-none transition-opacity group-hover:opacity-[0.02] mix-blend-multiply" />}
      {isRecommended && <div className="absolute inset-0 bg-swiss-dots opacity-40 pointer-events-none transition-opacity mix-blend-multiply" />}

      {/* Recommended Tag */}
      {isRecommended && (
        <div className="absolute top-0 right-0 bg-swiss-black text-swiss-white px-4 py-2 font-bold uppercase text-xs tracking-widest border-b-4 border-l-4 border-swiss-white transition-colors duration-150 group-hover:border-swiss-black">
          OPTIMIZED VECTOR
        </div>
      )}

      {/* Header section */}
      <div className="mb-12 relative z-10 border-b-4 border-current pb-8 flex flex-col h-full">
        <h3 className={`font-black text-4xl sm:text-5xl uppercase tracking-tighter leading-[0.9] break-words transition-transform duration-300 origin-left group-hover:scale-105`}>
          {option.method}
        </h3>
        
        <div className="mt-8">
           <span className={`inline-block border-2 px-3 py-1 font-bold text-xs uppercase tracking-widest ${isRecommended ? 'border-swiss-white' : 'border-swiss-black'}`}>
             GATEWAY STATUS: OPEN
           </span>
        </div>
      </div>

      {/* Data section */}
      <div className="relative z-10 w-full mt-auto space-y-4">
        <div className="flex justify-between items-center text-sm md:text-base border-b-2 border-current pb-4 border-dashed opacity-80">
          <span className="font-bold uppercase tracking-widest">YIELD RATE</span>
          <span className="font-bold">x{option.cashback}%</span>
        </div>
        
        <div className="flex justify-between items-end pt-2">
          <span className="font-bold uppercase tracking-widest text-sm opacity-80 mb-2">NET RETURN</span>
          <span className={`text-4xl sm:text-5xl font-black tracking-tighter ${option.savings > 0 && !isRecommended ? 'text-swiss-red group-hover:text-swiss-black' : ''}`}>
            +₹{option.savings.toFixed(2)}
          </span>
        </div>
        
        {/* Action Button */}
        <div className="mt-12 pt-8 border-t-4 border-current">
           <div className={`w-full text-center py-6 font-bold text-lg uppercase tracking-widest border-2 transition-colors duration-150
             ${isRecommended ? 'bg-swiss-white text-swiss-red border-swiss-white group-hover:text-swiss-black' : 'bg-transparent border-swiss-black text-swiss-black group-hover:bg-swiss-black group-hover:text-swiss-white'}
           `}>
             EXECUTE 
             <span className="inline-block transform group-hover:translate-x-4 transition-transform duration-300">→</span>
           </div>
        </div>
      </div>
    </div>
  );
}
