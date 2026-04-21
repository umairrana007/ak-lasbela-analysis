const fs = require('fs');

const records = JSON.parse(fs.readFileSync('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'utf8'));

// Sort by date ascending
records.sort((a, b) => new Date(a.date) - new Date(b.date));

function getRashi(digit) {
    const rashiMap = { 0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4 };
    return rashiMap[digit];
}

let total = 0;
let hitsSimple = 0;
let hitsWithRashi = 0;

for (let i = 0; i < records.length - 1; i++) {
    const current = records[i];
    const next = records[i + 1];

    if (!current.gm || !current.ls3 || !next.ls1 || !next.ls2 || !next.ls3) continue;

    const gmOpen = parseInt(current.gm[0]);
    const ls3Open = parseInt(current.ls3[0]);

    if (isNaN(gmOpen) || isNaN(ls3Open)) continue;

    const sum = gmOpen + ls3Open;
    const s_str = String(sum).padStart(2, '0');
    const digits = [...new Set(s_str.split('').map(Number))];
    
    const digitsWithRashi = [...new Set(digits.flatMap(d => [d, getRashi(d)]))];

    const nextCloseDigits = [
        parseInt(next.ls1[1]),
        parseInt(next.ls2[1]),
        parseInt(next.ls3[1])
    ];

    total++;
    if (digits.some(d => nextCloseDigits.includes(d))) hitsSimple++;
    if (digitsWithRashi.some(d => nextCloseDigits.includes(d))) hitsWithRashi++;
}

console.log(`--- GM+LS3 Master Haroof Trick Performance (Historical) ---`);
console.log(`Total Windows Analyzed: ${total}`);
console.log(`Simple Hit Rate: ${((hitsSimple / total) * 100).toFixed(2)}%`);
console.log(`Hit Rate with Rashi (Home): ${((hitsWithRashi / total) * 100).toFixed(2)}%`);
console.log(`---------------------------------------------------------`);
