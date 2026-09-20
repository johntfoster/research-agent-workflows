#!/usr/bin/env python3
"""Read-only project checks and explicitly requested infrastructure artifacts.

Manifests use the JSON subset of YAML so clean-clone audits need only Python.
No command edits manuscript sources or runs commands from a manifest.
"""
from __future__ import annotations
import argparse
import fnmatch
import hashlib
import html
from html.parser import HTMLParser
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import tarfile
from urllib.parse import urlparse, unquote

CORE = Path(__file__).resolve().parents[1]
CATEGORIES = ('infrastructure', 'implementation', 'analytical', 'convergence', 'finite_deformation', 'physical_validation')
DEFAULT_PROTECTED = ('*.tex','*.bib','*.sty','*.cls','*.bst','*.pdf','*.png','*.svg','*.eps','*.jpg','*.jpeg','paper/*','sections/*','figures/*','implementation_paper/*','submission/*','submissions/*')


def git(root, *args, check=True):
    return subprocess.run(['git', '--no-optional-locks', '-C', str(root), *args], text=True, capture_output=True, check=check)


def read(path):
    value = json.loads(Path(path).read_text())
    if not isinstance(value, dict):
        raise ValueError('manifest must be an object')
    return value


def relative(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute() or '..' in Path(value).parts:
        raise ValueError(f'not a repository-relative path: {value!r}')
    path = root / value
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'path escapes repository: {value}')
    return path


def validate(m, root=None):
    errors = []
    for key, typ in {'schema_version':int,'id':str,'repository':str,'default_branch':str,'status':str,'authority':dict,'workflow':dict,'maintenance':dict,'publication':dict,'verification':dict,'next_milestone':str}.items():
        if type(m.get(key)) is not typ:
            errors.append(f'{key}: expected {typ.__name__}')
    if errors:
        return errors
    if m['schema_version'] != 1:
        errors.append('unsupported schema_version')
    if not re.fullmatch(r'[a-z0-9][a-z0-9_-]*', m['id']):
        errors.append('invalid project id')
    if not m['repository'].startswith('https://github.com/'):
        errors.append('repository must be an authoritative HTTPS GitHub URL')
    if m['status'] not in {'active','incubating','submitted','superseded','shelved','archival'}:
        errors.append('invalid project status')
    if not re.fullmatch('[0-9a-f]{40}', str(m['workflow'].get('revision',''))):
        errors.append('workflow revision must be an exact 40-character commit')
    if type(m['maintenance'].get('manuscript_edits')) is not bool:
        errors.append('maintenance.manuscript_edits must be boolean')
    patterns = m['maintenance'].get('protected_paths')
    if not isinstance(patterns,list) or not patterns or not all(isinstance(x,str) for x in patterns):
        errors.append('maintenance.protected_paths must be nonempty strings')
    for category in CATEGORIES:
        if not isinstance(m['verification'].get(category),str):
            errors.append(f'missing separate verification category: {category}')
    for key in ('instructions','profile','manuscript'):
        try:
            path = relative(root or Path.cwd(), m['authority'].get(key))
            if root and not path.is_file():
                errors.append(f'authority path missing: {key}')
        except ValueError as e:
            errors.append(str(e))
    try:
        dependency = relative(root or Path.cwd(), m['workflow'].get('path'))
        if root:
            pin = git(dependency,'rev-parse','HEAD',check=False)
            if pin.returncode or pin.stdout.strip()!=m['workflow']['revision']:
                errors.append('checked-out shared workflow does not match manifest pin')
            tracked = git(root,'ls-files','--stage','--',m['workflow']['path']).stdout.split()
            if not tracked or tracked[0]!='160000' or tracked[1]!=m['workflow']['revision']:
                errors.append('Git index shared-workflow pin does not match manifest')
    except ValueError as e:
        errors.append(str(e))
    return errors


