const fs = require('fs');

const content = fs.readFileSync('c:\\Users\\Muhammad.Umair\\Desktop\\akwebapp\\Records.txt', 'utf8');
const lines = content.split('\n');
const results = [];

let currentYear = '2025'; // Default starting year

lines.forEach(line => {
    line = line.trim();
    if (!line) return;

    // Detect year changes if any
    if (line.includes('2026')) currentYear = '2026';
    if (line.includes('2025')) currentYear = '2025';

    // Regex to match the pattern: DD/MM..VAL1.VAL2.VAL3.VAL4.VAL5..DAY
    // Some lines use . instead of / or have different separators
    const match = line.match(/^(\d{2})[\/\.](\d{2})[\.\s]+(\d{2})[\.\s]+(\d{2})[\.\s]+(\d{2})[\.\s]+(\d{2})[\.\s]+(\d{2})[\.\s]*([A-Za-z]{3})/);
    
    if (match) {
        const day = match[1];
        const month = match[2];
        const date = `${currentYear}-${month}-${day}`;
        results.push({
            date,
            gm: match[3],
            ls1: match[4],
            ak: match[5],
            ls2: match[6],
            ls3: match[7],
            day: match[8],
            values: [match[3], match[4], match[5], match[6], match[7]]
        });
    } else {
        // Try fallback for different separators or 5 numbers
        const parts = line.split(/[\s\.\/]+/).filter(p => p.length > 0);
        if (parts.length >= 7 && /^\d{2}$/.test(parts[0]) && /^\d{2}$/.test(parts[1])) {
            const day = parts[0];
            const month = parts[1];
            const vals = parts.slice(2, 7).filter(v => /^\d{2}$/.test(v));
            const dayName = parts.find(p => ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Tues', 'The', 'Thur', 'Fir'].includes(p));
            
            if (vals.length === 5 && dayName) {
                const date = `${currentYear}-${month}-${day}`;
                results.push({
                    date,
                    gm: vals[0],
                    ls1: vals[1],
                    ak: vals[2],
                    ls2: vals[3],
                    ls3: vals[4],
                    day: dayName,
                    values: vals
                });
            }
        }
    }
});

fs.writeFileSync('c:\\Users\\Muhammad.Umair\\Desktop\\akwebapp\\frontend\\src\\parsed_records.json', JSON.stringify(results, null, 2));
console.log(`Successfully parsed ${results.length} records.`);
