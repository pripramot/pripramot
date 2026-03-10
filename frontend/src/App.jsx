import React, { useState, useEffect } from 'react';
import { invoke } from '@tauri-apps/api/core';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Search, ShoppingBag, Terminal, FileText, 
  ShieldCheck, LayoutGrid, AppWindow, 
  Settings, Download, Star, ChevronRight, Info
} from 'lucide-react';

export default function App() {
  const [activeTab, setActiveTab] = useState('store'); // เริ่มที่หน้า Store สวยๆ
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [apps, setApps] = useState([
    { id: 1, name: 'GSTORE Native Scanner', desc: 'Forensics & File Discovery', category: 'Security', rating: 4.9, icon: <ShieldCheck className="text-emerald-400" /> },
    { id: 2, name: 'AHQ Store', desc: 'Modern App Management', category: 'Utility', rating: 4.8, icon: <AppWindow className="text-blue-400" /> },
    { id: 3, name: 'CoCo-RS', desc: 'Rust-powered File Launcher', category: 'System', rating: 4.7, icon: <Terminal className="text-purple-400" /> },
    { id: 4, name: 'Hex Inspector', desc: 'Binary Data Analysis', category: 'Forensics', rating: 4.5, icon: <FileText className="text-orange-400" /> },
  ]);

  const handleSearch = async () => {
    if (!query) return;
    try {
      const res = await invoke('search_files', { query, path: 'C:\\Users\\usEr' });
      setResults(res);
      await invoke('log_forensic_event', { action: 'SEARCH', details: `User searched: ${query}` });
    } catch (err) { console.error(err); }
  };

  return (
    <div className="flex h-screen bg-[#0a0a0a] text-slate-200 overflow-hidden font-sans selection:bg-blue-500/30">
      
      {/* 🏙️ Microsoft Style Sidebar (Acrylic Blur) */}
      <nav className="w-64 flex flex-col p-4 bg-[#1c1c1c]/60 backdrop-blur-2xl border-r border-white/5">
        <div className="flex items-center gap-3 px-4 mb-8 py-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center shadow-lg shadow-blue-500/20">
            <ShieldCheck size={20} className="text-white" />
          </div>
          <span className="font-bold text-xl tracking-tight text-white">GSTORE</span>
        </div>

        <div className="flex-1 space-y-1">
          <SidebarItem active={activeTab === 'store'} onClick={() => setActiveTab('store')} icon={<LayoutGrid size={18} />} label="Home" />
          <SidebarItem active={activeTab === 'search'} onClick={() => setActiveTab('search')} icon={<Search size={18} />} label="Search Engine" />
          <SidebarItem active={activeTab === 'apps'} onClick={() => setActiveTab('apps')} icon={<AppWindow size={18} />} label="Installed Apps" />
          <SidebarItem active={activeTab === 'logs'} onClick={() => setActiveTab('logs')} icon={<Terminal size={18} />} label="Audit Logs" />
        </div>

        <div className="pt-4 border-t border-white/5">
          <SidebarItem active={activeTab === 'settings'} onClick={() => setActiveTab('settings')} icon={<Settings size={18} />} label="Settings" />
        </div>
      </nav>

      {/* 🚀 Main Display (Mica Effect) */}
      <main className="flex-1 overflow-auto bg-gradient-to-b from-[#121212] to-[#0a0a0a] relative">
        
        {/* Top Header Blur */}
        <div className="sticky top-0 z-30 h-16 bg-[#121212]/80 backdrop-blur-md border-b border-white/5 px-12 flex items-center justify-between">
           <div className="relative w-96 group">
              <Search className="absolute left-3 top-2.5 text-slate-500 group-focus-within:text-blue-400 transition-colors" size={16} />
              <input 
                value={query} onChange={(e) => setQuery(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
                className="w-full bg-[#1c1c1c] border border-white/5 rounded-md pl-10 pr-4 py-2 text-sm focus:outline-none focus:ring-1 focus:ring-blue-500/50 transition-all"
                placeholder="Search apps, files, or forensics data..."
              />
           </div>
           <div className="flex items-center gap-4">
              <button className="p-2 hover:bg-white/5 rounded-md transition-colors text-slate-400 hover:text-white"><Info size={18} /></button>
              <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-500 to-indigo-600 border border-white/20 shadow-inner"></div>
           </div>
        </div>

        <div className="p-12">
          <AnimatePresence mode="wait">
            {activeTab === 'store' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
                {/* 🌟 Hero Banner */}
                <div className="relative h-64 w-full rounded-3xl overflow-hidden mb-12 group cursor-pointer border border-white/5">
                  <div className="absolute inset-0 bg-gradient-to-r from-blue-600/40 to-purple-600/20 mix-blend-overlay group-hover:scale-105 transition-transform duration-700"></div>
                  <img src="https://images.unsplash.com/photo-1633356122544-f134324a6cee?q=80&w=2070" className="w-full h-full object-cover opacity-40 group-hover:scale-105 transition-transform duration-700" alt="Banner" />
                  <div className="absolute inset-0 p-10 flex flex-col justify-end bg-gradient-to-t from-black/80 to-transparent">
                    <h2 className="text-4xl font-bold text-white mb-2">Featured: GSTORE Alpha</h2>
                    <p className="text-slate-300 max-w-lg">สัมผัสประสบการณ์การค้นหาไฟล์ระดับนิติวิทยาศาสตร์ที่เร็วที่สุด พร้อมระบบ AI Discovery ของแท้!</p>
                  </div>
                </div>

                {/* 📦 App Grid */}
                <h3 className="text-2xl font-semibold mb-6 text-white px-2">Top Apps</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                  {apps.map((app) => (
                    <AppCard key={app.id} app={app} />
                  ))}
                </div>
              </motion.div>
            )}

            {activeTab === 'search' && (
              <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }} exit={{ opacity: 0, y: -10 }}>
                <div className="flex justify-between items-end mb-8">
                  <div>
                    <h1 className="text-3xl font-bold text-white">Forensic Search</h1>
                    <p className="text-slate-400">Scan your system with Rust-powered engine.</p>
                  </div>
                  <button onClick={handleSearch} className="px-6 py-2 bg-blue-600 hover:bg-blue-500 text-white font-semibold rounded-md transition-all shadow-lg shadow-blue-600/20 active:scale-95 flex items-center gap-2">
                    <Search size={16} /> Run Scan
                  </button>
                </div>

                <div className="bg-[#1c1c1c]/40 border border-white/5 rounded-2xl p-6 backdrop-blur-md min-h-[400px]">
                  {results.length === 0 ? (
                    <div className="flex flex-col items-center justify-center h-full text-slate-500 py-20">
                      <HardDrive size={48} className="mb-4 opacity-20" />
                      <p>ป้อนคำค้นหาและเลือก "Run Scan" เพื่อเริ่มงานค่ะ</p>
                    </div>
                  ) : (
                    <div className="divide-y divide-white/5">
                      {results.map((file) => (
                        <div key={file.path} className="py-4 px-2 hover:bg-white/5 transition-colors group flex items-center justify-between">
                          <div className="flex items-center gap-4">
                            <div className="p-2 bg-slate-800 rounded group-hover:bg-blue-600/20 transition-colors text-slate-400 group-hover:text-blue-400"><FileText size={18} /></div>
                            <div>
                              <div className="text-sm font-medium text-slate-200">{file.name}</div>
                              <div className="text-xs text-slate-500 font-mono">{file.path}</div>
                            </div>
                          </div>
                          <ChevronRight size={14} className="text-slate-600" />
                        </div>
                      ))}
                    </div>
                  )}
                </div>
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
    </div>
  );
}

function SidebarItem({ icon, label, active, onClick }) {
  return (
    <button 
      onClick={onClick}
      className={`w-full flex items-center gap-3 px-4 py-2.5 rounded-md text-sm transition-all relative group ${
        active ? 'bg-white/10 text-white font-medium shadow-sm' : 'text-slate-400 hover:bg-white/5 hover:text-slate-200'
      }`}
    >
      {active && <motion.div layoutId="navMarker" className="absolute left-0 w-1 h-5 bg-blue-500 rounded-full" />}
      <span className={active ? 'text-blue-400' : ''}>{icon}</span>
      {label}
    </button>
  );
}

function AppCard({ app }) {
  return (
    <motion.div 
      whileHover={{ y: -4 }}
      className="p-5 bg-[#1c1c1c]/40 hover:bg-[#252525]/60 border border-white/5 rounded-2xl cursor-pointer transition-all group relative overflow-hidden"
    >
      <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500/20 to-transparent opacity-0 group-hover:opacity-100 transition-opacity"></div>
      <div className="w-14 h-14 bg-[#0a0a0a] rounded-xl flex items-center justify-center mb-4 border border-white/5 shadow-inner transition-transform group-hover:scale-105 duration-500">
        {React.cloneElement(app.icon, { size: 32 })}
      </div>
      <h4 className="font-bold text-white mb-1">{app.name}</h4>
      <p className="text-xs text-slate-500 mb-4 h-8 overflow-hidden">{app.desc}</p>
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-1 text-[10px] text-orange-400 bg-orange-400/10 px-2 py-0.5 rounded-full font-bold">
          <Star size={10} fill="currentColor" /> {app.rating}
        </div>
        <button className="p-2 bg-blue-600/10 text-blue-400 hover:bg-blue-600 hover:text-white rounded-lg transition-all active:scale-90">
          <Download size={14} />
        </button>
      </div>
    </motion.div>
  );
}
