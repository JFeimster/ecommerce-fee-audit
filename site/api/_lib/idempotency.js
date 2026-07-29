const crypto = require('node:crypto'); const records = new Map();
function fingerprint(value) { return crypto.createHash('sha256').update(JSON.stringify(value || {})).digest('hex'); }
function begin(key, operationId, subject, payload) { if (!key) return { ok:false, code:'idempotency_key_required' }; const id=`${operationId}:${subject || 'anonymous'}:${key}`; const hash=fingerprint(payload); const prior=records.get(id); if (!prior) { records.set(id,{hash,status:'pending'}); return {ok:true,id,local_test_only:true}; } if (prior.hash!==hash) return {ok:false,code:'idempotency_conflict'}; if (prior.status==='ambiguous') return {ok:false,code:'idempotency_ambiguous'}; return {ok:true,reused:true,response:prior.response,local_test_only:true}; }
function complete(id,response) { const prior=records.get(id); if (prior) { prior.status='completed'; prior.response=response; } }
function ambiguous(id) { const prior=records.get(id); if (prior) prior.status='ambiguous'; }
function reset() { records.clear(); }
module.exports={begin,complete,ambiguous,reset,status:'local_test_only'};
