#!/usr/bin/env python3
"""Statistical tests for the lessons-learned claims. No scipy: exact/manual implementations."""
import csv, math, random
from collections import Counter, defaultdict
import numpy as np
D='/home/dtkachev/dantweb/development-story-papers/data/'
random.seed(12345); np.random.seed(12345)

# ---------- distributions ----------
def gammaincc(a, x):
    """Regularized upper incomplete gamma Q(a,x). Numerical Recipes gser/gcf."""
    if x < 0 or a <= 0: raise ValueError
    if x == 0: return 1.0
    gln = math.lgamma(a)
    if x < a + 1.0:                      # series for P, then Q = 1-P
        ap, s, dl = a, 1.0/a, 1.0/a
        for _ in range(1000):
            ap += 1; dl *= x/ap; s += dl
            if abs(dl) < abs(s)*1e-15: break
        return 1.0 - s*math.exp(-x + a*math.log(x) - gln)
    # continued fraction for Q
    FPMIN=1e-300
    b = x + 1.0 - a; c = 1.0/FPMIN; d = 1.0/b; h = d
    for i in range(1, 1000):
        an = -i*(i-a); b += 2.0
        d = an*d + b
        if abs(d) < FPMIN: d = FPMIN
        c = b + an/c
        if abs(c) < FPMIN: c = FPMIN
        d = 1.0/d; de = d*c; h *= de
        if abs(de-1.0) < 1e-15: break
    return math.exp(-x + a*math.log(x) - gln) * h

def chi2_sf(chi2, df):
    return gammaincc(df/2.0, chi2/2.0)

def binom_sf_two_sided(k, n, p):
    """Two-sided exact binomial p-value (method of small p's)."""
    pk = math.comb(n,k)*p**k*(1-p)**(n-k)
    tot = 0.0
    for i in range(n+1):
        pi = math.comb(n,i)*p**i*(1-p)**(n-i)
        if pi <= pk*(1+1e-12): tot += pi
    return min(1.0, tot)

def fisher_2x2(a,b,c,d):
    """Two-sided Fisher exact test on [[a,b],[c,d]]."""
    n = a+b+c+d; r1=a+b; c1=a+c
    def hg(x):
        lo=max(0,c1-(n-r1)); hi=min(r1,c1)
        if x<lo or x>hi: return 0.0
        return math.comb(r1,x)*math.comb(n-r1,c1-x)/math.comb(n,c1)
    p_obs = hg(a); lo=max(0,c1-(n-r1)); hi=min(r1,c1)
    return min(1.0, sum(hg(x) for x in range(lo,hi+1) if hg(x) <= p_obs*(1+1e-12)))

def fmt_p(p):
    if p == 0: return "< 1e-300"
    if p < 1e-4: return f"{p:.2e}"
    return f"{p:.4f}"

C=list(csv.DictReader(open(D+'commits.csv')))
L=list(csv.DictReader(open(D+'commit_loc_by_category.csv')))
J=list(csv.DictReader(open(D+'jira_issues.csv')))
SQ='6e828a242d6b'

print("="*74)
print("T1  Test code exceeds production code (LL-3 / N-4)")
print("="*74)
m=defaultdict(lambda:[0,0])
for r in L:
    if r['sha']==SQ: continue
    k=r['date'][:7]; m[k][0]+=int(r['src_ins']); m[k][1]+=int(r['tests_ins'])
months=sorted(m); wins=sum(1 for k in months if m[k][1]>m[k][0])
print(f"  months where test+ > src+: {wins}/{len(months)}")
p=binom_sf_two_sided(wins,len(months),0.5)
print(f"  exact two-sided sign test vs p=0.5:  p = {fmt_p(p)}")
si=sum(m[k][0] for k in months); ti=sum(m[k][1] for k in months)
print(f"  pooled ratio = {ti/si:.3f}  (tests +{ti:,} / src +{si:,})")
# bootstrap CI over commits
pairs=np.array([[int(r['src_ins']),int(r['tests_ins'])] for r in L if r['sha']!=SQ])
boot=[]
for _ in range(20000):
    idx=np.random.randint(0,len(pairs),len(pairs)); s=pairs[idx].sum(axis=0)
    if s[0]>0: boot.append(s[1]/s[0])
