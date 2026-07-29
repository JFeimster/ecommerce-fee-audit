const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { execFileSync } = require('node:child_process');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const openapiRoot = path.join(repositoryRoot, 'api', 'openapi');
const schemaRoot = path.join(repositoryRoot, 'api', 'schemas');
const approvedContractRoots = [openapiRoot, schemaRoot];
const approvedSchemaNamespace = 'https://ecommerce-fee-audit.example/api/schemas/';
const httpMethods = new Set(['get', 'post', 'put', 'patch', 'delete', 'options', 'head', 'trace']);
const approvedSharedRoutes = new Map([
  ['/api/public', 1],
  ['/api/intake', 2],
  ['/api/uploads', 3],
  ['/api/audits', 4],
  ['/api/exports', 5],
  ['/api/connectors', 6],
  ['/api/oauth-callback', 7],
  ['/api/webhooks/{provider}', 8],
  ['/api/jobs', 9],
  ['/api/health', 10]
]);
const documentCache = new Map();

function relativePath(absolutePath) {
  return path.relative(repositoryRoot, absolutePath).split(path.sep).join('/');
}

function listContractFiles(directory) {
  return fs.readdirSync(directory, { withFileTypes: true })
    .sort((left, right) => left.name.localeCompare(right.name))
    .flatMap((entry) => {
      const fullPath = path.join(directory, entry.name);
      if (entry.isDirectory()) return listContractFiles(fullPath);
      return entry.isFile() && /\.ya?ml$|\.json$/i.test(entry.name) ? [fullPath] : [];
    });
}

function loadYamlOrJson(filePath) {
  if (documentCache.has(filePath)) return documentCache.get(filePath);
  const parser = [
    'import json, pathlib, sys, yaml',
    'source = pathlib.Path(sys.argv[1])',
    'with source.open(encoding="utf-8") as handle:',
    '    value = json.load(handle) if source.suffix.lower() == ".json" else yaml.safe_load(handle)',
    'print(json.dumps(value))'
  ].join('\n');
  try {
    const document = JSON.parse(execFileSync('python', ['-c', parser, filePath], { encoding: 'utf8' }));
    documentCache.set(filePath, document);
    return document;
  } catch (error) {
    const detail = error.stderr ? error.stderr.toString().trim() : error.message;
    assert.fail(`Unable to parse ${relativePath(filePath)} as YAML or JSON: ${detail}`);
  }
}

function isWithinApprovedRoot(filePath) {
  return approvedContractRoots.some((root) => {
    const relative = path.relative(root, filePath);
    return relative === '' || (!relative.startsWith(`..${path.sep}`) && relative !== '..' && !path.isAbsolute(relative));
  });
}

function decodePointerToken(token, context) {
  assert.doesNotMatch(token, /~(?:[^01]|$)/, `Malformed JSON Pointer escape in ${context}: ${token}`);
  return token.replace(/~1/g, '/').replace(/~0/g, '~');
}

function resolveJsonPointer(document, fragment, context) {
  if (!fragment || fragment === '#') return document;
  const decoded = decodeURIComponent(fragment);
  assert.ok(decoded.startsWith('#/'), `Malformed JSON Pointer fragment in ${context}: ${fragment}`);
  return decoded.slice(2).split('/').reduce((value, token) => {
    const key = decodePointerToken(token, context);
    assert.ok(value !== null && typeof value === 'object' && Object.prototype.hasOwnProperty.call(value, key), `Unresolved JSON Pointer fragment in ${context}: ${fragment}`);
    return value[key];
  }, document);
}

function resolveReference(sourceFile, reference) {
  const hashIndex = reference.indexOf('#');
  const referencePath = hashIndex === -1 ? reference : reference.slice(0, hashIndex);
  const fragment = hashIndex === -1 ? '' : reference.slice(hashIndex);

  if (/^https:\/\//i.test(referencePath)) {
    assert.ok(referencePath.startsWith(approvedSchemaNamespace), `External reference is outside the approved schema namespace in ${relativePath(sourceFile)}: ${reference}`);
    return { external: true, reference, fragment };
  }
  assert.ok(!/^[a-z][a-z0-9+.-]*:/i.test(referencePath), `Unsupported URI scheme in ${relativePath(sourceFile)}: ${reference}`);
  const decodedPath = decodeURIComponent(referencePath);
  assert.ok(!path.isAbsolute(decodedPath) && !/^[a-z]:[\\/]/i.test(decodedPath), `Absolute filesystem reference is prohibited in ${relativePath(sourceFile)}: ${reference}`);

  const targetFile = decodedPath ? path.resolve(path.dirname(sourceFile), decodedPath) : sourceFile;
  assert.ok(isWithinApprovedRoot(targetFile), `Reference escapes approved contract roots in ${relativePath(sourceFile)}: ${reference}`);
  assert.ok(fs.existsSync(targetFile), `Missing local reference from ${relativePath(sourceFile)}: ${reference}`);
  const targetDocument = loadYamlOrJson(targetFile);
  resolveJsonPointer(targetDocument, fragment, `${relativePath(sourceFile)} -> ${reference}`);
  return { external: false, targetFile, targetDocument, fragment };
}

