/* iPBL search normalization independent of minified React bundle. */
(function (global) {
  'use strict';
  function norm(value) {
    return String(value == null ? '' : value)
      .replace(/[łŁ]/g, c => c === 'ł' ? 'l' : 'L')
      .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
      .toLocaleLowerCase('pl')
      .replace(/[,;]+/g, ' ').replace(/\s+/g, ' ').trim();
  }
  function aliases(value) {
    const text=norm(value);
    if (!text) return [];
    const out=[text];
    const raw=String(value || '').trim();
    const match=raw.match(/^([^,]+),\s*(.+)$/);
    if (match) {
      out.push(norm(match[2]+' '+match[1]));
    } else {
      const words=text.split(/\s+/);
      if (words.length>=2 && words.length<=4)
        out.push([words[words.length-1],...words.slice(0,-1)].join(' '));
    }
    return out;
  }
  function indexRecords(records) {
    for(const record of records) {
      const parts=Object.entries(record)
        .filter(([key,val])=>key!=='_searchText' && typeof val==='string')
        .map(([,val])=>val);
      for(const person of (record.authorTerms || []))
        parts.push(...aliases(person.label || ''));
      record._searchText=norm(parts.join(' '));
    }
    return records;
  }
  function matchesRecord(record,query) {
    const wanted=norm(query);
    if(!wanted) return true;
    return (record._searchText ||
      norm(Object.values(record).filter(x=>typeof x==='string').join(' '))).includes(wanted);
  }
  function matchesSource(source,query,rawIndex='') {
    const wanted=norm(query);
    if(!wanted) return true;
    const text=norm([source.name,source.file,source.url,source.method,rawIndex].join(' '));
    if(text.includes(wanted))return true;
    const words=wanted.split(' ');
    if(words.length===2)return text.includes(words[1]+' '+words[0]);
    return false;
  }
  global.IPBLSearchUtils={norm,aliases,indexRecords,matchesRecord,matchesSource};
})(window);
