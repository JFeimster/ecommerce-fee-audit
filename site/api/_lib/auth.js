const crypto = require('node:crypto');
function header(req, name) { const headers = (req && req.headers) || {}; return headers[name] || headers[name.toLowerCase()] || headers[name.toUpperCase()]; }
function equal(left, right) { if (typeof left !== 'string' || typeof right !== 'string') return false; const a = Buffer.from(left); const b = Buffer.from(right); return a.length === b.length && crypto.timingSafeEqual(a, b); }
function authorize(req, authClass) {
  if (authClass === 'no_auth') return { ok: true, subject: 'public' };
  if (authClass === 'api_key') { const configured = process.env.EFA_API_KEY || process.env.EFA_MOCK_API_KEY; const supplied = header(req, 'x-api-key'); return configured && supplied && equal(supplied, configured) ? { ok: true, subject: 'api_key' } : { ok: false, status: configured ? 401 : 503, code: configured ? 'api_key_invalid' : 'server_auth_not_configured' }; }
  if (authClass === 'oauth') { const provider = header(req, 'x-oauth-provider'); const subject = header(req, 'x-oauth-subject'); return provider && subject ? { ok: true, subject, provider } : { ok: false, status: 401, code: 'oauth_context_required' }; }
  if (authClass === 'internal_only') { const configured = process.env.EFA_INTERNAL_KEY; const supplied = header(req, 'x-internal-authorization'); return configured && supplied && equal(supplied, configured) ? { ok: true, subject: 'internal' } : { ok: false, status: configured ? 403 : 503, code: configured ? 'internal_authorization_invalid' : 'internal_authorization_not_configured' }; }
  return { ok: false, status: 403, code: 'auth_class_not_supported' };
}
module.exports = { authorize, equal, header };
