const fs = require('fs');
const path = require('path');

const jsonPath = path.join(__dirname, 'src', 'parsed_records.json');
const data = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));

const existingDates = new Set(data.map(r => r.date));

// Determine range
const dates = data.map(r => new Date(r.date));
const minDate = new Date(Math.min(...dates));
const maxDate = new Date(Math.max(...dates));

console.log(`Checking range: ${minDate.toISOString().split('T')[0]} to ${maxDate.toISOString().split('T')[0]}`);

const missing = [];
let current = new Date(minDate);

while (current <= maxDate) {
    const iso = current.toISOString().split('T')[0];
    if (!existingDates.has(iso)) {
        missing.push(iso);
    }
    current.setDate(current.getDate() + 1);
}

if (missing.length === 0) {
    console.log("No missing dates found in the historical range!");
} else {
    console.log(`Found ${missing.length} missing dates:`);
    console.log(JSON.stringify(missing, null, 2));
}
