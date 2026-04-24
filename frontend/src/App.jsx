import React, { useState, useEffect, useRef, useMemo } from 'react';
import { collection, query, orderBy, limit, onSnapshot, doc, setDoc, deleteDoc } from "firebase/firestore";
import { db } from "./firebase";
import parsedRecords from "./parsed_records.json";
import predictionsData from "./predictions.json";

// High Accuracy Lookup (Calculated from 450+ records)
// Accuracy lookup removed (unused)

// GMLSTrick and TripleX helper functions removed (unused)




const InvestmentTracker = () => {
    const plan = [
        { game: 'GM', budget: 300, main_stake: 50, support_stake: 25, open_stake: 100 },
        { game: 'LS1', budget: 300, main_stake: 50, support_stake: 25, open_stake: 100 },
        { game: 'AK', budget: 300, main_stake: 50, support_stake: 25, open_stake: 100 },
        { game: 'LS2', budget: 300, main_stake: 50, support_stake: 25, open_stake: 100 },
        { game: 'LS3', budget: 300, main_stake: 50, support_stake: 25, open_stake: 100 },
    ];

    const totalInvested = plan.reduce((sum, p) => sum + p.budget, 0);
    
    // Calculation: (Stake / 10) * 800 for Jori | (Stake / 100) * 900 for Open
    const calculateReturn = (type, stake) => {
        if (type === 'jori') return (stake / 10) * 800;
        if (type === 'open') return (stake / 100) * 900;
        return 0;
    };

    return (
        <div className="neural-card glow-green" style={{
            background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1) 0%, rgba(15, 23, 42, 0.95) 100%)',
            border: '1px solid rgba(34, 197, 94, 0.4)',
            marginBottom: '25px'
        }}>
            <div className="neural-title" style={{color: '#4ade80', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <span style={{display: 'flex', alignItems: 'center', gap: '10px'}}>
                    <span style={{fontSize: '1.2em'}}>💰</span> REAL-TIME INVESTMENT TRACKER
                </span>
                <span style={{fontSize: '0.8em', color: '#fff', fontWeight: '900', background: 'rgba(34, 197, 94, 0.2)', padding: '4px 12px', borderRadius: '20px'}}>LIVE ROI ANALYSIS</span>
            </div>
            
            <div className="analysis-grid" style={{gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '20px'}}>
                <div style={{background: 'rgba(0,0,0,0.4)', padding: '20px', borderRadius: '15px', border: '1px solid rgba(255,255,255,0.1)'}}>
                    <div style={{fontSize: '0.8em', color: '#94a3b8', textTransform: 'uppercase', marginBottom: '10px'}}>Daily Exposure</div>
                    <div style={{fontSize: '2.5em', fontWeight: '950', color: '#fff'}}>Rs {totalInvested}</div>
                    <div style={{fontSize: '0.7em', color: '#ef4444', marginTop: '5px'}}>Total Risk Amount for 5 Games</div>
                </div>

                <div style={{background: 'rgba(0,0,0,0.4)', padding: '20px', borderRadius: '15px', border: '1px solid rgba(74, 222, 128, 0.2)'}}>
                    <div style={{fontSize: '0.8em', color: '#4ade80', textTransform: 'uppercase', marginBottom: '10px'}}>Max Winning Potential</div>
                    <div style={{fontSize: '2.5em', fontWeight: '950', color: '#4ade80'}}>Rs {calculateReturn('jori', 50)}</div>
                    <div style={{fontSize: '0.7em', color: '#94a3b8', marginTop: '5px'}}>Per Main Jori Hit (on Rs 50)</div>
                </div>

                <div style={{background: 'rgba(0,0,0,0.4)', padding: '20px', borderRadius: '15px', border: '1px solid rgba(59, 130, 246, 0.2)'}}>
                    <div style={{fontSize: '0.8em', color: '#60a5fa', textTransform: 'uppercase', marginBottom: '10px'}}>Harf/Open Payout</div>
                    <div style={{fontSize: '2.5em', fontWeight: '950', color: '#60a5fa'}}>Rs {calculateReturn('open', 100)}</div>
                    <div style={{fontSize: '0.7em', color: '#94a3b8', marginTop: '5px'}}>Per Open Figure Hit (on Rs 100)</div>
                </div>
            </div>

            <div style={{marginTop: '20px', padding: '15px', background: 'rgba(255,255,255,0.02)', borderRadius: '10px', border: '1px dashed rgba(255,255,255,0.1)', fontSize: '0.8em', lineHeight: '1.6'}}>
                <div style={{color: '#4ade80', fontWeight: 'bold', marginBottom: '5px'}}>📌 HOW TO CALCULATE PROFIT:</div>
                <ul style={{listStyle: 'none', padding: 0, color: '#cbd5e1'}}>
                    <li>• If 1 Main Jori hits: 4000 - 300 (Game Exp) = <b style={{color: '#fff'}}>Rs 3700 Net Profit</b></li>
                    <li>• If 1 Support Jori hits: 2000 - 300 (Game Exp) = <b style={{color: '#fff'}}>Rs 1700 Net Profit</b></li>
                    <li>• If Open hits: 900 - 300 (Game Exp) = <b style={{color: '#fff'}}>Rs 600 Net Profit</b></li>
                </ul>
            </div>
        </div>
    );
};

