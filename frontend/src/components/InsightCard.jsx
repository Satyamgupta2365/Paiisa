import React from 'react';

export default function InsightCard({ title, value, sub, variant = 'white' }) {
  const styles = {
    white: "bg-swiss-white text-swiss-black border-swiss-black hover:bg-swiss-gray",
    gray: "bg-swiss-gray text-swiss-black border-swiss-black hover:bg-swiss-white",
    black: "bg-swiss-black text-swiss-white border-swiss-black hover:bg-swiss-red hover:border-swiss-red",
    red: "bg-swiss-red text-swiss-white border-swiss-red hover:bg-swiss-black hover:border-swiss-black",
  };

  return (
    <div 
      className={`border-4 p-8 group transition-colors duration-150 ease-linear flex flex-col justify-between min-h-[220px] ${styles[variant]} relative overflow-hidden`}
    >
      {/* Background patterns based on variant */}
      {variant === 'gray' && <div className="absolute inset-0 bg-swiss-grid opacity-20 transition-opacity group-hover:opacity-5" />}
      {variant === 'red' && <div className="absolute inset-0 bg-swiss-dots opacity-40 transition-opacity group-hover:opacity-10 mix-blend-multiply" />}

      <div className={`relative z-10 font-bold text-xs uppercase tracking-widest mb-16 opacity-80 ${variant === 'black' || variant === 'red' ? 'text-swiss-white' : 'text-[#666]'}`}>
        {title}
      </div>
      
      <div className="relative z-10">
        <div className={`font-black text-5xl md:text-7xl uppercase tracking-tighter leading-none transition-transform duration-300 group-hover:scale-[1.05] group-hover:translate-x-2 origin-left`}>
          {value}
        </div>
        {sub && (
           <div className="mt-8">
              <span className={`inline-block border-2 font-bold px-4 py-2 text-xs uppercase tracking-widest ${variant === 'white' || variant === 'gray' ? 'border-swiss-black text-swiss-black' : 'border-swiss-white text-swiss-white'}`}>
                 {sub}
              </span>
           </div>
        )}
      </div>

      {/* Swiss corner accent */}
      <div className={`absolute top-0 right-0 w-8 h-8 flex items-center justify-center border-l-4 border-b-4 ${variant === 'black' || variant === 'red' ? 'border-swiss-white' : 'border-swiss-black'}`}>
         <div className="w-3 h-3 rounded-full bg-current transition-transform duration-300 group-hover:rotate-90"></div>
      </div>
    </div>
  );
}
