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

    // A very flexible regex to find:
    // 1. Date (DD/MM or DD.MM)
    // 2. A bunch of numbers separated by dots or double dots
    // 3. A day of the week at the end
    
    // Look for the date at the start
    const dateMatch = line.match(/^(\d{2})[\/\.](\d{2})/);
    if (!dateMatch) return;

    const day = dateMatch[1];
    const month = dateMatch[2];

    // Remove the date part and any leading dots
    let rest = line.slice(dateMatch[0].length).replace(/^[\.\s]+/, '');

    // Extract everything before the day name
    // The day name is usually at the end, prefixed by dots
    const parts = rest.split(/\.\./);
    
    let rawNumbers = '';
    let dayOfWeek = '';

    if (parts.length >= 2) {
        rawNumbers = parts[0];
        dayOfWeek = parts[parts.length - 1].trim();
    } else {
        // Fallback for lines like 09/04.65.62.71.56.45.Thur
        const segments = rest.split('.');
        if (segments.length >= 6) {
            dayOfWeek = segments[segments.length - 1].trim();
            rawNumbers = segments.slice(0, segments.length - 1).join('.');
        }
    }

    if (!rawNumbers) return;

    // Clean up rawNumbers to get exactly 5 numbers
    const values = rawNumbers.split('.')
        .map(v => v.trim())
        .filter(v => v.length > 0 && !isNaN(v));

    if (values.length >= 5) {
        const dateStr = `${currentYear}-${month}-${day}`;
        const displayDate = `${day}-${month}-${currentYear.slice(2)}`;

        records.push({
            date: dateStr,
            display_date: displayDate,
            gm: values[0].padStart(2, '0'),
            ls1: values[1].padStart(2, '0'),
            ak: values[2].padStart(2, '0'),
            ls2: values[3].padStart(2, '0'),
            ls3: values[4].padStart(2, '0'),
            day: dayOfWeek || '??'
        });
    }
});

// Remove duplicates by date
const uniqueRecords = [];
const seenDates = new Set();
records.forEach(r => {
    if (!seenDates.has(r.date)) {
        uniqueRecords.push(r);
        seenDates.add(r.date);
    }
});

// Sort records by date
uniqueRecords.sort((a, b) => new Date(a.date) - new Date(b.date));

fs.writeFileSync('frontend/src/parsed_records.json', JSON.stringify(uniqueRecords, null, 2));
console.log(`Successfully parsed ${uniqueRecords.length} unique records into frontend/src/parsed_records.json`);
