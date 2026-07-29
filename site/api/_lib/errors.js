const { redact } = require('./redaction');
function requestId(req) { return (req && req.headers && (req.headers['x-request-id'] || req.headers['X-Request-Id'])) || `req_${Date.now().toString(36)}`; }
function error(res, status, code, operationId, req, details) {
  const body = { error: { code, message: 'Request cannot be completed in this runtime mode.', request_id: requestId(req), operation_id: operationId || null, retryable: false, review_required: false, timestamp: new Date().toISOString() } };
  if (details) body.error.details = redact(details);
  return res.status(status).json(body);
}
module.exports = { error, requestId };