lo,hi=np.percentile(boot,[2.5,97.5])
print(f"  bootstrap 95% CI on the ratio (20k resamples of commits): [{lo:.2f}, {hi:.2f}]")
print(f"  -> ratio > 1 in {100*np.mean(np.array(boot)>1):.1f}% of resamples")

print()
print("="*74)
print("T2  Role separation: reporters do not file all issue types (LL-6 / N-3)")
print("="*74)
dev=[r for r in J if r['reporter'].startswith('Daniil')]
qa=[r for r in J if r['reporter'].startswith('Zerfas')]
a=sum(1 for r in dev if r['issue_type']=='Story'); b=sum(1 for r in dev if r['issue_type']=='Bug')
c=sum(1 for r in qa if r['issue_type']=='Story'); d=sum(1 for r in qa if r['issue_type']=='Bug')
print(f"  2x2 (developer vs tester) x (Story vs Bug) = [[{a},{b}],[{c},{d}]]")
print(f"  Fisher exact, two-sided:  p = {fmt_p(fisher_2x2(a,b,c,d))}")
# full contingency, top reporters x 3 types
types=['Story','Task','Bug']
reps=[r for r,n in Counter(x['reporter'] for x in J).most_common(4)]
tab=[[sum(1 for x in J if x['reporter']==rp and x['issue_type']==t) for t in types] for rp in reps]
n=sum(sum(row) for row in tab)
rt=[sum(row) for row in tab]; ct=[sum(tab[i][j] for i in range(len(tab))) for j in range(len(types))]
chi2=sum((tab[i][j]-rt[i]*ct[j]/n)**2/(rt[i]*ct[j]/n) for i in range(len(tab)) for j in range(len(types)) if rt[i]*ct[j]>0)
df=(len(tab)-1)*(len(types)-1)
V=math.sqrt(chi2/(n*min(len(tab)-1,len(types)-1)))
print(f"  full table {reps} x {types}")
for rp,row in zip(reps,tab): print(f"    {rp:<20} {row}")
print(f"  chi-square = {chi2:.1f}, df = {df},  p = {fmt_p(chi2_sf(chi2,df))},  Cramer's V = {V:.3f}")

print()
print("="*74)
print("T3  AI-trailer adoption is a step change, not a trend (LL-5 / N-2)")
print("="*74)
pre=[x for x in C if x['date']<'2026-05-07']; post=[x for x in C if x['date']>='2026-05-07']
a=sum(int(x['ai_coauthored']) for x in pre); b=len(pre)-a
c=sum(int(x['ai_coauthored']) for x in post); d=len(post)-c
print(f"  before 2026-05-07: {a}/{len(pre)} trailered ({100*a/len(pre):.1f}%)")
print(f"  from   2026-05-07: {c}/{len(post)} trailered ({100*c/len(post):.1f}%)")
print(f"  Fisher exact, two-sided:  p = {fmt_p(fisher_2x2(a,b,c,d))}")

print()
print("="*74)
print("T4  Weekend abstention (LL-8 / M-14)")
print("="*74)
sat=sum(1 for x in C if x['weekday']=='Sat'); sun=sum(1 for x in C if x['weekday']=='Sun')
n=len(C)
print(f"  Saturday commits: {sat}/{n};  Sunday: {sun}/{n}")
lp=n*math.log(6/7)
print(f"  P(zero Saturdays | commits uniform over 7 days) = {math.exp(lp):.3e}  (log10 = {lp/math.log(10):.1f})")
wd=Counter(x['weekday'] for x in C)
obs=[wd[k] for k in ['Mon','Tue','Wed','Thu','Fri']]; N=sum(obs); E=N/5
chi2=sum((o-E)**2/E for o in obs)
print(f"  weekday spread Mon-Fri {obs} vs uniform ({E:.1f} each)")
print(f"  chi-square = {chi2:.1f}, df = 4,  p = {fmt_p(chi2_sf(chi2,4))}  -> weekdays are NOT uniform (Wed heavy)")

