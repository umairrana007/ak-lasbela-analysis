import React, { useState, useEffect, useRef } from 'react';
import { collection, query, orderBy, limit, onSnapshot, doc, setDoc, deleteDoc } from "firebase/firestore";
import { db } from "./firebase";
import parsedRecords from "./parsed_records.json";
import predictionsData from "./predictions.json";

const App = () => {
  const [records, setRecords] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [editIndex, setEditIndex] = useState('-1');
  const [neuralStats, setNeuralStats] = useState({ hot: [], cold: [] });
  const [formData, setFormData] = useState({
    date: '', day: '', gm: '', ls1: '', ak: '', ls2: '', ls3: ''
  });
  const [predictions, setPredictions] = useState(predictionsData);
  
  const fileInputRef = useRef(null);

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
      calculateNeuralStats(combined);
    });
    return () => unsubscribe();
  }, []);

  useEffect(() => {
    // Live listener for AI Predictions
    const unsubPreds = onSnapshot(doc(db, "metadata", "predictions"), (snapshot) => {
        if (snapshot.exists()) {
            setPredictions(snapshot.data());
        }
    });
    return () => unsubPreds();
  }, []);

  const calculateNeuralStats = (allRecords) => {
    const counts = {};
    allRecords.forEach(r => {
      ['gm', 'ls1', 'ak', 'ls2', 'ls3'].forEach(key => {
        const val = r[key];
        if (val && val !== '--' && val !== '??' && !isNaN(val) && val.length === 2) {
          counts[val] = (counts[val] || 0) + 1;
        }
      });
    });

    const sorted = Object.entries(counts).sort((a, b) => b[1] - a[1]);
    setNeuralStats({
      hot: sorted.slice(0, 8),
      cold: sorted.slice(-8).reverse()
    });
  };

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
    if (!record.isFirebase) {
        alert("Historical records from JSON cannot be edited directly.");
        return;
    }
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

  const handleDelete = async (record) => {
    if (!record.isFirebase) {
        alert("Historical records from JSON cannot be deleted.");
        return;
    }
    if (window.confirm('Are you sure you want to delete this record?')) {
        try {
            await deleteDoc(doc(db, "draws", record.id));
        } catch (err) {
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

            const dateMatch = trimmed.match(/^(\d{2})[\/.](\d{2})/);
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

  const filteredRecords = records.filter(record => {
      if (!searchTerm) return true;
      const term = searchTerm.toLowerCase();
      return (record.date && record.date.includes(term)) ||
             (record.day && record.day.toLowerCase().includes(term)) ||
             record.gm === term ||
             record.ls1 === term ||
             record.ak === term ||
             record.ls2 === term ||
             record.ls3 === term;
  });

  return (
    <div className="container">
        <div className="header">
            🎮 AK Lasbela Records 2025-2026 🎮
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

        <div className="neural-center">
            <div className="neural-card">
                <div className="neural-title">
                    🧠 Neural Prediction Center
                </div>
                <div className="prediction-grid">
                    <div className="prediction-item">
                        <div className="prediction-label">GM</div>
                        <div className="prediction-value">{predictions.results?.gm?.primary || '??'}</div>
                    </div>
                    <div className="prediction-item">
                        <div className="prediction-label">LS1</div>
                        <div className="prediction-value">{predictions.results?.ls1?.primary || '??'}</div>
                    </div>
                    <div className="prediction-item">
                        <div className="prediction-label">AK</div>
                        <div className="prediction-value">{predictions.results?.ak?.primary || '??'}</div>
                    </div>
                    <div className="prediction-item">
                        <div className="prediction-label">LS2</div>
                        <div className="prediction-value">{predictions.results?.ls2?.primary || '??'}</div>
                    </div>
                    <div className="prediction-item">
                        <div className="prediction-label">LS3</div>
                        <div className="prediction-value">{predictions.results?.ls3?.primary || '??'}</div>
                    </div>
                </div>
                <div style={{marginTop: '15px', fontSize: '0.85em', opacity: 0.8, fontStyle: 'italic'}}>
                    *AI Engine Analysis based on latest trends.
                </div>
            </div>

            <div className="stats-grid">
                <div className="frequency-card">
                    <div className="frequency-title">🔥 Hot Numbers (Frequency)</div>
                    <div className="number-badges">
                        {neuralStats.hot.map(([num, count]) => (
                            <div key={num} className="badge badge-hot">
                                {num}
                                <span className="badge-count">{count}x</span>
                            </div>
                        ))}
                    </div>
                </div>
                <div className="frequency-card">
                    <div className="frequency-title">❄️ Cold Numbers (Gap)</div>
                    <div className="number-badges">
                        {neuralStats.cold.map(([num, count]) => (
                            <div key={num} className="badge badge-cold">
                                {num}
                                <span className="badge-count">{count}x</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </div>

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

        <div className="table-container">
            <table id="recordsTable">
                <thead>
                    <tr>
                        <th>Date</th>
                        <th>Day</th>
                        <th className="gm-column">GM</th>
                        <th className="ls1-column">LS1</th>
                        <th className="ak-column">AK</th>
                        <th className="ls2-column">LS2</th>
                        <th className="ls3-column">LS3</th>
                        <th>Actions</th>
                    </tr>
                </thead>
                <tbody id="tableBody">
                    {filteredRecords.length > 0 ? filteredRecords.map((record, index) => (
                        <tr key={record.id || index}>
                            <td>{formatDate(record.date)}</td>
                            <td>{record.day}</td>
                            <td className="gm-column">{record.gm || '-'}</td>
                            <td className="ls1-column">{record.ls1 || '-'}</td>
                            <td className="ak-column">{record.ak || '-'}</td>
                            <td className="ls2-column">{record.ls2 || '-'}</td>
                            <td className="ls3-column">{record.ls3 || '-'}</td>
                            <td className="action-buttons">
                                {record.isFirebase ? (
                                    <>
                                        <button className="btn btn-edit" onClick={() => handleEdit(record)}>✏️</button>
                                        <button className="btn btn-danger" onClick={() => handleDelete(record)}>🗑️</button>
                                    </>
                                ) : (
                                    <span style={{ fontSize: '0.8em', color: '#999' }}>Historical</span>
                                )}
                            </td>
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
        </div>

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
    </div>
  );
};

export default App;