function collectReferences(value, references = []) {
  if (Array.isArray(value)) {
    value.forEach((item) => collectReferences(item, references));
  } else if (value && typeof value === 'object') {
    for (const [key, item] of Object.entries(value)) {
      if (key === '$ref' && typeof item === 'string') references.push(item);
      collectReferences(item, references);
    }
  }
  return references;
}

function collectOperations(document, sourceFile) {
  const operations = [];
  for (const [route, pathItem] of Object.entries(document.paths || {})) {
    if (!pathItem || typeof pathItem !== 'object') continue;
    for (const [method, operation] of Object.entries(pathItem)) {
      if (!httpMethods.has(method.toLowerCase())) continue;
      operations.push({ sourceFile, route, method: method.toUpperCase(), operation });
    }
  }
  return operations;
}

function loadActionRouting() {
  return loadYamlOrJson(path.join(repositoryRoot, 'config', 'actions', 'action-routing.yaml')).operations;
}

function approvedRouteFamily(route) {
  return [...approvedSharedRoutes.keys()].find((sharedRoute) => route === sharedRoute || route.startsWith(`${sharedRoute}/`));
}

const openapiFiles = listContractFiles(openapiRoot);
const documents = openapiFiles.map((sourceFile) => ({ sourceFile, document: loadYamlOrJson(sourceFile) }));
const operations = documents.flatMap(({ sourceFile, document }) => collectOperations(document, sourceFile));
const routing = loadActionRouting();

test('OpenAPI documents parse and declare OpenAPI 3.1', () => {
  assert.ok(documents.length > 0, 'Expected at least one OpenAPI YAML or JSON document under api/openapi/');
  for (const { sourceFile, document } of documents) {
    assert.ok(document && typeof document === 'object', `${relativePath(sourceFile)} must parse to an OpenAPI object`);
    assert.match(String(document.openapi || ''), /^3\.1(?:\.|$)/, `${relativePath(sourceFile)} must declare an OpenAPI 3.1.x version; found ${document.openapi}`);
  }
});

test('OpenAPI operations have non-empty globally unique operation IDs', () => {
  const seen = new Map();
  for (const { sourceFile, route, method, operation } of operations) {
    assert.ok(operation && typeof operation === 'object', `${relativePath(sourceFile)} ${method} ${route} must define an operation object`);
    const operationId = operation.operationId;
    assert.equal(typeof operationId, 'string', `${relativePath(sourceFile)} ${method} ${route} must define a string operationId`);
    assert.ok(operationId.trim(), `${relativePath(sourceFile)} ${method} ${route} must define a non-empty operationId`);
    assert.ok(!seen.has(operationId), `Duplicate operationId ${operationId} in ${relativePath(sourceFile)} ${method} ${route}; first seen at ${seen.get(operationId)}`);
    seen.set(operationId, `${relativePath(sourceFile)} ${method} ${route}`);
  }
  assert.ok(seen.size > 0, 'Expected at least one direct HTTP operation across api/openapi/ documents');
});

test('local references resolve safely inside approved OpenAPI and schema roots', () => {
  let resolvedLocalReferences = 0;
  for (const { sourceFile, document } of documents) {
    for (const reference of collectReferences(document)) {
      const resolved = resolveReference(sourceFile, reference);
      if (!resolved.external) resolvedLocalReferences += 1;
    }
  }
  assert.ok(resolvedLocalReferences > 0, 'Expected OpenAPI contracts to contain at least one local reference to validate');
});