print()
print("="*74)
print("T5  Cadence is bursty, not steady (LL-1 / M-12)")
print("="*74)
per=Counter(x['date'] for x in C); v=np.array(list(per.values()))
print(f"  active days = {len(v)}, mean = {v.mean():.2f}, variance = {v.var(ddof=1):.2f}, median = {np.median(v):.0f}, max = {v.max()}")
disp=v.var(ddof=1)/v.mean()
chi2=disp*(len(v)-1)
print(f"  dispersion index (var/mean) = {disp:.2f}  (Poisson expects 1.0)")
print(f"  overdispersion test: chi-square = {chi2:.1f}, df = {len(v)-1},  p = {fmt_p(chi2_sf(chi2,len(v)-1))}")

print()
print("="*74)
print("T6  Issue-to-code coverage depends on issue type (LL-6 / M-19)")
print("="*74)
tab=[]; labs=['Story','Task','Bug','Sub-task']
for t in labs:
    rows=[x for x in J if x['issue_type']==t]
    yes=sum(1 for x in rows if x['has_code']=='1'); tab.append([yes,len(rows)-yes])
    print(f"  {t:<10} {yes:>3}/{len(rows):<3} ({100*yes/len(rows):.0f}%)")
n=sum(sum(r) for r in tab)
rt=[sum(r) for r in tab]; ct=[sum(tab[i][j] for i in range(len(tab))) for j in range(2)]
chi2=sum((tab[i][j]-rt[i]*ct[j]/n)**2/(rt[i]*ct[j]/n) for i in range(len(tab)) for j in range(2) if rt[i]*ct[j]>0)
print(f"  chi-square = {chi2:.1f}, df = 3,  p = {fmt_p(chi2_sf(chi2,3))}")

print()
print("="*74)
print("T7  PM-1: did decimal sub-sprints improve 1-commit mapping? (UNDERPOWERED)")
print("="*74)
import re
sp=defaultdict(int)
for x in C:
    if x['sprint_ref']: sp[x['sprint_ref']]+=1
dec=[k for k in sp if '.' in k]; wh=[k for k in sp if '.' not in k]
da=sum(1 for k in dec if sp[k]==1); db=len(dec)-da
wa=sum(1 for k in wh if sp[k]==1); wb=len(wh)-wa
print(f"  decimal sub-sprints with exactly 1 commit: {da}/{len(dec)} ({100*da/len(dec):.0f}%)")
print(f"  whole sprints with exactly 1 commit:       {wa}/{len(wh)} ({100*wa/len(wh):.0f}%)")
print(f"  Fisher exact, two-sided:  p = {fmt_p(fisher_2x2(da,db,wa,wb))}   <-- NOT significant")
print(f"  => the COMPARISON is underpowered (n={len(dec)} vs {len(wh)} groups).")
print(f"  What IS established without inference: {db}/{len(dec)} ({100*db/len(dec):.0f}%) of decimal")
print(f"  sub-sprints span >1 commit, median {np.median([sp[k] for k in dec]):.0f} - so the convention")
print(f"  demonstrably did not produce 1 commit per phase, whatever ordinary sprints did.")

print()
print("="*74)
print("T8  Out-of-hours work is concentrated (LL-8)")
print("="*74)
oh=[x for x in C if int(x['hour_local'])>=20 or int(x['hour_local'])<8]
byday=Counter(x['date'] for x in oh)
top=byday.most_common(1)[0]
print(f"  out-of-hours commits: {len(oh)} on {len(byday)} distinct days")
print(f"  largest single day: {top[0]} with {top[1]} ({100*top[1]/len(oh):.0f}% of all out-of-hours)")
p=binom_sf_two_sided(top[1],len(oh),1/len(byday))
print(f"  exact binomial vs uniform over those {len(byday)} days: p = {fmt_p(p)}")

