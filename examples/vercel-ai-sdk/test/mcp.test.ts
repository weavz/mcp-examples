import assert from 'node:assert/strict';
import { test } from 'node:test';
import { DEMO_RECORD, FIXTURE_TOKEN, KNOWN_CODE, startFixture } from './fixture.js';
import { runFixtureSmoke, validateLiveConnection } from '../src/index.js';

test('native MCP adapter discovers and invokes Tool Mode tools without a model', async () => {
  const fixture = await startFixture('tools');
  try {
    const result = await runFixtureSmoke(fixture.url, FIXTURE_TOKEN, 'tools');
    assert.ok(JSON.stringify(result.result).includes(DEMO_RECORD.title));
    assert.ok(JSON.stringify(result.result).includes(DEMO_RECORD.recordId));
    assert.equal(result.calls.length, 1);
    assert.ok(fixture.authenticatedMethods.length >= 2);
    assert.ok(fixture.methods.includes('tools/list'));
    assert.ok(fixture.methods.includes('tools/call'));
  } finally { await fixture.close(); }
});

test('native MCP adapter discovers and invokes Code Mode tools without a model', async () => {
  const fixture = await startFixture('code');
  try {
    const result = await runFixtureSmoke(fixture.url, FIXTURE_TOKEN, 'code');
    assert.ok(JSON.stringify(result.result).includes(DEMO_RECORD.title));
    assert.ok(JSON.stringify(result.result).includes(DEMO_RECORD.recordId));
    assert.equal(KNOWN_CODE, 'return await weavz.demo.lookup_record({recordId: "record-1"});');
    assert.equal(result.calls.length, 3);
    assert.ok(result.calls.every(call => JSON.stringify(call).includes('Fixture record')));
    assert.ok(fixture.authenticatedMethods.length >= 4);
    assert.ok(fixture.methods.filter(method => method === 'tools/call').length >= 3);
  } finally { await fixture.close(); }
});

test('fixture rejects an invalid bearer token before processing MCP requests', async () => {
  const fixture = await startFixture('tools');
  try {
    const response = await fetch(fixture.url, {
      method: 'POST',
      headers: { Authorization: 'Bearer wrong-token', 'Content-Type': 'application/json' },
      body: JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'initialize', params: {} }),
    });
    assert.equal(response.status, 401);
    assert.deepEqual(fixture.methods, []);
  } finally { await fixture.close(); }
});

test('live connection validation rejects unsafe or incompatible bearer setup', () => {
  assert.throws(() => validateLiveConnection('http://remote.example/mcp', 'mcp_example-token'), /HTTPS/);
  assert.throws(() => validateLiveConnection('https://remote.example/mcp', 'wvz_example-rest-key'), /MCP access token/);
  assert.throws(() => validateLiveConnection('https://platform.weavz.io/mcp/weavz', 'mcp_example-token'), /uses OAuth/);
  assert.doesNotThrow(() => validateLiveConnection('https://tenant.example/mcp', 'mcp_example-token'));
});