const DailyGamePlan = () => {
    const plan = [
        { game: 'GM', primary: ['08', '06', '49'], support: ['48', '59'], open: '0', budget: 300 },
        { game: 'LS1', primary: ['20', '51', '63'], support: ['42', '06'], open: '2', budget: 300 },
        { game: 'AK', primary: ['06', '77', '98'], support: ['90', '12'], open: '0', budget: 300 },
        { game: 'LS2', primary: ['40', '84', '27'], support: ['06', '09'], open: '4', budget: 300 },
        { game: 'LS3', primary: ['35', '03', '70'], support: ['72', '91'], open: '3', budget: 300 },
    ];

    return (
        <div className="neural-card glow-amber" style={{
            background: 'linear-gradient(135deg, rgba(251, 191, 36, 0.1) 0%, rgba(15, 23, 42, 0.9) 100%)',
            border: '2px solid #fbbf24',
            marginBottom: '25px',
            boxShadow: '0 0 30px rgba(251, 191, 36, 0.2)'
        }}>
            <div className="neural-title" style={{color: '#fbbf24', marginBottom: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                <span style={{display: 'flex', alignItems: 'center', gap: '10px'}}>
                    <span style={{fontSize: '1.2em'}}>📅</span> DAILY MASTER INVESTMENT PLAN (24 APRIL)
                </span>
                <span style={{fontSize: '0.65em', background: '#fbbf24', color: '#000', padding: '4px 12px', borderRadius: '20px', fontWeight: '900'}}>TOTAL BUDGET: Rs 1500</span>
            </div>
            <div className="analysis-grid" style={{gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))'}}>
                {plan.map(p => (
                    <div key={p.game} style={{background: 'rgba(0,0,0,0.5)', padding: '15px', borderRadius: '15px', border: '1px solid rgba(251, 191, 36, 0.3)', position: 'relative'}}>
                        <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '12px', borderBottom: '1px solid rgba(251, 191, 36, 0.2)', paddingBottom: '8px'}}>
                            <span style={{fontSize: '1.2em', fontWeight: '950', color: '#fbbf24'}}>{p.game}</span>
                            <span style={{fontSize: '0.7em', color: '#4ade80', fontWeight: 'bold'}}>Limit: Rs {p.budget}</span>
                        </div>
                        
                        <div style={{marginBottom: '10px'}}>
                            <div style={{fontSize: '0.6em', color: '#fff', opacity: 0.7, textTransform: 'uppercase', marginBottom: '5px'}}>Main Jori (Rs 50 each)</div>
                            <div style={{display: 'flex', gap: '6px', flexWrap: 'wrap'}}>
                                {p.primary.map(j => (
                                    <span key={j} style={{background: '#fbbf24', color: '#000', padding: '4px 10px', borderRadius: '6px', fontWeight: '950', fontSize: '1.1em'}}>{j}</span>
                                ))}
                            </div>
                        </div>

                        <div style={{marginBottom: '10px'}}>
                            <div style={{fontSize: '0.6em', color: '#fff', opacity: 0.7, textTransform: 'uppercase', marginBottom: '5px'}}>Backup Jori (Rs 25 each)</div>
                            <div style={{display: 'flex', gap: '6px', flexWrap: 'wrap'}}>
                                {p.support.map(j => (
                                    <span key={j} style={{background: 'rgba(255,255,255,0.1)', color: '#fff', padding: '3px 8px', borderRadius: '4px', fontWeight: 'bold', fontSize: '0.9em', border: '1px solid rgba(255,255,255,0.2)'}}>{j}</span>
                                ))}
                            </div>
                        </div>

                        <div style={{background: 'rgba(251, 191, 36, 0.1)', padding: '8px', borderRadius: '8px', display: 'flex', justifyContent: 'space-between', alignItems: 'center'}}>
                            <span style={{fontSize: '0.7em', color: '#fbbf24', fontWeight: 'bold'}}>OPEN FIGURE (Rs 100)</span>
                            <span style={{fontSize: '1.4em', fontWeight: '950', color: '#fff', textShadow: '0 0 10px #fbbf24'}}>{p.open}</span>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

const App = () => {
  const [records, setRecords] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editIndex, setEditIndex] = useState('-1');
  const [predictions, setPredictions] = useState(predictionsData);
  const [isAdmin, setIsAdmin] = useState(false);
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [loginPass, setLoginPass] = useState('');
  const [isSyncing, setIsSyncing] = useState(false);
  const [visibleRecords, setVisibleRecords] = useState(20);
  const [syncStatus, setSyncStatus] = useState('');
  const [formData, setFormData] = useState({ date: '', day: '', gm: '', ls1: '', ak: '', ls2: '', ls3: '' });

  const fileInputRef = useRef(null);
  
  // detectExpertLogic removed (unused)

  // 1. Memoized Filtered Records (prevents lag on scroll/re-render)
  const filteredRecords = useMemo(() => {
    return records.filter(record => {
        if (!searchTerm) return true;
        const term = searchTerm.toLowerCase();
        return (record.date && record.date.includes(term)) ||
               (record.day && record.day.toLowerCase().includes(term)) ||
               String(record.gm) === term ||
               String(record.ls1) === term ||
               String(record.ak) === term ||
               String(record.ls2) === term ||
               String(record.ls3) === term;
    });
  }, [records, searchTerm]);

  // 2. Memoized Neural Stats (Heavy calculation on 4000+ records)
  // Neural stats, Heatmap, and Odd/Even calculations removed (unused in current UI)
  
  // allExpertSignals removed (unused)



  // NOTE: calculateNeuralStats, calculateOddEvenDistribution, calculateDigitHeatmap
  // were removed — they called non-existent state setters (setNeuralStats, setOddEvenStats, setHeatmapData)
  // causing React to crash. These are now handled by useMemo hooks above (neuralStats, oddEvenStats, heatmapData).

  useEffect(() => {
    // We fetch from firebase, but we also append parsed_records.
    const q = query(collection(db, "draws"), orderBy("date", "desc"), limit(100));
    const unsubscribe = onSnapshot(q, (snapshot) => {
      const data = [];
      snapshot.forEach((doc) => data.push({ id: doc.id, ...doc.data(), isFirebase: true }));
      
      const firebaseDates = new Set(data.map(r => r.date));

      // Combine with parsedRecords, skipping ones already in Firebase
      const historicalData = parsedRecords
        .filter(r => !firebaseDates.has(r.date))
        .map(r => ({ ...r, id: `hist-${r.date}`, isFirebase: false }));

      const combined = [...data, ...historicalData]
        .sort((a, b) => new Date(b.date) - new Date(a.date));
      
      setRecords(combined);
    });
    return () => unsubscribe();
  }, []);

  useEffect(() => {
    // Live listener for AI Predictions
    const unsubPreds = onSnapshot(doc(db, "metadata", "predictions"), (snapshot) => {
        if (snapshot.exists()) {
            const data = snapshot.data();
            console.log("AI Predictions Updated:", data);
            setPredictions(prev => ({
                ...prev,
                ...data
            }));
        }
    });
    return () => unsubPreds();
  }, []);


  const formatDate = (dateString) => {
    const date = new Date(dateString);
    if (isNaN(date.getTime())) return dateString;
    const day = String(date.getDate()).padStart(2, '0');
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const year = String(date.getFullYear()).slice(-2);
    return `${day}/${month}/${year}`;
  };

  const updateStats = () => {
    const total = records.length;
    const now = new Date();
    const thisMonth = records.filter(r => {
        const rDate = new Date(r.date);
        return rDate.getMonth() === now.getMonth() && 
               rDate.getFullYear() === now.getFullYear();
    }).length;

    let lastRecord = '-';
    if (records.length > 0) {
        lastRecord = new Date(records[0].date).toLocaleDateString('en-US', { 
            day: '2-digit', 
            month: 'short' 
        });
    }

    return { total, thisMonth, lastRecord };
  };

  const stats = updateStats();

  const handleAdminLogin = () => {
    setShowLoginModal(true);
  };

  const submitLogin = (e) => {
    if (e) e.preventDefault();
    if (loginPass === "admin786") {
        setIsAdmin(true);
        setShowLoginModal(false);
        setLoginPass('');
        alert("Admin Mode Activated!");
    } else {
        alert("Wrong Password!");
    }
  };

  const handleOpenModal = () => {
    setShowModal(true);
    setFormData({ date: '', day: '', gm: '', ls1: '', ak: '', ls2: '', ls3: '' });
    setEditIndex('-1');
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const docId = formData.date;
      await setDoc(doc(db, "draws", docId), { 
        ...formData, 
        display_date: formData.date.split('-').reverse().join('-'),
        timestamp: new Date().toISOString() 
      });
      handleCloseModal();
    } catch (err) {
      alert("Error saving record to Firebase: " + err.message);
    }
  };

  const handleEdit = (record) => {
    setEditIndex(record.id);
    setFormData({
      date: record.date,
      day: record.day || '',
      gm: record.gm || '',
      ls1: record.ls1 || '',
      ak: record.ak || '',
      ls2: record.ls2 || '',
      ls3: record.ls3 || ''
    });
    setShowModal(true);
  };

  const triggerSync = async () => {
    setIsSyncing(true);
    setSyncStatus('Triggering AI Sync...');
    try {
      // Secure call — token server-side pe rehta hai, browser ko nahi milta
      const response = await fetch('/api/trigger-sync', { method: 'POST' });
      const data = await response.json();
      if (response.ok) {
        setSyncStatus('✅ AI Sync Started! Check back in 2-3 mins.');
      } else {
        setSyncStatus('❌ Sync failed: ' + (data.error || 'Unknown error'));
      }
    } catch {
      setSyncStatus('❌ Network error. Try again!');
    } finally {
      setIsSyncing(false);
      setTimeout(() => setSyncStatus(''), 6000);
    }
  };

  const handleDelete = async (record) => {
    if (!record.isFirebase) {
        alert("Historical records from JSON cannot be deleted.");
        return;
    }
    if (window.confirm('Are you sure you want to delete this record?')) {
        try {
            await deleteDoc(doc(db, "draws", record.id));
        } catch {
            alert("Error deleting record.");
        }
    }
  };

  const exportToCSV = () => {
    if (records.length === 0) {
        alert('No records to export!');
        return;
    }

    let csv = 'Date,Day,GM,LS1,AK,LS2,LS3\n';
    records.forEach(record => {
        csv += `${record.date},${record.day},${record.gm || ''},${record.ls1 || ''},${record.ak || ''},${record.ls2 || ''},${record.ls3 || ''}\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `ak_lasbela_records_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    window.URL.revokeObjectURL(url);
  };

  const importFromFile = (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const reader = new FileReader();
    reader.onload = async function(event) {
        const text = event.target.result;
        const lines = text.split('\n');
        let imported = 0;
        let currentYear = new Date().getFullYear();

        for (const line of lines) {
            const trimmed = line.trim();
            if (!trimmed) continue;
            
            // Year detection
            const yearMatch = trimmed.match(/(\d{4})/);
            if (yearMatch && (trimmed.includes('-') || trimmed.includes('20'))) {
                currentYear = yearMatch[1];
                continue;
            }

            const dateMatch = trimmed.match(/^(\d{2})[/.](\d{2})/);
            if (!dateMatch) continue;
            
            const dayNum = dateMatch[1];
            const monthNum = dateMatch[2];
            const remainingText = trimmed.slice(5);
            const numbers = remainingText.match(/\d{2}/g) || [];
            
            const daysList = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Tues', 'Thur', 'Fir'];
            let dayOfWeek = 'Unknown';
            for (const d of daysList) {
                if (trimmed.toLowerCase().includes(d.toLowerCase())) {
                    dayOfWeek = d;
                    break;
                }
            }

            if (numbers.length >= 5) {
                const record = {
                    date: `${currentYear}-${monthNum}-${dayNum}`,
                    day: dayOfWeek,
                    gm: numbers[0],
                    ls1: numbers[1],
                    ak: numbers[2],
                    ls2: numbers[3],
                    ls3: numbers[4]
                };
                
                if (!records.some(r => r.date === record.date)) {
                    await setDoc(doc(db, "draws", record.date), { 
                        ...record, 
                        display_date: `${dayNum}/${monthNum}/${currentYear.slice(-2)}`,
                        timestamp: new Date().toISOString() 
                    });
                    imported++;
                }
            }
        }

        alert(`Successfully imported ${imported} records to Firebase!`);
        e.target.value = '';
    };
    reader.readAsText(file);
  };

  // Removed duplicated filteredRecords logic from here as it's now memoized above

  return (
    <>
        <div className="container">

        {/* YESTERDAY MATCH ALERT - ENHANCED VISIBILITY */}
        {predictions && predictions.yesterday_match && (
            <div className="ai-status-banner yesterday-match-banner" style={{
                background: predictions.yesterday_match.type === 'Direct' 
                    ? 'linear-gradient(90deg, rgba(34, 197, 94, 0.15) 0%, rgba(34, 197, 94, 0.05) 100%)' 
                    : 'linear-gradient(90deg, rgba(99, 102, 241, 0.1) 0%, rgba(99, 102, 241, 0.02) 100%)',
                borderColor: predictions.yesterday_match.type === 'Direct' ? '#22c55e' : '#6366f1',
                borderLeft: '4px solid ' + (predictions.yesterday_match.type === 'Direct' ? '#22c55e' : '#6366f1'),
                marginBottom: '15px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
            }}>
                <div className="status-primary">
                    <span style={{fontSize: '1.5em'}}>{predictions.yesterday_match.type === 'Direct' ? '🔥' : '📡'}</span>
                    <div className="neural-calibration-content">
                        <div style={{fontSize: '0.9em', fontWeight: 'bold', color: predictions.yesterday_match.type === 'Direct' ? '#4ade80' : '#cbd5e1'}}>
                            {predictions.yesterday_match.status}
                        </div>
                        <div style={{fontSize: '0.75em', color: '#94a3b8'}}>{predictions.yesterday_match.details}</div>
                    </div>
                </div>
                {predictions.yesterday_match.type === 'Direct' && (
                    <div className="hit-badge"> Verified Hit </div>
                )}
            </div>
        )}

        <div className="header header-responsive">
            <div className="header-title">🎮 AK Lasbela Records 2025-2026 🎮</div>
            <button 
                className="admin-toggle-btn"
                onClick={isAdmin ? () => setIsAdmin(false) : handleAdminLogin}
            >
                {isAdmin ? '🔓 ADMIN MODE' : '🔒 PUBLIC VIEW'}
            </button>
        </div>

        <div className="stats">
            <div className="stat-card">
                <div className="stat-value" id="totalRecords">{stats.total}</div>
                <div className="stat-label">Total Records</div>
            </div>
            <div className="stat-card">
                <div className="stat-value" id="thisMonth">{stats.thisMonth}</div>
                <div className="stat-label">This Month</div>
            </div>
            <div className="stat-card">
                <div className="stat-value" id="lastRecord">{stats.lastRecord}</div>
                <div className="stat-label">Last Entry</div>
            </div>
        </div>

            {/* ELITE DASHBOARD SECTION */}
            <div className="dashboard-container">

                {/* AI Status Banner */}
                <div className="ai-status-banner">
                    <div className="status-indicator">
                        <div className="pulse"></div>
                        <span>Neural Processing Active</span>
                    </div>
                </div>

                {/* ROW 1: MASTER ACTION CENTER */}
                <div style={{display: 'grid', gridTemplateColumns: '1fr', gap: '25px'}}>
                    {/* MAIN ACTIONABLE PLAN */}
                    <DailyGamePlan />
                    
                    {/* INVESTMENT TRACKER */}
                    <InvestmentTracker />


                </div>


                <div className="resync-container" style={{display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '15px', padding: '0 5px'}}>
                    <div style={{fontSize: '0.75em', opacity: 0.6, fontStyle: 'italic'}}>*Quantum Intelligence Sync Active</div>
                    <div style={{display: 'flex', alignItems: 'center', gap: '15px'}}>
                        {predictions.last_updated && (
                            <div style={{fontSize: '0.65em', color: '#666', fontWeight: 'bold'}}>
                                Last Re-Sync: {new Date(predictions.last_updated).toLocaleString()}
                            </div>
                        )}
                        <button className={`btn ${isSyncing ? 'btn-disabled' : 'btn-primary'}`} onClick={triggerSync} disabled={isSyncing} style={{padding: '6px 18px', fontSize: '0.85em', fontWeight: '900'}}>
                            {isSyncing ? 'Synchronizing...' : '⚡ Re-Sync Neural Hub'}
                        </button>
                    </div>
                </div>
        </div>

        {isAdmin && (
            <div className="controls">
                <div className="search-box">
                    <input 
                        type="text" 
                        id="searchInput" 
                        placeholder="🔍 Search by date or number..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
                <div className="import-export">
                    <button className="btn btn-primary" onClick={handleOpenModal}>➕ Add Record</button>
                    <button className="btn btn-success" onClick={exportToCSV}>📥 Export CSV</button>
                    <button className="btn btn-primary" onClick={() => fileInputRef.current.click()}>📤 Import CSV</button>
                    <input 
                        type="file" 
                        id="fileInput" 
                        className="file-input" 
                        accept=".csv,.txt" 
                        ref={fileInputRef}
                        onChange={importFromFile}
                    />
                </div>
            </div>
        )}

        {!isAdmin && (
            <div className="controls" style={{justifyContent: 'center'}}>
                <div className="search-box" style={{maxWidth: '600px'}}>
                    <input 
                        type="text" 
                        id="searchInput" 
                        placeholder="🔍 Search historical results..."
                        value={searchTerm}
                        onChange={(e) => setSearchTerm(e.target.value)}
                    />
                </div>
            </div>
        )}

        <div className="table-container">
            <table id="recordsTable">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th className="gm-column">GM</th>
                        <th className="ls1-column">LS1</th>
                        <th className="ak-column">AK</th>
                        <th className="ls2-column">LS2</th>
                        <th className="ls3-column">LS3</th>
                        <th>Day</th>
                        {isAdmin && <th>Actions</th>}
                    </tr>
                </thead>
                <tbody id="tableBody">
                    {filteredRecords.length > 0 ? filteredRecords.slice(0, visibleRecords).map((record, index) => (
                        <tr key={record.id || index}>
                            <td className="date-column">{formatDate(record.date)}</td>
                            <td className="gm-column">{record.gm || '-'}</td>
                            <td className="ls1-column">{record.ls1 || '-'}</td>
                            <td className="ak-column">{record.ak || '-'}</td>
                            <td className="ls2-column">{record.ls2 || '-'}</td>
                            <td className="ls3-column">{record.ls3 || '-'}</td>
                            <td className="day-column">{record.day}</td>
                            {isAdmin && (
                                <td className="action-buttons">
                                    <button className="btn btn-edit" onClick={() => handleEdit(record)}>✏️</button>
                                    <button className="btn btn-danger" onClick={() => handleDelete(record)}>🗑️</button>
                                </td>
                            )}
                        </tr>
                    )) : (
                        <tr>
                            <td colSpan="8">
                                <div id="noData" className="no-data">
                                    No records found. Click "Add Record" to create one!
                                </div>
                            </td>
                        </tr>
                    )}
                </tbody>
            </table>

            {visibleRecords < filteredRecords.length && (
                <div style={{textAlign: 'center', marginTop: '20px', paddingBottom: '40px'}}>
                    <button 
                        className="btn btn-primary" 
                        onClick={() => setVisibleRecords(prev => prev + 50)}
                        style={{padding: '12px 40px', fontSize: '1.1em', fontWeight: '900', background: 'linear-gradient(135deg, #3b82f6 0%, #2563eb 100%)', border: 'none', boxShadow: '0 4px 15px rgba(59, 130, 246, 0.3)'}}
                    >
                        📂 Show More Records ({filteredRecords.length - visibleRecords} Remaining)
                    </button>
                </div>
            )}
        </div>
        </div>

        {/* Modal for Admin Login */}
        {showLoginModal && (
            <div className="modal show" onClick={() => setShowLoginModal(false)}>
                <div className="modal-content" style={{maxWidth: '400px'}} onClick={e => e.stopPropagation()}>
                    <span className="close" onClick={() => setShowLoginModal(false)}>&times;</span>
                    <h2>🔓 Admin Login</h2>
                    <p style={{fontSize: '0.8em', opacity: 0.7, marginBottom: '20px'}}>Enter password to unlock edit/delete controls.</p>
                    <form onSubmit={submitLogin}>
                        <div className="form-group">
                            <label>Password</label>
                            <input 
                                type="password" 
                                value={loginPass}
                                onChange={(e) => setLoginPass(e.target.value)}
                                placeholder="••••••••"
                                autoFocus
                                style={{
                                    width: '100%',
                                    padding: '12px',
                                    background: 'rgba(0,0,0,0.2)',
                                    border: '1px solid rgba(255,255,255,0.1)',
                                    borderRadius: '8px',
                                    color: '#fff',
                                    fontSize: '1.2em',
                                    textAlign: 'center',
                                    letterSpacing: '5px'
                                }}
                            />
                        </div>
                        <div className="modal-actions" style={{marginTop: '20px'}}>
                            <button type="button" className="btn" onClick={() => setShowLoginModal(false)}>Cancel</button>
                            <button type="submit" className="btn btn-primary" style={{flex: 1}}>Login</button>
                        </div>
                    </form>
                </div>
            </div>
        )}

        {/* Modal for Add/Edit */}
        <div id="recordModal" className={`modal ${showModal ? 'show' : ''}`} onClick={(e) => { if(e.target.className.includes('modal ')) handleCloseModal(); }}>
            <div className="modal-content" onClick={e => e.stopPropagation()}>
                <span className="close" onClick={handleCloseModal}>&times;</span>
                <div className="modal-header" id="modalTitle">{editIndex === '-1' ? 'Add New Record' : 'Edit Record'}</div>
                <form id="recordForm" onSubmit={handleSubmit}>
                    <input type="hidden" id="editIndex" value={editIndex} />
                    <div className="form-row">
                        <div className="form-group">
                            <label>Date *</label>
                            <input 
                                type="date" 
                                id="date" 
                                required 
                                value={formData.date}
                                onChange={e => setFormData({...formData, date: e.target.value})}
                                disabled={editIndex !== '-1'}
                            />
                        </div>
                        <div className="form-group">
                            <label>Day *</label>
                            <select 
                                id="day" 
                                required
                                value={formData.day}
                                onChange={e => setFormData({...formData, day: e.target.value})}
                            >
                                <option value="">Select Day</option>
                                <option value="Monday">Monday</option>
                                <option value="Tuesday">Tuesday</option>
                                <option value="Wednesday">Wednesday</option>
                                <option value="Thursday">Thursday</option>
                                <option value="Friday">Friday</option>
                                <option value="Saturday">Saturday</option>
                                <option value="Sunday">Sunday</option>
                            </select>
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-group">
                            <label>GM</label>
                            <input 
                                type="number" 
                                id="gm" 
                                min="0" 
                                max="99" 
                                placeholder="00-99"
                                value={formData.gm}
                                onChange={e => setFormData({...formData, gm: e.target.value})}
                            />
                        </div>
                        <div className="form-group">
                            <label>LS1</label>
                            <input 
                                type="number" 
                                id="ls1" 
                                min="0" 
                                max="99" 
                                placeholder="00-99"
                                value={formData.ls1}
                                onChange={e => setFormData({...formData, ls1: e.target.value})}
                            />
                        </div>
                    </div>
                    <div className="form-row">
                        <div className="form-group">
                            <label>AK</label>
                            <input 
                                type="number" 
                                id="ak" 
                                min="0" 
                                max="99" 
                                placeholder="00-99"
                                value={formData.ak}
                                onChange={e => setFormData({...formData, ak: e.target.value})}
                            />
                        </div>
                        <div className="form-group">
                            <label>LS2</label>
                            <input 
                                type="number" 
                                id="ls2" 
                                min="0" 
                                max="99" 
                                placeholder="00-99"
                                value={formData.ls2}
                                onChange={e => setFormData({...formData, ls2: e.target.value})}
                            />
                        </div>
                    </div>
                    <div className="form-group">
                        <label>LS3</label>
                        <input 
                            type="number" 
                            id="ls3" 
                            min="0" 
                            max="99" 
                            placeholder="00-99"
                            value={formData.ls3}
                            onChange={e => setFormData({...formData, ls3: e.target.value})}
                        />
                    </div>
                    <button type="submit" className="btn btn-primary" style={{width: '100%', marginTop: '10px'}}>
                        💾 Save Record
                    </button>
                </form>
            </div>
        </div>
    </>
  );
}

export default App;
