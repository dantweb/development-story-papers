#!/usr/bin/env python3
"""Join GitHub Actions runs to the commit record; emit three CSVs."""
import csv, json, subprocess
from collections import defaultdict, Counter
from datetime import datetime
T='/home/dtkachev/.claude/jobs/dafaedde/tmp/'
D='/home/dtkachev/dantweb/development-story-papers/data/'
REPOS={'stripe-wallet':'/home/dtkachev/osc/strpwt7-nov26/source/extensions/stripe',
       'payment-base':'/home/dtkachev/osc/strpwt7-nov26/source/extensions/payment-base'}

R=[json.loads(l) for f in ('runs_stripe-wallet.jsonl','runs_payment-base.jsonl') for l in open(T+f)]

# commit metadata: sha12 -> row  (also index full shas)
C={c['sha']:c for c in csv.DictReader(open(D+'commits.csv'))}
L={r['sha']:r for r in csv.DictReader(open(D+'commit_loc_by_category.csv'))}
full2short={}
for repo,path in REPOS.items():
    for s in subprocess.run(['git','-C',path,'rev-list','--all'],capture_output=True,text=True).stdout.split():
        full2short[s]=s[:12]

def dur(a,b):
    try: return round((datetime.fromisoformat(b.replace('Z','+00:00'))-datetime.fromisoformat(a.replace('Z','+00:00'))).total_seconds())
    except Exception: return ''

# ---------- 1. one row per run ----------
rows=[]
for r in R:
    sh=full2short.get(r['head_sha'],'')
    c=C.get(sh); loc=L.get(sh)
    rows.append({
        'repo':r['repo'],'run_id':r['run_id'],'run_number':r['run_number'],
        'run_attempt':r['run_attempt'],'workflow_name':r['name'],
        'workflow_path':r['path'],'event':r['event'],'conclusion':r['conclusion'],
        'created_at':r['created_at'],'duration_seconds':dur(r['run_started_at'] or r['created_at'],r['updated_at']),
        'head_branch':r['head_branch'],'actor':r['actor'],
        'head_sha':r['head_sha'][:12],
        'commit_in_corpus':1 if c else 0,
        'commit_date':c['date'] if c else '','commit_author':c['author'] if c else '',
        'files_changed':c['files_changed'] if c else '',
        'insertions':c['insertions'] if c else '','deletions':c['deletions'] if c else '',
        'src_ins':loc['src_ins'] if loc else '','tests_ins':loc['tests_ins'] if loc else '',
        'ai_coauthored':c['ai_coauthored'] if c else '',
        'commit_subject':c['subject'] if c else '',
    })
rows.sort(key=lambda x:x['created_at'])
cols=['repo','run_id','run_number','run_attempt','workflow_name','workflow_path','event',
      'conclusion','created_at','duration_seconds','head_branch','actor','head_sha',
      'commit_in_corpus','commit_date','commit_author','files_changed','insertions',
      'deletions','src_ins','tests_ins','ai_coauthored','commit_subject']
with open(D+'actions_runs.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(rows)

# ---------- 2. one row per commit that has runs ----------
byc=defaultdict(list)
for x in rows:
    if x['commit_in_corpus']: byc[x['head_sha']].append(x)
crows=[]
for sh,rs in byc.items():
    c=C[sh]; loc=L.get(sh,{})
    con=Counter(x['conclusion'] for x in rs)
    ds=[int(x['duration_seconds']) for x in rs if x['duration_seconds']!='']
    rs_sorted=sorted(rs,key=lambda x:x['created_at'])
    crows.append({
        'repo':c['repo'],'sha':sh,'date':c['date'],'author':c['author'],
        'insertions':c['insertions'],'deletions':c['deletions'],'files_changed':c['files_changed'],
        'src_ins':loc.get('src_ins',''),'tests_ins':loc.get('tests_ins',''),
        'docs_ins':loc.get('docs_ins',''),'ci_ins':loc.get('ci_ins',''),
        'ai_coauthored':c['ai_coauthored'],'ticket_ref':c['ticket_ref'],
        'runs':len(rs),'success':con.get('success',0),'failure':con.get('failure',0),
        'cancelled':con.get('cancelled',0),
        'any_failure':1 if con.get('failure',0) else 0,
        'all_success':1 if con.get('success',0)==len(rs) else 0,
        'first_conclusion':rs_sorted[0]['conclusion'],
        'last_conclusion':rs_sorted[-1]['conclusion'],
        'max_run_attempt':max(int(x['run_attempt']) for x in rs),
        'total_ci_seconds':sum(ds),'workflows':len({x['workflow_name'] for x in rs}),
        'subject':c['subject'],
    })
crows.sort(key=lambda x:x['date'])
ccols=['repo','sha','date','author','insertions','deletions','files_changed','src_ins',
       'tests_ins','docs_ins','ci_ins','ai_coauthored','ticket_ref','runs','success',
       'failure','cancelled','any_failure','all_success','first_conclusion',
       'last_conclusion','max_run_attempt','total_ci_seconds','workflows','subject']
with open(D+'actions_by_commit.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=ccols);w.writeheader();w.writerows(crows)

# ---------- 3. per workflow ----------
bw=defaultdict(list)
for x in rows: bw[(x['repo'],x['workflow_name'])].append(x)
wrows=[]
for (repo,name),rs in bw.items():
    con=Counter(x['conclusion'] for x in rs)
    ds=[int(x['duration_seconds']) for x in rs if x['duration_seconds']!='']
    n=len(rs)
    wrows.append({'repo':repo,'workflow_name':name,'runs':n,
        'success':con.get('success',0),'failure':con.get('failure',0),
        'cancelled':con.get('cancelled',0),
        'failure_rate_pct':round(100*con.get('failure',0)/n,1),
        'median_duration_seconds':sorted(ds)[len(ds)//2] if ds else '',
        'total_duration_seconds':sum(ds),
        'first_run':min(x['created_at'] for x in rs)[:10],
        'last_run':max(x['created_at'] for x in rs)[:10]})
wrows.sort(key=lambda x:-x['runs'])
with open(D+'actions_workflows.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(wrows[0].keys()));w.writeheader();w.writerows(wrows)

print(f"actions_runs.csv       {len(rows)} rows")
print(f"actions_by_commit.csv  {len(crows)} rows")
print(f"actions_workflows.csv  {len(wrows)} rows")
tot=Counter(x['conclusion'] for x in rows)
print(f"\nconclusions: {dict(tot)}  failure rate = {100*tot['failure']/len(rows):.1f}%")
print(f"runs joined to a corpus commit: {sum(x['commit_in_corpus'] for x in rows)}/{len(rows)}")
ci=sum(int(x['duration_seconds']) for x in rows if x['duration_seconds']!='')
print(f"total CI wall-clock: {ci/3600:.1f} h")
