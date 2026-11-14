"""Check standalone packaging, catalog identity and synthetic workflow metrics."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
catalog = json.loads((ROOT / 'catalog.json').read_text())
entries = catalog['examples']
assert len(entries) >= 50
assert len({e['id'] for e in entries}) == len(entries)
assert len({e['repository'] for e in entries}) == len(entries)
for entry in entries:
    directory = ROOT / entry['path']
    for name in ['README.md', 'AGENTS.md', 'LICENSE', '.gitignore']:
        assert (directory / name).is_file(), f'{entry["id"]}: missing {name}'
    assert list((directory / '.github/workflows').glob('*.yml'))
    assert set(entry['modes']) == {'tools', 'code'}
    if entry['category'] != 'workflow': continue
    scenario = json.loads((directory / 'scenario.json').read_text())
    assert scenario == json.loads((ROOT / 'workflows' / f'{entry["id"]}.json').read_text())
    assert scenario['id'] == entry['id']
    assert 1 <= len(scenario['steps']) <= 4
    records = {record['id']: record for step in scenario['steps'] for record in step['records']}
    assert 2 <= len(records) <= 6
    actual = {}
    for metric in scenario['metrics']:
        selected = [record for record in records.values() if all(record.get(k) == v for k, v in metric.get('where', {}).items())]
        assert metric['op'] in {'count', 'sum'}
        actual[metric['name']] = len(selected) if metric['op'] == 'count' else sum(record.get(metric['field'], 0) for record in selected)
    assert actual == scenario['expected_metrics'], entry['id']
    for name in ['engine.py', 'main.py', 'contract.py']:
        assert (directory / name).read_bytes() == (ROOT / 'shared/workflow-python' / name).read_bytes(), f'{entry["id"]}: stale {name}'
    assert (directory / 'tests/test_workflow.py').read_bytes() == (ROOT / 'shared/workflow-python/test_workflow.py').read_bytes()
print(f'{len(entries)} standalone example contracts passed')
