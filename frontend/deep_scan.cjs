const fs = require('fs');
const path = require('path');

const recordsPath = path.join(__dirname, '..', 'Records.txt');
const content = fs.readFileSync(recordsPath, 'utf8');

const jsonPath = path.join(__dirname, 'src', 'parsed_records.json');
const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
const parsedDates = new Set(data.map(r => r.date));

const allLines = content.split('\n').map(l => l.trim()).filter(l => l);

// Range: 2025-01-01 to 2026-04-09
const start = new Date('2025-01-01');
const end = new Date('2026-04-09');

const realMissing = [];
const offDays = [];

let current = new Date(start);
while (current <= end) {
    const d = String(current.getDate()).padStart(2, '0');
    const m = String(current.getMonth() + 1).padStart(2, '0');
    const searchStr = `${d}/${m}`;
    
    // Check if this date (DD/MM) appears in the file
    // We need to be careful about which year we are in.
    // For now, let's just see if the date string exists.
    const hasLine = allLines.some(line => line.startsWith(searchStr));
    const hasData = parsedDates.has(current.toISOString().split('T')[0]);

    if (!hasLine) {
        realMissing.push(current.toISOString().split('T')[0]);
    } else if (!hasData) {
        offDays.push(current.toISOString().split('T')[0]);
    }
    
    current.setDate(current.getDate() + 1);
}

console.log("--- ANALYSIS ---");
console.log(`Real Missing (No line in file): ${realMissing.length}`);
if (realMissing.length > 0) console.log(JSON.stringify(realMissing, null, 2));

console.log(`Off Days (Line exists but no numbers): ${offDays.length}`);
if (offDays.length > 0) console.log(JSON.stringify(offDays, null, 2));
