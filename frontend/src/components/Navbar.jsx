import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useUser } from '../context/UserContext';

export default function Navbar() {
  const { user, setUser } = useUser();
  const location = useLocation();

  const isActive = (path) => location.pathname === path ? "bg-swiss-red text-swiss-white" : "text-swiss-black hover:bg-swiss-black hover:text-swiss-white transition-colors duration-150 ease-linear";

  return (
    <nav className="fixed top-0 left-0 w-full z-50 border-b-2 border-swiss-black bg-swiss-white">
      <div className="flex items-center justify-between px-4 sm:px-8 xl:px-16 h-16 w-full max-w-[1920px] mx-auto">
        
        <Link to="/" className="flex items-center gap-4 h-full border-r-2 border-swiss-black pr-8 hover:bg-swiss-red hover:text-swiss-white transition-colors duration-150 ease-linear px-4 -ml-4">
           {/* Geometric Logo */}
           <div className="w-6 h-6 bg-swiss-black rounded-none group-hover:bg-swiss-white"></div>
           <span className="font-black text-xl uppercase tracking-widest leading-none">PAISA</span>
        </Link>
        
        <div className="hidden md:flex items-center h-full font-bold uppercase tracking-widest text-xs">
          <Link to="/dashboard" className={`h-full flex items-center px-6 border-l-2 border-swiss-black ${isActive('/dashboard')}`}>MERCHANT</Link>
          <Link to="/travel" className={`h-full flex items-center px-6 border-l-2 border-swiss-black ${isActive('/travel')}`}>STMT AI</Link>
          <Link to="/agent" className={`h-full flex items-center px-6 border-l-2 border-swiss-black ${isActive('/agent')}`}>TAP SERVER</Link>
          <Link to="/tax" className={`h-full flex items-center px-6 border-l-2 border-swiss-black ${isActive('/tax')}`}>ITR COMPLIANCE</Link>
          <Link to="/checkout" className={`h-full flex items-center px-6 border-l-2 border-swiss-black ${isActive('/checkout')}`}>CHECKOUT</Link>
          <Link to="/history" className={`h-full flex items-center px-6 border-l-2 border-swiss-black ${isActive('/history')}`}>AUDIT</Link>
        </div>

        <div className="flex items-center h-full border-l-2 border-swiss-black pl-8 ml-auto md:ml-0">
          {user ? (
            <div className="flex items-center gap-6 h-full">
              <span className="font-bold text-xs uppercase tracking-widest hidden sm:block">ID: {user.name}</span>
              <button 
                onClick={() => setUser(null)}
                className="h-full flex items-center px-6 border-l-2 border-swiss-black font-bold uppercase text-xs tracking-widest hover:bg-swiss-red hover:text-swiss-white transition-colors duration-150 ease-linear -mr-4 sm:-mr-8 xl:-mr-16 bg-swiss-black text-swiss-white"
              >
                REVOKE AA
              </button>
            </div>
          ) : (
            <Link to="/login" className="h-full flex items-center px-8 border-l-2 border-swiss-black font-bold uppercase text-xs tracking-widest hover:bg-swiss-black hover:text-swiss-white transition-colors duration-150 ease-linear -mr-4 sm:-mr-8 xl:-mr-16 bg-swiss-red text-swiss-white">
              LINK BANK
            </Link>
          )}
        </div>

      </div>
    </nav>
  );
}
