const fs = require('fs');

const records = JSON.parse(fs.readFileSync('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'utf8'));

// Sort by date ascending
records.sort((a, b) => new Date(a.date) - new Date(b.date));

function getRashi(digit) {
    const rashiMap = { 0: 5, 1: 6, 2: 7, 3: 8, 4: 9, 5: 0, 6: 1, 7: 2, 8: 3, 9: 4 };
    return rashiMap[digit];
}

function checkHit(digits, record) {
    if (!record) return false;
    const closeDigits = [
        parseInt(record.ls1[1]),
        parseInt(record.ls2[1]),
        parseInt(record.ls3[1])
    ];
    return digits.some(d => closeDigits.includes(d));
}

let total = 0;
let nextDayHits = 0;
let next2DaysHits = 0;
let next3DaysHits = 0;

for (let i = 0; i < records.length - 3; i++) {
    const current = records[i];
    
    if (!current.gm || !current.ls3) continue;

    const gmOpen = parseInt(current.gm[0]);
    const ls3Open = parseInt(current.ls3[0]);
    if (isNaN(gmOpen) || isNaN(ls3Open)) continue;

    const sum = gmOpen + ls3Open;
    const digits = [...new Set(String(sum).padStart(2, '0').split('').map(Number))];
    const digitsWithRashi = [...new Set(digits.flatMap(d => [d, getRashi(d)]))];

    total++;
    
    const hitDay1 = checkHit(digitsWithRashi, records[i+1]);
    const hitDay2 = checkHit(digitsWithRashi, records[i+2]);
    const hitDay3 = checkHit(digitsWithRashi, records[i+3]);

    if (hitDay1) nextDayHits++;
    if (hitDay1 || hitDay2) next2DaysHits++;
    if (hitDay1 || hitDay2 || hitDay3) next3DaysHits++;
}

console.log(`--- GM+LS3 Master Haroof Trick (Multi-Day Analysis) ---`);
console.log(`Total Windows: ${total}`);
console.log(`Hit on Next Day: ${((nextDayHits / total) * 100).toFixed(2)}%`);
console.log(`Hit within 2 Days: ${((next2DaysHits / total) * 100).toFixed(2)}%`);
console.log(`Hit within 3 Days: ${((next3DaysHits / total) * 100).toFixed(2)}%`);
console.log(`*Note: Using Rashi (Home) digits + Close Side target.*`);
console.log(`------------------------------------------------------`);
