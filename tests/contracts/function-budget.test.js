const test = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');

const repositoryRoot = path.resolve(__dirname, '..', '..');
const apiDirectory = path.join(repositoryRoot, 'site', 'api');
const expectedRouteFiles = [
  'site/api/public.js',
  'site/api/intake.js',
  'site/api/uploads.js',
  'site/api/audits.js',
  'site/api/exports.js',
  'site/api/connectors.js',
  'site/api/oauth-callback.js',
  'site/api/webhooks/[provider].js',
  'site/api/jobs.js',
  'site/api/health.js'
].sort();

const approvedRouteToFile = new Map([
  ['/api/public', 'site/api/public.js'],
  ['/api/intake', 'site/api/intake.js'],
  ['/api/uploads', 'site/api/uploads.js'],
  ['/api/audits', 'site/api/audits.js'],
  ['/api/exports', 'site/api/exports.js'],
  ['/api/connectors', 'site/api/connectors.js'],
  ['/api/oauth-callback', 'site/api/oauth-callback.js'],
  ['/api/webhooks/{provider}', 'site/api/webhooks/[provider].js'],
  ['/api/jobs', 'site/api/jobs.js'],
  ['/api/health', 'site/api/health.js']
]);

function normalizedRelativePath(absolutePath) {
  return path.relative(repositoryRoot, absolutePath).split(path.sep).join('/');
}

function listJavaScriptFiles(directory) {
  return fs.readdirSync(directory, { withFileTypes: true })
    .sort((left, right) => left.name.localeCompare(right.name))
    .flatMap((entry) => {
      const fullPath = path.join(directory, entry.name);
      if (entry.isDirectory()) return listJavaScriptFiles(fullPath);
      return entry.isFile() && entry.name.endsWith('.js') ? [fullPath] : [];
    });
}

function physicalRouteFiles() {
  return listJavaScriptFiles(apiDirectory)
    .map(normalizedRelativePath)
    .filter((relativePath) => !relativePath.startsWith('site/api/_lib/') && !relativePath.startsWith('site/api/_data/'))
    .sort();
}

function parseFunctionBudget() {
  const budgetPath = path.join(repositoryRoot, 'config', 'actions', 'function-budget.yaml');
  const lines = fs.readFileSync(budgetPath, 'utf8').replace(/\r\n/g, '\n').split('\n');
  const scalar = Object.create(null);
  const slots = [];

  for (const line of lines) {
    const scalarMatch = line.match(/^([a-z_]+):\s*(.+)$/);
    if (scalarMatch && !line.startsWith('  ')) {
      scalar[scalarMatch[1]] = scalarMatch[2].replace(/^['"]|['"]$/g, '');
      continue;
    }

    const slotMatch = line.match(/^\s*-\s*\{(.+)\}\s*$/);
    if (!slotMatch) continue;
    const slot = Object.create(null);
    const fields = [...slotMatch[1].matchAll(/(?:^|,\s*)([a-z_]+):\s*(.*?)(?=,\s*[a-z_]+:|$)/g)];
    assert.ok(fields.length > 0, `Invalid function-budget slot entry: ${line}`);
    for (const [, key, rawValue] of fields) {
      slot[key] = rawValue.trim().replace(/^['"]|['"]$/g, '');
    }
    slots.push(slot);
  }

  return { scalar, slots };
}

test('physical Vercel route inventory is exactly the approved ten shared routes', () => {
  const actual = physicalRouteFiles();
  assert.deepEqual(
    actual,
    expectedRouteFiles,
    `Physical route inventory differs from the approved shared routes. Missing: ${expectedRouteFiles.filter((file) => !actual.includes(file)).join(', ') || 'none'}. Unexpected: ${actual.filter((file) => !expectedRouteFiles.includes(file)).join(', ') || 'none'}.`
  );
  assert.equal(actual.length, 10, `Expected exactly 10 physical Vercel routes; found ${actual.length}: ${actual.join(', ')}`);
});

test('function budget maps all active slots to physical shared routes and reserves slots 11 and 12', () => {
  const { scalar, slots } = parseFunctionBudget();
  assert.equal(scalar.active_function_limit, '10', 'function-budget.yaml must declare active_function_limit: 10');
  assert.equal(scalar.reserved_function_slots, '2', 'function-budget.yaml must declare reserved_function_slots: 2');
  assert.equal(scalar.maximum_total_slots, '12', 'function-budget.yaml must declare maximum_total_slots: 12');

  const activeSlots = slots.filter((slot) => Number(slot.slot) <= 10);
  const reservedSlots = slots.filter((slot) => Number(slot.slot) > 10);
  assert.equal(activeSlots.length, 10, `Expected 10 configured active slots; found ${activeSlots.length}`);
  assert.deepEqual(reservedSlots.map((slot) => Number(slot.slot)).sort((a, b) => a - b), [11, 12], 'Only slots 11 and 12 may be reserved');

  for (const slot of activeSlots) {
    const routeFile = approvedRouteToFile.get(slot.route);
    assert.ok(routeFile, `Configured slot ${slot.slot} uses an unapproved route: ${slot.route}`);
    assert.ok(fs.existsSync(path.join(repositoryRoot, routeFile)), `Configured slot ${slot.slot} route ${slot.route} has no physical route file: ${routeFile}`);
  }
  for (const slot of reservedSlots) {
    assert.equal(slot.route, 'reserved', `Reserved slot ${slot.slot} must not declare a deployable route`);
    assert.equal(slot.activation_status, 'reserved', `Reserved slot ${slot.slot} must retain activation_status: reserved`);
  }
});

test('shared webhook route prevents provider and operation-specific route proliferation', () => {
  const routes = physicalRouteFiles();
  assert.ok(routes.includes('site/api/webhooks/[provider].js'), 'The shared webhook route site/api/webhooks/[provider].js must exist');
  assert.deepEqual(
    routes.filter((route) => route.startsWith('site/api/webhooks/')),
    ['site/api/webhooks/[provider].js'],
    `Webhook route proliferation detected: ${routes.filter((route) => route.startsWith('site/api/webhooks/')).join(', ')}`
  );

  const reservedRouteNames = ['create-audit', 'run-audit', 'submit-funding-application', 'shopify', 'stripe'];
  const prohibited = routes.filter((route) => reservedRouteNames.some((name) => route.endsWith(`/${name}.js`)));
  assert.deepEqual(prohibited, [], `Provider- or operation-specific route proliferation detected: ${prohibited.join(', ')}`);
  assert.deepEqual([...approvedRouteToFile.values()].sort(), expectedRouteFiles, 'Each approved shared route must have one physical route file');
});

test('Vercel deployment lock keeps preview deployments disabled without changing main production behavior', () => {
  const vercelPath = path.join(repositoryRoot, 'site', 'vercel.json');
  const vercel = JSON.parse(fs.readFileSync(vercelPath, 'utf8'));
  const deploymentEnabled = vercel.git && vercel.git.deploymentEnabled;
  assert.ok(deploymentEnabled && typeof deploymentEnabled === 'object', 'site/vercel.json must retain git.deploymentEnabled controls');
  assert.equal(deploymentEnabled['*'], false, 'Preview deployments must remain disabled through git.deploymentEnabled["*"]');
  assert.equal(deploymentEnabled.main, true, 'The main branch production deployment behavior must remain enabled');
  assert.deepEqual(Object.keys(deploymentEnabled).sort(), ['*', 'main'], 'Deployment lock must not add an unreviewed branch deployment override');
});
