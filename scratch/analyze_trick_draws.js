const fs = require('fs');

const records = JSON.parse(fs.readFileSync('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'utf8'));

// Sort by date ascending
records.sort((a, b) => new Date(a.date) - new Date(b.date));

function getRashi(digit) {
    const rashiMap = { 0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4 };
    return rashiMap[digit];
}

function checkHit(digits, record, draws) {
    if (!record) return false;
    const closeDigits = draws.map(d => parseInt(record[d.toLowerCase()][1]));
    return digits.some(d => closeDigits.includes(d));
}

let total = 0;
let ls1Hits = 0;
let ls2Hits = 0;
let ls3Hits = 0;
let comboHits = 0;

for (let i = 0; i < records.length - 1; i++) {
    const current = records[i];
    const next = records[i + 1];
    
    if (!current.gm || !current.ls3 || !next.ls1 || !next.ls2 || !next.ls3) continue;

    const gmOpen = parseInt(current.gm[0]);
    const ls3Open = parseInt(current.ls3[0]);
    const sum = gmOpen + ls3Open;
    const digits = [...new Set(String(sum).padStart(2, '0').split('').map(Number))].flatMap(d => [d, getRashi(d)]);

    total++;
    if (checkHit(digits, next, ['LS1'])) ls1Hits++;
    if (checkHit(digits, next, ['LS2'])) ls2Hits++;
    if (checkHit(digits, next, ['LS3'])) ls3Hits++;
    if (checkHit(digits, next, ['LS1', 'LS2', 'LS3'])) comboHits++;
}

console.log(`--- Individual Draw Hit Rates (Next Day) ---`);
console.log(`LS1 Close Hit Rate: ${((ls1Hits / total) * 100).toFixed(2)}%`);
console.log(`LS2 Close Hit Rate: ${((ls2Hits / total) * 100).toFixed(2)}%`);
console.log(`LS3 Close Hit Rate: ${((ls3Hits / total) * 100).toFixed(2)}%`);
console.log(`Combined (Any of LS1/2/3): ${((comboHits / total) * 100).toFixed(2)}%`);
