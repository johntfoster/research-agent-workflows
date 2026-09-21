from pathlib import Path
import json
import re
import unittest
import yaml
CORE=Path(__file__).resolve().parents[1]
class CatalogTests(unittest.TestCase):
 def test_all_35_skills_have_discoverable_frontmatter(self):
  files=list((CORE/'skills').glob('*/SKILL.md'));self.assertEqual(len(files),35)
  for p in files:
   fm=yaml.safe_load(p.read_text().split('---',2)[1]);self.assertEqual(fm['name'],p.parent.name);self.assertTrue(fm['description'])
 def test_declared_routes_resolve(self):
  m=json.loads((CORE/'agent-profile.json').read_text())
  for r in m['routes']:
   for n in r['skills']:self.assertTrue((CORE/'skills'/n/'SKILL.md').is_file())
 def test_ci_actions_use_immutable_commits(self):
  for p in (CORE/'.github/workflows').glob('*.yml'):
   yaml.load(p.read_text(),Loader=yaml.BaseLoader)
   for action in re.findall(r'uses:\s+(\S+)',p.read_text()):
    self.assertRegex(action,r'@[a-f0-9]{40}$')
 def test_manuscript_job_is_explicit_and_frozen_by_default(self):
  p=yaml.load((CORE/'.github/workflows/research-manuscript.yml').read_text(),Loader=yaml.BaseLoader)
  self.assertEqual(p['on']['workflow_call']['inputs']['authorized']['default'],'false')
  self.assertIn('maintenance',str(p['jobs']))
if __name__=='__main__':unittest.main()
