const fs = require('fs');

const records = JSON.parse(fs.readFileSync('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/parsed_records.json', 'utf8'));

// Sort by date ascending to process day-by-day
records.sort((a, b) => new Date(a.date) - new Date(b.date));

let totalPredictions = 0;
let hits = 0;

for (let i = 0; i < records.length - 1; i++) {
    const current = records[i];
    const next = records[i + 1];

    if (!current.gm || !current.ls3 || !next.ls1 || !next.ls2 || !next.ls3) continue;

    // GM and LS3 Open digits sum
    const gmOpen = parseInt(current.gm[0]);
    const ls3Open = parseInt(current.ls3[0]);

    if (isNaN(gmOpen) || isNaN(ls3Open)) continue;

    const sum = gmOpen + ls3Open;
    const haroofs = String(sum).split('').map(d => parseInt(d));

    // Next day target Close digits
    const nextLs1Close = parseInt(next.ls1[1]);
    const nextLs2Close = parseInt(next.ls2[1]);
    const nextLs3Close = parseInt(next.ls3[1]);

    const targetCloseDigits = [nextLs1Close, nextLs2Close, nextLs3Close];

    const isHit = haroofs.some(h => targetCloseDigits.includes(h));

    totalPredictions++;
    if (isHit) hits++;
}

console.log(`--- GM+LS3 Master Haroof Trick Analysis ---`);
console.log(`Total Records Analyzed: ${records.length}`);
console.log(`Total Valid Prediction Windows: ${totalPredictions}`);
console.log(`Hits: ${hits}`);
console.log(`Hit Rate: ${((hits / totalPredictions) * 100).toFixed(2)}%`);
console.log(`------------------------------------------`);