print()
print("="*74)
print("T9  GitHub Actions: CI failure rate, and does commit size predict it?")
print("="*74)
A=list(csv.DictReader(open(D+'actions_runs.csv')))
B=list(csv.DictReader(open(D+'actions_by_commit.csv')))
con=Counter(x['conclusion'] for x in A)
n=len(A)
print(f"  runs = {n}: success {con['success']}, failure {con['failure']}, cancelled {con['cancelled']}")
print(f"  failure rate = {100*con['failure']/n:.1f}%")
print("  NOTE: no coin-flip test is reported. An earlier revision ran an exact binomial")
print("  against 0.5 (p=0.28); that test ASSUMES INDEPENDENT RUNS and is INVALID -- see T10")
print("  (lag-1 autocorrelation 0.680). The failure proportion is a census fact needing no test.")
ci=sum(int(x['duration_seconds']) for x in A if x['duration_seconds'])
print(f"  total CI wall-clock = {ci/3600:.1f} h  (vs ~140.1 h of measured human session time)")
wasted=sum(int(x['duration_seconds']) for x in A if x['duration_seconds'] and x['conclusion']=='failure')
print(f"  wall-clock in FAILING runs = {wasted/3600:.1f} h ({100*wasted/ci:.0f}% of CI time)")

print()
print("  -- does commit size predict CI failure? (per-commit, n=%d) --" % len(B))
big=[x for x in B if int(x['insertions'])>=500]; small=[x for x in B if int(x['insertions'])<500]
a=sum(int(x['any_failure']) for x in big); b=len(big)-a
c=sum(int(x['any_failure']) for x in small); d=len(small)-c
print(f"    >=500 insertions: {a}/{len(big)} commits had >=1 failing run ({100*a/len(big):.0f}%)")
print(f"    < 500 insertions: {c}/{len(small)} ({100*c/len(small):.0f}%)")
print(f"    Fisher exact, two-sided:  p = {fmt_p(fisher_2x2(a,b,c,d))}")
# rank correlation insertions vs any_failure
ins=np.array([int(x['insertions']) for x in B],dtype=float)
fail=np.array([int(x['any_failure']) for x in B],dtype=float)
def rankdata(v):
    o=np.argsort(v,kind='mergesort'); r=np.empty(len(v)); r[o]=np.arange(1,len(v)+1)
    # average ties
    vals,inv,cnt=np.unique(v,return_inverse=True,return_counts=True)
    means=np.zeros(len(vals))
    for i in range(len(vals)):
        means[i]=r[v==vals[i]].mean()
    return means[inv]
rx,ry=rankdata(ins),rankdata(fail)
rho=np.corrcoef(rx,ry)[0,1]
t=rho*math.sqrt((len(B)-2)/max(1e-12,1-rho**2))
# two-sided p from normal approx
pz=2*(1-0.5*(1+math.erf(abs(t)/math.sqrt(2))))
print(f"    Spearman rho(insertions, any_failure) = {rho:.3f},  approx p = {fmt_p(pz)}")

print()
print("  -- AI-trailered commits vs the rest --")
ai=[x for x in B if x['ai_coauthored']=='1']; na=[x for x in B if x['ai_coauthored']=='0']
if ai and na:
    a=sum(int(x['any_failure']) for x in ai); b=len(ai)-a
    c=sum(int(x['any_failure']) for x in na); d=len(na)-c
    print(f"    AI-trailered:  {a}/{len(ai)} with a failing run ({100*a/len(ai):.0f}%)")
    print(f"    not trailered: {c}/{len(na)} ({100*c/len(na):.0f}%)")
    print(f"    Fisher exact, two-sided:  p = {fmt_p(fisher_2x2(a,b,c,d))}")

print()
print("  -- failure rate by half of the record --")
mid='2026-04-01'
for lab,sel in (('before '+mid,[x for x in A if x['created_at'][:10]<mid]),('from '+mid,[x for x in A if x['created_at'][:10]>=mid])):
    cc=Counter(x['conclusion'] for x in sel)
    tot=cc['success']+cc['failure']
    if tot: print(f"    {lab:<16} {cc['failure']}/{tot} failed ({100*cc['failure']/tot:.0f}%)")