def audit(root):
    m=read(root/'research-project.yml')
    errors=validate(m,root)
    return {'project':m.get('id'),'errors':errors,'head':git(root,'rev-parse','HEAD').stdout.strip(),
            'dirty_paths':git(root,'status','--porcelain=v1','-uall').stdout.splitlines(),
            'workflow_revision':m.get('workflow',{}).get('revision'),
            'manuscript_edits':m.get('maintenance',{}).get('manuscript_edits'),
            'publication':m.get('publication'), 'verification':m.get('verification')}


def freeze(root):
    setting=git(root,'config','--bool','--get','research.manuscriptFreeze',check=False)
    if setting.returncode==0 and setting.stdout.strip()=='false':
        return []
    m=read(root/'research-project.yml')
    patterns=tuple(m.get('maintenance',{}).get('protected_paths',())) + DEFAULT_PROTECTED
    paths=git(root,'diff','--cached','--no-renames','--name-only','-z').stdout.split('\0')
    return [p for p in paths if p and any(fnmatch.fnmatchcase(p.lower(),g.lower()) for g in patterns)]


def runtime_output(root, output):
    p=Path(output)
    p=p if p.is_absolute() else root/p
    p=p.resolve()
    if not p.is_relative_to((root/'.agent-runtime').resolve()):
        raise ValueError('generated output must be below this repository .agent-runtime/')
    p.mkdir(parents=True,exist_ok=True)
    return p


