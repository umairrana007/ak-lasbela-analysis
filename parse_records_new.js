const fs = require('fs');

const content = fs.readFileSync('Records.txt', 'utf8');
const lines = content.split('\n');

const records = [];
let currentYear = '2025';

lines.forEach(line => {
    line = line.trim();
    if (!line) return;

    // Detect year headers
    if (line.includes('2026')) {
        currentYear = '2026';
        return;
    }
    if (line.includes('2025')) {
        currentYear = '2025';
        return;
    }

    // Match patterns like: 01/01..61.46.61.47.64..Wed
    // The format is: DD/MM..V1.V2.V3.V4.V5..Day
    // Some lines have extra dots or spaces
    const match = line.match(/^(\d{2})[\/\.](\d{2}).*?\.\.([\d\.\sA-Za-z_-]+)\.\.(.*)$/);
    
    if (match) {
        const day = match[1];
        const month = match[2];
        const rawPart = match[3];
        const dayOfWeek = match[4].trim();

        // If rawPart contains "off" or "Game Off", it's a holiday
        if (rawPart.toLowerCase().includes('off')) {
            return; 
        }

        const rawValues = rawPart.split('.').map(v => v.trim()).filter(v => v.length > 0 && !isNaN(v));
        
        if (rawValues.length >= 5) {
            const dateStr = `${currentYear}-${month}-${day}`;
            const displayDate = `${day}-${month}-${currentYear.slice(2)}`;

            records.push({
                date: dateStr,
                display_date: displayDate,
                gm: rawValues[0].padStart(2, '0'),
                ls1: rawValues[1].padStart(2, '0'),
                ak: rawValues[2].padStart(2, '0'),
                ls2: rawValues[3].padStart(2, '0'),
                ls3: rawValues[4].padStart(2, '0'),
                values: rawValues.slice(0, 5).map(v => v.padStart(2, '0')),
                day: dayOfWeek
            });
        }
    }
});

// Sort records by date
records.sort((a, b) => new Date(a.date) - new Date(b.date));

fs.writeFileSync('frontend/src/parsed_records.json', JSON.stringify(records, null, 2));
console.log(`Successfully parsed ${records.length} valid records into frontend/src/parsed_records.json`);