e=[x for x in A if x['created_at'][:10]<mid]; l=[x for x in A if x['created_at'][:10]>=mid]
ea=sum(1 for x in e if x['conclusion']=='failure'); eb=sum(1 for x in e if x['conclusion']=='success')
la=sum(1 for x in l if x['conclusion']=='failure'); lb=sum(1 for x in l if x['conclusion']=='success')
print(f"    Fisher exact, two-sided:  p = {fmt_p(fisher_2x2(ea,eb,la,lb))}")

print()
print("="*74)
print("T10  CI outcomes are strongly autocorrelated (invalidates naive run-level tests)")
print("="*74)
seq=defaultdict(list)
for r in sorted(A,key=lambda x:x['created_at']):
    if r['conclusion'] in ('success','failure'):
        seq[(r['repo'],r['workflow_name'])].append(1 if r['conclusion']=='failure' else 0)
xs=[];ys=[];trans=0;tot=0;prev_fail=0;tot_fail=0
for k,v in seq.items():
    for i in range(1,len(v)):
        xs.append(v[i-1]); ys.append(v[i]); tot+=1
        if v[i]!=v[i-1]: trans+=1
        if v[i]==1:
            tot_fail+=1
            if v[i-1]==1: prev_fail+=1
nn=sum(len(v) for v in seq.values())
pfail=sum(sum(v) for v in seq.values())/nn
mx=sum(xs)/len(xs); my=sum(ys)/len(ys)
num=sum((a-mx)*(b-my) for a,b in zip(xs,ys))
den=math.sqrt(sum((a-mx)**2 for a in xs)*sum((b-my)**2 for b in ys))
rho1=num/den
print(f"  decided runs = {nn}, failure proportion = {pfail:.4f}")
print(f"  failures preceded by another failure: {prev_fail}/{tot_fail} = {100*prev_fail/tot_fail:.1f}%")
print(f"     (published comparison: '>50% of failed builds follow a previous failure' for 10 projects)")
print(f"  outcome transitions: {trans}/{tot} = {100*trans/tot:.1f}%  (expected under independence: {100*2*pfail*(1-pfail):.1f}%)")
print(f"  lag-1 autocorrelation = {rho1:.3f}")
defl=(1-rho1)/(1+rho1)
print(f"  AR(1) effective-sample deflation factor = {defl:.3f}  ->  n_eff ~ {nn*defl:.0f} (nominal {nn})")
print()
print("  Consequence for T9b (the 57%->46% trend):")
mid='2026-04-01'
e=[x for x in A if x['created_at'][:10]<mid and x['conclusion'] in('success','failure')]
l=[x for x in A if x['created_at'][:10]>=mid and x['conclusion'] in('success','failure')]
ea=sum(1 for x in e if x['conclusion']=='failure'); eb=len(e)-ea
la=sum(1 for x in l if x['conclusion']=='failure'); lb=len(l)-la
print(f"    nominal Fisher p = {fmt_p(fisher_2x2(ea,eb,la,lb))}")
sa,sb,sc,sd=[max(1,round(v*defl)) for v in (ea,eb,la,lb)]
print(f"    deflated [[{sa},{sb}],[{sc},{sd}]] -> Fisher p = {fmt_p(fisher_2x2(sa,sb,sc,sd))}")
print("    => the improvement DOES NOT survive as a significant result. Demoted to descriptive.")
print()
Bs=sorted(B,key=lambda x:x['date'])
v=[int(x['any_failure']) for x in Bs]
mxb=sum(v)/len(v)
nb=sum((v[i-1]-mxb)*(v[i]-mxb) for i in range(1,len(v)))
db=sum((a-mxb)**2 for a in v)
print(f"  per-COMMIT any_failure lag-1 autocorrelation = {nb/db:.3f} (n={len(v)}) -- weaker.")
print("  T9a and T9c are per-commit NULLS; autocorrelation inflates false positives, so a")
print("  surviving null is conservative. They stand.")
