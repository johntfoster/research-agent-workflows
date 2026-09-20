from datetime import datetime,timezone
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tarfile
import tempfile
import unittest
CORE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(CORE/'tools'))
import research_project as rp
import review_scan
import session_ledger
import bootstrap_project

class ResearchTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)/'paper';self.root.mkdir()
  self.git('init','-q');self.git('config','user.name','Fixture');self.git('config','user.email','fixture@example.invalid')
  for f in ['AGENTS.md','agent-profile.json','main.tex']:(self.root/f).write_text('{}\n')
  dep=self.root/'.agent/shared';dep.parent.mkdir(parents=True)
  subprocess.run(['git','clone','-q',str(CORE),str(dep)],check=True)
  self.pin=rp.git(dep,'rev-parse','HEAD').stdout.strip()
  self.git('update-index','--add','--cacheinfo',f'160000,{self.pin},.agent/shared')
  self.manifest={'schema_version':1,'id':'fixture','repository':'https://github.com/example/fixture','default_branch':'main','status':'active','authority':{'instructions':'AGENTS.md','profile':'agent-profile.json','manuscript':'main.tex'},'workflow':{'repository':'https://github.com/example/core','path':'.agent/shared','revision':self.pin,'release':'fixture'},'maintenance':{'manuscript_edits':False,'protected_paths':list(rp.DEFAULT_PROTECTED)},'publication':{'codespace':{'url':'https://codespaces.new/example/fixture'},'citation':None},'verification':{k:'not-run' for k in rp.CATEGORIES},'next_milestone':'Run fixture tests.'}
  self.save();self.git('add','AGENTS.md','agent-profile.json','main.tex','research-project.yml');self.git('commit','-qm','fixture')
 def save(self):(self.root/'research-project.yml').write_text(json.dumps(self.manifest))
 def git(self,*args):return rp.git(self.root,*args)
 def tearDown(self):self.tmp.cleanup()
 def test_manifest_and_drift(self):
  self.assertEqual(rp.validate(self.manifest,self.root),[])
  self.manifest['workflow']['revision']='0'*40
  self.assertGreaterEqual(len(rp.validate(self.manifest,self.root)),2)
 def test_schema_agrees_with_valid_fixture(self):
  import jsonschema
  jsonschema.Draft202012Validator(json.loads((CORE/'config/research-project.schema.json').read_text())).validate(self.manifest)
 def test_paths_cannot_escape(self):
  self.manifest['authority']['manuscript']='../outside.tex';self.assertTrue(rp.validate(self.manifest,self.root))
  with self.assertRaises(ValueError):rp.runtime_output(self.root,'main.tex')
 def test_default_freeze_rejects_rename_and_case(self):
  self.git('mv','main.tex','innocent.md');self.assertIn('main.tex',rp.freeze(self.root))
  f=self.root/'other.TEX';f.write_text('test');self.git('add','other.TEX');self.assertIn('other.TEX',rp.freeze(self.root))
 def test_weak_manifest_cannot_remove_hard_protection(self):
  self.manifest['maintenance']['protected_paths']=[];self.save()
  (self.root/'main.tex').write_text('changed');self.git('add','main.tex');self.assertIn('main.tex',rp.freeze(self.root))
 def test_site_and_link_errors(self):
  before=(self.root/'main.tex').read_bytes();dest=rp.site(self.root,'.agent-runtime/site')
  self.assertEqual(rp.check_links(dest),[]);self.assertEqual((self.root/'main.tex').read_bytes(),before)
  with (dest/'index.html').open('a') as f:f.write('<a href="missing.html">missing</a>')
  self.assertTrue(rp.check_links(dest))
 def test_package_pins_core_and_excludes_dirty(self):
  (self.root/'main.tex').write_text('uncommitted source')
  dest=rp.package(self.root,'.agent-runtime/package')
  with tarfile.open(dest/'source.tar') as t:
   self.assertEqual(t.extractfile('main.tex').read(),b'{}\n')
   self.assertIn('.agent/shared/VERSION',t.getnames())
  self.assertFalse(json.loads((dest/'provenance.json').read_text())['scientific_release'])
  subprocess.run(['sha256sum','-c','SHA256SUMS'],cwd=dest,check=True,capture_output=True)
  self.git('bundle','verify',str(dest/'repository.bundle'))
 def test_bootstrap_refuses_existing_and_writes_no_manuscript(self):
  dest=Path(self.tmp.name)/'new'
  bootstrap_project.create(dest,'new','https://github.com/example/new',self.pin,'New')
  self.assertFalse(list(dest.rglob('*.tex')))
  self.assertEqual(rp.git(dest,'ls-files','--stage','.agent/shared').stdout.split()[1],self.pin)
  with self.assertRaises(ValueError):bootstrap_project.create(dest,'new','https://github.com/example/new',self.pin,'New')

class ForwardTests(unittest.TestCase):
 def test_held_out_prose_preserves_mathematical_negation(self):
  good='The fluid is incompressible. Its density does not change along this path. The balance gives the pressure response.'
  self.assertEqual(review_scan.scan(good)['findings'],[])
  bad='Unlike prior models, this revision addresses an unprecedented result.'
  self.assertEqual({x['rule'] for x in review_scan.scan(bad)['findings']},{'negative-positioning','drafting-history','unsupported-rhetoric'})
  self.assertFalse(review_scan.scan(bad)['edits_applied'])
 def test_synthetic_ledger_dedup_and_coverage(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);repo=root/'paper';repo.mkdir();store=root/'sessions';store.mkdir()
   text=json.dumps({'cwd':str(repo),'timestamp':'2026-09-19T00:00:00Z','message':{'role':'user','content':'a private fixture message'}})+'\n'
   (store/'a.jsonl').write_text(text);(store/'mirror.jsonl').write_text(text)
   (store/'unrelated.jsonl').write_text(text.replace(str(repo),str(root/'elsewhere')))
   report=session_ledger.collect(repo,[('fixture',store),('missing',root/'absent')],datetime(2026,9,18,tzinfo=timezone.utc),datetime(2026,9,20,tzinfo=timezone.utc))
   self.assertEqual(len(report['sessions']),1);self.assertEqual(len(report['sessions'][0]['mirrors']),1)
   self.assertTrue(report['limitations']);self.assertNotIn('private fixture message',json.dumps(report))
 def test_synthetic_process_log_checks(self):
  spec=importlib.util.spec_from_file_location('validator',CORE/'tools/validate_process_log.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
  good='Fixture\n\n'+'\n\n'.join(s+'\n\n'+('AI model(s): fixture\nAI session(s): synthetic-1\n' if s=='Summary' else '')+'Evidence from a synthetic window.' for s in m.SECTIONS)
  self.assertEqual(m.validate(good),[]);self.assertTrue(m.validate(good.replace('AI session(s): synthetic-1','AI session(s): unknown')))

if __name__=='__main__':unittest.main()
