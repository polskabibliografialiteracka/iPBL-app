const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
global.window=global;
vm.runInThisContext(fs.readFileSync('js/search-utils.js','utf8'));
const S=global.IPBLSearchUtils;
const rows=S.indexRecords([
 {title:'Raczej szarpnięcie',author:'Honet, Roman | Sala, Zuzanna',authorTerms:[{label:'Honet, Roman'},{label:'Sala, Zuzanna'}]},
 {title:'Książka',author:'Olga Kowalska',authorTerms:[{label:'Olga Kowalska'}]}
]);
for(const q of ['Roman Honet','Honet Roman','Honet, Roman','sala zuzanna','zuzanna sala','RACZEJ SZARPNIĘCIE'])
 assert(S.matchesRecord(rows[0],q),q);
for(const q of ['Olga Kowalska','Kowalska Olga','kowalska, olga'])
 assert(S.matchesRecord(rows[1],q),q);
assert(!S.matchesRecord(rows[0],'Nieistniejący Autor'));
assert(S.matchesSource({name:'Biuro Literackie',file:'biuro.bib',url:'https://example.org',method:'manualna'},'Roman Honet','Honet, Roman'));
console.log('test wyszukiwania OK');