test('request and response schema references stay within the approved Batch 2 schema contract', () => {
  for (const { sourceFile, route, method, operation } of operations) {
    const areas = [operation.requestBody, operation.responses].filter(Boolean);
    for (const area of areas) {
      for (const reference of collectReferences(area)) {
        const resolved = resolveReference(sourceFile, reference);
        if (reference.startsWith('#/components/')) {
          // Small response envelopes are intentionally defined in the OpenAPI document.
          continue;
        }
        if (resolved.external) {
          assert.ok(reference.startsWith(approvedSchemaNamespace), `${relativePath(sourceFile)} ${method} ${route} uses a request/response schema outside the Batch 2 namespace: ${reference}`);
          continue;
        }
        assert.ok(resolved.targetFile.startsWith(schemaRoot), `${relativePath(sourceFile)} ${method} ${route} uses a request/response reference outside api/schemas/: ${reference}`);
        const schemaId = resolved.targetDocument.$id;
        assert.ok(typeof schemaId === 'string' && schemaId.startsWith(approvedSchemaNamespace), `${relativePath(resolved.targetFile)} must use the approved Batch 2 schema namespace; found ${schemaId}`);
      }
    }
  }
});

test('logical OpenAPI paths and canonical routing remain within the ten shared function routes', () => {
  for (const { sourceFile, route, method, operation } of operations) {
    const operationId = operation.operationId;
    const sharedPathFamily = approvedRouteFamily(route);
    assert.ok(sharedPathFamily, `${relativePath(sourceFile)} ${method} ${route} (${operationId}) is outside the approved shared API route families`);
    assert.ok(!/^\/api\/(?:webhooks|connectors)\/(?:shopify|stripe)(?:\/|$)/.test(route), `${relativePath(sourceFile)} ${method} ${route} (${operationId}) introduces provider-specific route proliferation`);
    assert.ok(!['/api/create-audit', '/api/run-audit', '/api/submit-funding-application', '/api/create-dispute-case'].some((prefix) => route === prefix || route.startsWith(`${prefix}/`)), `${relativePath(sourceFile)} ${method} ${route} (${operationId}) introduces operation-specific route proliferation`);

    const policy = routing[operationId];
    assert.ok(policy, `${relativePath(sourceFile)} ${method} ${route} (${operationId}) is missing from config/actions/action-routing.yaml`);
    assert.ok(approvedSharedRoutes.has(policy.route), `${operationId} maps to unapproved shared route ${policy.route} in action-routing.yaml`);
    assert.ok(Number(policy.function_slot) >= 1 && Number(policy.function_slot) <= 10, `${operationId} maps to prohibited function slot ${policy.function_slot}`);
    assert.equal(approvedSharedRoutes.get(policy.route), Number(policy.function_slot), `${operationId} maps ${policy.route} to slot ${policy.function_slot}; expected slot ${approvedSharedRoutes.get(policy.route)}`);
  }
});

test('funding and dispute submission terms remain distinct from outcomes', () => {
  const requireOperation = (operationId) => {
    assert.ok(routing[operationId], `Expected canonical action routing to define ${operationId}`);
    return routing[operationId];
  };

  const fundingCreation = requireOperation('createFundingApplication');
  const fundingSubmission = requireOperation('submitFundingApplication');
  assert.notEqual(fundingCreation.discriminator, fundingSubmission.discriminator, 'Funding application creation and submission must use distinct action discriminators');
  assert.equal(fundingSubmission.discriminator, 'submit_funding', 'Funding submission must retain the submit_funding discriminator');
  assert.doesNotMatch('submitFundingApplication', /approve|funded|provider.?decision/i, 'Funding submission operation must not be represented as approval, funding, or provider decision');

  const disputeCase = requireOperation('createDisputeCase');
  const disputePackage = requireOperation('assembleDisputePackage');
  const disputeSubmission = requireOperation('submitDisputePackage');
  const disputeEscalation = requireOperation('escalateDisputeCase');
  assert.equal(new Set([disputeCase.discriminator, disputePackage.discriminator, disputeSubmission.discriminator, disputeEscalation.discriminator]).size, 4, 'Dispute case creation, package assembly, submission, and escalation must use distinct action discriminators');
  assert.equal(disputeSubmission.discriminator, 'submit_dispute', 'Dispute submission must retain the submit_dispute discriminator');
  assert.doesNotMatch('submitDisputePackage', /recover|recovery/i, 'Dispute submission operation must not be represented as recovery');
});
