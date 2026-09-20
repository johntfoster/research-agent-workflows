#!/usr/bin/env python3
"""Index explicit local session stores without exporting transcript text.

JSON/JSONL adapters accept common role/content, message, session_meta/payload,
cwd, timestamp and session-id fields. Unsupported/broken inputs remain reported.
"""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys


def stamp(value):
    if isinstance(value,(int,float)):
        return datetime.fromtimestamp(value/(1000 if value>10**11 else 1),timezone.utc)
    if isinstance(value,str):
        try:
            d=datetime.fromisoformat(value.replace('Z','+00:00'))
            return d if d.tzinfo else d.replace(tzinfo=timezone.utc)
        except ValueError:return None
    return None


def objects(value):
    if isinstance(value,dict):
        yield value
        for key in ('payload','message','messages','data','session','metadata'):
            yield from objects(value.get(key))
    elif isinstance(value,list):
        for item in value:yield from objects(item)


def inspect_file(path, repo, since, until):
    raw=path.read_bytes();sha=hashlib.sha256(raw).hexdigest()
    text=raw.decode('utf-8')
    values=[json.loads(line) for line in text.splitlines() if line.strip()] if path.suffix=='.jsonl' else [json.loads(text)]
    nodes=[n for v in values for n in objects(v)]
    roots={str(n[k]) for n in nodes for k in ('cwd','working_directory','repository_path','repo_path') if isinstance(n.get(k),str)}
    matches=any(Path(s).resolve()==repo or Path(s).resolve().is_relative_to(repo) for s in roots)
    if not matches:return None
    times=[t for n in nodes for k in ('timestamp','created_at','createdAt','updated_at','time') if (t:=stamp(n.get(k)))]
    if times and (max(times)<since or min(times)>until):return None
    messages=[]
    for n in nodes:
        if n.get('role') in {'user','assistant'} and 'content' in n:
            # Do not export private text or hidden reasoning: hashes only.
            content=n['content']
            if isinstance(content,list):content=[x for x in content if isinstance(x,dict) and x.get('type') in {'text','input_text','output_text'}]
            if content:messages.append({'role':n['role'],'content':content})
    digest=hashlib.sha256(json.dumps(messages,sort_keys=True).encode()).hexdigest() if messages else sha
    return {'file':str(path),'sha256':sha,'message_digest':digest,'visible_messages':len(messages),
            'first_timestamp':min(times).isoformat() if times else None,'last_timestamp':max(times).isoformat() if times else None,
            'coverage':'matched-repository-and-window' if times else 'matched-repository-time-unknown'}


def collect(repo, sources, since, until):
    entries=[];limitations=[];seen={}
    for label,root in sources:
        if not root.exists():limitations.append({'source':label,'reason':'unavailable'});continue
        paths=[root] if root.is_file() else sorted(p for p in root.rglob('*') if p.is_file() and p.suffix in {'.json','.jsonl'})
        for path in paths:
            try:
                item=inspect_file(path,repo,since,until)
                if item:
                    item['source']=label;key=item['message_digest']
                    if key in seen:seen[key].setdefault('mirrors',[]).append(str(path))
                    else:seen[key]=item;entries.append(item)
            except (OSError,ValueError,UnicodeError) as e:
                limitations.append({'source':label,'file':str(path),'reason':type(e).__name__})
    return {'schema_version':1,'repository':str(repo),'since':since.isoformat(),'until':until.isoformat(),'sessions':entries,'limitations':limitations,
            'coverage_note':'Only explicitly supplied accessible stores were scanned. Unnamed machines/harnesses are not covered. This index contains no reasoning narrative.'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--repo',type=Path,required=True);p.add_argument('--since',required=True);p.add_argument('--until',required=True);p.add_argument('--source',action='append',default=[],help='harness=path; repeat for accessible stores')
    a=p.parse_args();since,until=stamp(a.since),stamp(a.until)
    if not since or not until or since>until:p.error('valid ordered ISO timestamps required')
    sources=[]
    for s in a.source:
        label,sep,path=s.partition('=')
        if not sep or not label or not path:p.error('source must be harness=path')
        sources.append((label,Path(path)))
    print(json.dumps(collect(a.repo.resolve(),sources,since,until),indent=2));return 0
if __name__=='__main__':sys.exit(main())
