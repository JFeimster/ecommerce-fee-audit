const sensitive = /(authorization|api[_-]?key|token|password|secret|ssn|tax[_-]?id|account[_-]?number|routing[_-]?number|card[_-]?number)/i;
function redact(value) {
  if (Array.isArray(value)) return value.map(redact);
  if (!value || typeof value !== 'object') return value;
  return Object.fromEntries(Object.entries(value).map(([key, item]) => [key, sensitive.test(key) ? '[REDACTED]' : redact(item)]));
}
module.exports = { redact, isSensitiveKey: (key) => sensitive.test(key) };
