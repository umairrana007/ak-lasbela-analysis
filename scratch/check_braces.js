const fs = require('fs');
const content = fs.readFileSync('c:/Users/Muhammad.Umair/Desktop/akwebapp/frontend/src/App.jsx', 'utf8');

function count(str, sub) {
    let count = 0;
    let pos = 0;
    while ((pos = str.indexOf(sub, pos)) !== -1) {
        count++;
        pos += sub.length;
    }
    return count;
}

console.log('--- HTML TAGS ---');
console.log('Open <div:', count(content, '<div'));
console.log('Close </div>:', count(content, '</div>'));

console.log('\n--- BRACKETS ---');
console.log('Open {:', count(content, '{'));
console.log('Close }:', count(content, '}'));

console.log('\n--- PARENTHESES ---');
console.log('Open (:', count(content, '('));
console.log('Close ):', count(content, ')'));
