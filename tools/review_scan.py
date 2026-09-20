#!/usr/bin/env python3
"""Read-only prose triage; findings require contextual editorial review."""
import argparse
import hashlib
import json
from pathlib import Path
import re

RULES={
 'negative-positioning':r'\b(?:unlike (?:prior|previous|existing)|not merely|not ad hoc|prior (?:models|work) (?:do not|does not|lack))\b',
 'drafting-history':r'\b(?:as requested|in the previous draft|we now fix|this revision addresses)\b',
 'unsupported-rhetoric':r'\b(?:obviously|trivially|unprecedented|groundbreaking)\b',
 'manual-delimiter':r'\\(?:big|Big|bigg|Bigg)[lrm]?\b',
 'unnumbered-display':r'\\\[|\\begin\{(?:equation|align)\*\}'
}
CRITERIA=['physical purpose and engineering consequence','purpose → equation → definitions → implication → limit','just-in-time definitions and necessary notation','explicit non-obvious derivation steps','positive contribution and supported scope','logical transitions','equation/citation/claim preservation']

def scan(text):
    findings=[]
    for key,pattern in RULES.items():
        for match in re.finditer(pattern,text,re.IGNORECASE):
            findings.append({'rule':key,'line':text.count('\n',0,match.start())+1,'excerpt':match.group()})
    return {'findings':sorted(findings,key=lambda x:(x['line'],x['rule'])),'requires_contextual_review':CRITERIA,'scientific_correctness':'not-assessed','edits_applied':False}

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);a=p.parse_args()
    data=a.source.read_bytes();result=scan(data.decode());result['sha256']=hashlib.sha256(data).hexdigest();print(json.dumps(result,indent=2))
if __name__=='__main__':main()
