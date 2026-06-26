import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { UserProvider } from './context/UserContext';
import Navbar from './components/Navbar';
import CheckoutPage from './pages/CheckoutPage';
import DashboardPage from './pages/DashboardPage';
import TravelPage from './pages/TravelPage';
import AgentPage from './pages/AgentPage';
import HistoryPage from './pages/HistoryPage';
import LoginPage from './pages/LoginPage';
import ItrPage from './pages/ItrPage';
import DemoOne from './components/ui/demo';

export default function App() {
  return (
    <UserProvider>
      <BrowserRouter future={{ v7_startTransition: true, v7_relativeSplatPath: true }}>
        <Toaster position="bottom-right" 
          toastOptions={{
            style: {
              borderRadius: '0px',
              background: '#000000',
              color: '#FFFFFF',
              border: '2px solid #FF3000',
              fontFamily: '"Inter", sans-serif',
              fontWeight: '700',
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              padding: '16px 24px',
              boxShadow: 'none',
            },
          }}
        />

        <Routes>
          <Route path="/" element={<DemoOne />} />
          <Route path="/*" element={
            <div className="relative min-h-screen w-full bg-swiss-white text-swiss-black font-inter selection:bg-swiss-red selection:text-swiss-white flex flex-col">
              
              {/* Global Grid pattern overlay, very subtle */}
              <div className="fixed inset-0 pointer-events-none z-0 bg-swiss-grid bg-swiss-grid mix-blend-multiply opacity-50" />

              <Navbar />
              
              <main className="relative z-10 w-full flex-grow pt-24 px-4 sm:px-8 xl:px-16 mx-auto max-w-[1920px]">
                <Routes>
                  <Route path="/dashboard" element={<DashboardPage />} />
                  <Route path="/travel" element={<TravelPage />} />
                  <Route path="/agent" element={<AgentPage />} />
                  <Route path="/checkout" element={<CheckoutPage />} />
                  <Route path="/history" element={<HistoryPage />} />
                  <Route path="/tax" element={<ItrPage />} />
                  <Route path="/login" element={<LoginPage />} />
                  <Route path="*" element={
                    <div className="flex flex-col justify-center items-start h-[60vh] border-l-4 border-swiss-black pl-8 ml-8">
                      <h1 className="font-black text-[10rem] leading-none text-swiss-red tracking-tighter">404</h1>
                      <div className="font-bold text-2xl uppercase tracking-widest mt-4">
                        FILE NOT FOUND.
                      </div>
                    </div>
                  } />
                </Routes>
              </main>

              <footer className="relative z-10 border-t-2 border-swiss-black py-8 px-4 sm:px-8 xl:px-16 mt-32 flex justify-between items-center text-sm font-bold uppercase tracking-widest bg-swiss-white">
                 <span className="text-swiss-black">PAISA // RBI AA FRAMEWORK</span>
                 <span className="text-swiss-red">INTELLIGENCE LAYER</span>
              </footer>
            </div>
          } />
        </Routes>
      </BrowserRouter>
    </UserProvider>
  );
}
