import { MCPAdapter } from '@langchain/mcp-adapters';
import { ChatOpenAI } from '@langchain/openai';
import { MessagesAnnotation, START, StateGraph } from '@langchain/langgraph';
import { ToolNode, toolsCondition } from '@langchain/langgraph/prebuilt';

export function validateLiveConnection(url: string, token: string): void {
  const endpoint = new URL(url);
  if (endpoint.username || endpoint.password || endpoint.search || endpoint.hash) throw new Error('Use an MCP URL without embedded credentials, query parameters, or fragments.');
  if (endpoint.protocol !== 'https:') throw new Error('Live MCP endpoints must use HTTPS.');
  if (!token || /\s/.test(token)) throw new Error('Use a non-empty MCP access token without whitespace.');
  if (token.startsWith('wvz_')) throw new Error('WEAVZ_MCP_TOKEN must be an MCP access token, not a Weavz REST API key.');
  if (endpoint.pathname.replace(/\/$/, '') === '/mcp/weavz') {
    throw new Error('The hosted /mcp/weavz resource uses OAuth. Use the custom MCP endpoint and access token returned by setup.');
  }
}

export function createMcpAdapter(url: string, token: string) {
  return new MCPAdapter({ servers: { weavz: { url, headers: { Authorization: `Bearer ${token}` } } } });
}

export async function runFixtureSmoke(url: string, token: string, mode: 'tools' | 'code') {
  const adapter = createMcpAdapter(url, token);
  try {
    const tools = await adapter.listTools();
    const names = tools.map(tool => tool.name).sort();
    const invoke = async (suffix: string, input: Record<string, unknown>) => {
      const tool = tools.find(candidate => candidate.name.endsWith(suffix));
      if (!tool) throw new Error(`Expected executable MCP tool ending in ${suffix}; discovered ${names.join(', ')}`);
      return tool.invoke(input);
    };
    let result: unknown;
    const calls: unknown[] = [];
    if (mode === 'tools') {
      result = await invoke('demo__lookup_record', { recordId: 'record-1' });
      calls.push(result);
    } else {
      result = await invoke('weavz_search', { query: 'record-1' });
      calls.push(result);
      calls.push(await invoke('weavz_read_api', { alias: 'demo', action: 'lookup_record' }));
      calls.push(await invoke('weavz_execute', {
        code: 'return await weavz.demo.lookup_record({recordId: "record-1"});',
      }));
    }
    return { names, result, calls };
  } finally { await adapter.close(); }
}

export async function discoverTools(url: string, token: string) {
  const adapter = createMcpAdapter(url, token);
  try { return (await adapter.listTools()).map(tool => tool.name).sort(); } finally { await adapter.close(); }
}

export async function runAgent(url: string, token: string, prompt: string) {
  const modelId = process.env.OPENAI_MODEL;
  if (!process.env.OPENAI_API_KEY || !modelId) throw new Error('Set OPENAI_API_KEY and OPENAI_MODEL to run the live agent.');
  const adapter = createMcpAdapter(url, token);
  try {
    const tools = await adapter.listTools();
    const model = new ChatOpenAI({ model: modelId }).bindTools(tools);
    const graph = new StateGraph(MessagesAnnotation)
      .addNode('agent', async (state) => ({ messages: [await model.invoke(state.messages)] }))
      .addNode('tools', new ToolNode(tools))
      .addEdge(START, 'agent')
      .addConditionalEdges('agent', toolsCondition)
      .addEdge('tools', 'agent')
      .compile();
    const result = await graph.invoke({ messages: [{ role: 'user', content: prompt }] });
    return result.messages.at(-1)?.content;
  } finally { await adapter.close(); }
}

async function main() {
  const args = process.argv.slice(2);
  if (args.includes('--fixture')) {
    if (args.includes('--prompt')) throw new Error('--fixture runs deterministic adapter checks; it cannot run a model prompt.');
    const mode = args[args.indexOf('--mode') + 1];
    if (mode !== 'tools' && mode !== 'code') throw new Error('Choose --mode tools or --mode code.');
    const { startFixture, FIXTURE_TOKEN } = await import('../test/fixture.js');
    const fixture = await startFixture(mode);
    try { console.log(JSON.stringify(await runFixtureSmoke(fixture.url, FIXTURE_TOKEN, mode), null, 2)); }
    finally { await fixture.close(); }
    return;
  }
  const url = process.env.WEAVZ_MCP_URL;
  const token = process.env.WEAVZ_MCP_TOKEN;
  const promptIndex = args.indexOf('--prompt');
  const prompt = promptIndex >= 0 ? args[promptIndex + 1] : undefined;
  if (promptIndex >= 0 && !prompt?.trim()) throw new Error('Pass a non-empty prompt after --prompt.');
  if (!url || !token) throw new Error('Set WEAVZ_MCP_URL and WEAVZ_MCP_TOKEN.');
  validateLiveConnection(url, token);
  if (args.includes('--mode')) throw new Error('Tool Mode and Code Mode are server settings; use --mode only with --fixture.');
  if (!prompt) {
    console.log(JSON.stringify({ tools: await discoverTools(url, token) }, null, 2));
    return;
  }
  console.log(await runAgent(url, token, prompt));
}
if (import.meta.url === `file://${process.argv[1]}`) main().catch(error => { console.error(error instanceof Error ? error.message : error); process.exitCode = 1; });
