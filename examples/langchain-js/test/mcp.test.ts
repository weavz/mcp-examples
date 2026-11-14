import assert from 'node:assert/strict';
import { test } from 'node:test';
import { DEMO_RECORD, FIXTURE_TOKEN, startFixture } from './fixture.js';
import { createMcpAdapter, runFixtureSmoke, validateLiveConnection } from '../src/index.js';

function containsFixtureRecord(value: unknown): boolean {
  return JSON.stringify(value).includes(DEMO_RECORD.title) && JSON.stringify(value).includes(DEMO_RECORD.recordId);
}

test('LangChain MCPAdapter discovers and invokes Tool Mode without a model', async () => {
  const fixture = await startFixture('tools');
  try {
    const result = await runFixtureSmoke(fixture.url, FIXTURE_TOKEN, 'tools');
    assert.ok(result.names.some(name => name.endsWith('demo__lookup_record')));
    assert.ok(containsFixtureRecord(result.result));
    assert.equal(result.calls.length, 1);
    assert.ok(fixture.authenticatedMethods.length >= 2);
    assert.ok(fixture.methods.includes('tools/list'));
    assert.ok(fixture.methods.includes('tools/call'));
  } finally { await fixture.close(); }
});

test('LangChain MCPAdapter discovers and invokes Code Mode without a model', async () => {
  const fixture = await startFixture('code');
  try {
    const result = await runFixtureSmoke(fixture.url, FIXTURE_TOKEN, 'code');
    assert.ok(result.names.some(name => name.endsWith('weavz_search')));
    assert.ok(containsFixtureRecord(result.result));
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