def site(root, output):
    m=read(root/'research-project.yml');errors=validate(m,root)
    if errors:raise ValueError('; '.join(errors))
    destination=runtime_output(root,output)
    esc=html.escape
    links=[('Authoritative source',m['repository']),('Releases',m['repository']+'/releases'),('Open Codespace',m['publication']['codespace']['url'])]
    if m['publication'].get('citation'):
        links.append(('Citation metadata',m['repository']+'/blob/'+m['default_branch']+'/'+m['publication']['citation']))
    links.append(('Reproduction instructions',m['repository']+'/blob/'+m['default_branch']+'/.agent/maintenance.md'))
    nav=''.join(f'<a href="{esc(url,quote=True)}">{esc(label)}</a>' for label,url in links)
    rows=''.join(f'<tr><th>{esc(k.replace("_"," "))}</th><td>{esc(v)}</td></tr>' for k,v in m['verification'].items() if isinstance(v,str))
    body=f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{esc(m.get('title',m['id']))}</title><style>body{{font:18px/1.6 system-ui;max-width:960px;margin:4rem auto;padding:0 1.5rem;color:#163043;background:#f8fafb}}nav{{display:flex;flex-wrap:wrap;gap:1rem}}a{{color:#00667c}}h1{{line-height:1.2}}table{{border-collapse:collapse;width:100%}}th,td{{text-align:left;padding:.6rem;border-bottom:1px solid #bbcbd2}}.note{{padding:1rem;background:#e9f0f4}}code{{overflow-wrap:anywhere}}</style></head><body><p>Independent research repository</p><h1>{esc(m.get('title',m['id']))}</h1><nav>{nav}</nav><h2>Reproduce and inspect</h2><p>The linked repository owns the manuscript, implementation where present, and verification evidence. Initialize its pinned submodules, then follow its reproduction instructions.</p><p class="note">Repository status: {esc(m['status'])}. Infrastructure checks are distinct from scientific validation. A Codespace link is a launch option, not proof that a remote environment has been tested.</p><h2>Recorded evidence</h2><table>{rows}</table><h2>Current milestone</h2><p>{esc(m['next_milestone'])}</p><p>Shared workflow revision: <code>{esc(m['workflow']['revision'])}</code></p><p>Read the repository's LICENSES.md for the scope of any license; no manuscript license is implied by this site.</p></body></html>'''
    (destination/'index.html').write_text(body+'\n')
    (destination/'research-project.json').write_text(json.dumps(m,indent=2)+'\n')
    return destination


class Links(HTMLParser):
    def __init__(self):
        super().__init__();self.links=[];self.ids=set()
    def handle_starttag(self, tag, attrs):
        a=dict(attrs)
        if 'id' in a:self.ids.add(a['id'])
        for k in ('href','src'):
            if k in a:self.links.append(a[k])


def check_links(directory):
    errors=[];cache={}
    for p in sorted(directory.rglob('*.html')):
        parser=Links();parser.feed(p.read_text());cache[p.resolve()]=parser
    for p, parser in cache.items():
        for link in parser.links:
            u=urlparse(link)
            if u.scheme in {'https','http','mailto','data'}:continue
            if u.scheme or u.netloc:errors.append(f'{p.name}: unsupported link {link}');continue
            target=(p.parent/unquote(u.path)).resolve() if u.path else p
            if target.is_dir():target=target/'index.html'
            if not target.is_relative_to(directory.resolve()) or not target.is_file():
                errors.append(f'{p.name}: missing or escaping link {link}')
            elif u.fragment and target in cache and unquote(u.fragment) not in cache[target].ids:
                errors.append(f'{p.name}: missing fragment {link}')
    return errors


def package(root, output):
    m=read(root/'research-project.yml');errors=validate(m,root)
    if errors:raise ValueError('; '.join(errors))
    destination=runtime_output(root,output)
    head=git(root,'rev-parse','HEAD').stdout.strip()
    source=destination/'source.tar'
    subprocess.run(['git','-C',str(root),'archive','--format=tar','--output',str(source),head],check=True)
    # Include the pinned shared dependency, absent from Git's superproject archive.
    dep=m['workflow']; data=subprocess.check_output(['git','-C',str(root/dep['path']),'archive','--format=tar',dep['revision']])
    with tarfile.open(source,'a') as target,tarfile.open(fileobj=io.BytesIO(data)) as sub:
        for member in sub:
            member.name=dep['path'].rstrip('/')+'/'+member.name
            target.addfile(member,sub.extractfile(member) if member.isfile() else None)
    bundle=destination/'repository.bundle'
    subprocess.run(['git','-C',str(root),'bundle','create',str(bundle),'HEAD'],check=True,capture_output=True)
    provenance={'head':head,'shared_revision':dep['revision'],'source':'committed HEAD only; uncommitted files excluded','dirty_paths_at_packaging':git(root,'status','--porcelain=v1','-uall').stdout.splitlines(),'scientific_release':False,'verification':m['verification']}
    (destination/'provenance.json').write_text(json.dumps(provenance,indent=2)+'\n')
    lines=[]
    for name in ('source.tar','repository.bundle','provenance.json'):
        h=hashlib.sha256()
        with (destination/name).open('rb') as f:
            for chunk in iter(lambda:f.read(1048576),b''):h.update(chunk)
        lines.append(h.hexdigest()+'  '+name)
    (destination/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
    return destination


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--root',type=Path,default=Path.cwd())
    sub=p.add_subparsers(dest='command',required=True)
    sub.add_parser('audit');sub.add_parser('check');sub.add_parser('freeze')
    for name in ('site','package'):
        q=sub.add_parser(name);q.add_argument('--output',default='.agent-runtime/'+name)
    q=sub.add_parser('links');q.add_argument('directory',type=Path)
    args=p.parse_args();root=args.root.resolve()
    try:
        if args.command in {'check','audit'}:
            result=audit(root);print(json.dumps(result,indent=2));return bool(result['errors'])
        if args.command=='freeze':
            blocked=freeze(root)
            if blocked:print('Manuscript freeze rejects staged paths:\n'+'\n'.join(blocked),file=sys.stderr)
            return bool(blocked)
        if args.command=='links':
            errors=check_links(args.directory.resolve());print(json.dumps({'errors':errors}));return bool(errors)
        result=site(root,args.output) if args.command=='site' else package(root,args.output)
        print(result);return 0
    except (OSError,ValueError,KeyError,subprocess.CalledProcessError) as e:
        print(f'research-project: {e}',file=sys.stderr);return 2

if __name__=='__main__':sys.exit(main())
