#!/usr/bin/env python3
"""Create an infrastructure-only paper scaffold; never overwrite a destination."""
import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
from research_project import CORE, DEFAULT_PROTECTED, CATEGORIES


def create(dest, project_id, repository, revision, title):
    if dest.exists():raise ValueError('destination already exists')
    if not re.fullmatch('[a-z0-9][a-z0-9_-]*',project_id):raise ValueError('invalid project id')
    if not re.fullmatch('[0-9a-f]{40}',revision):raise ValueError('exact shared revision required')
    if not repository.startswith('https://github.com/'):raise ValueError('HTTPS GitHub repository required')
    dest.mkdir(parents=True)
    subprocess.run(['git','init','-q','-b','main',str(dest)],check=True)
    (dest/'AGENTS.md').write_text('# Paper authority\n\nThis independent paper owns its scientific authority. Read the pinned shared\nworkflow and local project manifest. Manuscript creation and edits require an\nexplicit task. Preserve manuscript freeze and unrelated work.\n')
    (dest/'README.md').write_text('# '+title+'\n\nInfrastructure scaffold; manuscript authoring has not started. Initialize\nsubmodules and install tracked hooks before work. No scientific verification is\nclaimed. Fill the authority and publication metadata before conformance checks.\n')
    (dest/'.gitignore').write_text('.agent-runtime/\nbuild/\n__pycache__/\n')
    (dest/'.gitmodules').write_text('[submodule ".agent/shared"]\n\tpath = .agent/shared\n\turl = https://github.com/johntfoster/research-agent-workflows.git\n')
    profile=json.loads((CORE/'agent-profile.json').read_text());profile['manuscript_root']='main.tex';profile['build_directory']='build'
    (dest/'agent-profile.json').write_text(json.dumps(profile,indent=2)+'\n')
    manifest={'schema_version':1,'id':project_id,'title':title,'repository':repository,'default_branch':'main','status':'incubating','authority':{'instructions':'AGENTS.md','profile':'agent-profile.json','manuscript':'main.tex'},'workflow':{'repository':'https://github.com/johntfoster/research-agent-workflows','path':'.agent/shared','revision':revision,'release':'explicit-pin'},'maintenance':{'manuscript_edits':False,'protected_paths':list(DEFAULT_PROTECTED)},'publication':{'site':{'url':None,'status':'not-configured'},'codespace':{'url':'https://codespaces.new/'+repository.removeprefix('https://github.com/'),'verification':'not-run'},'citation':None,'license':{'status':'owner-decision-needed'},'release':{'status':'not-created'}},'verification':{k:'not-run' for k in CATEGORIES},'next_milestone':'Author the manuscript only under an explicit request, then validate this scaffold.'}
    (dest/'research-project.yml').write_text(json.dumps(manifest,indent=2)+'\n')
    shutil.copytree(CORE/'templates/hooks',dest/'.githooks')
    workflows=dest/'.github/workflows';workflows.mkdir(parents=True)
    (workflows/'pages.yml').write_text((CORE/'templates/workflows/pages.yml').read_text().replace('__SHARED_REVISION__',revision))
    (dest/'tools').mkdir();(dest/'tools/agentctl').symlink_to('../.agent/shared/tools/agentctl')
    subprocess.run(['git','-C',str(dest),'update-index','--add','--cacheinfo',f'160000,{revision},.agent/shared'],check=True)
    subprocess.run(['git','-C',str(dest),'config','core.hooksPath','.githooks'],check=True)
    return dest


def main():
    p=argparse.ArgumentParser(description=__doc__)
    for name in ('destination','id','repository','revision','title'):p.add_argument('--'+name,required=True)
    a=p.parse_args()
    try:print(create(Path(a.destination),a.id,a.repository,a.revision,a.title))
    except ValueError as e:p.error(str(e))
if __name__=='__main__':main()
