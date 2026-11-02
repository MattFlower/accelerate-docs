"""Phase 0c replays on stored trials using judged matches (consensus of Claude+Terra where both exist, else Claude)."""
import json,os,sqlite3,collections
R=os.path.expanduser('~/limitless-orch/review-research/')
exec(open(R+'scripts/rescore.py').read().split('agg=collections')[0])  # items, CL, TE, jm, BLK, cases
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
TRUE_CLEAN_EXCLUDE={'review-068','review-092','review-108'}   # relabelled real 10-29 (clean_adjudication.md)
def caught_by(k,gid,fs,rule):
    """consensus: both judges' matched findings satisfy the rule (either judge's duplicate is fine); a lone judge needs conf>=0.8"""
    def ok(J):
        m=next((m for m in (J.get(k) or []) if m.get('gold')==gid),None)
        if m is None: return None,0
        f=m.get('finding'); return (bool(f) and rule(fs[int(f[1:])-1])), (m.get('confidence') or 0)
    (c,cc),(t,tc)=ok(CL),ok(TE)
    if c is None or t is None: return bool(c or t)
    if c and t: return True
    if c and not t: return cc>=0.8 and False
    return False
def trials(ev):
    for cid,trial,oj,dj in db.execute("select case_id,trial,output_json,details_json from eval_trials where eval_run_id=? and status='ok'",(ev,)):
        yield cid,trial,json.loads(oj),json.loads(dj).get('system')
def recall_and_fb(ev,system,rule):
    rc=collections.Counter()
    for cid,trial,o,s in trials(ev):
        if s!=system: continue
        c=cases[cid]; fs=o.get('findings',[])
        blocking=[i for i,f in enumerate(fs) if rule(f)]
        if not any(d.get('required') for d in c.get('defects',[])):
            if cid in TRUE_CLEAN_EXCLUDE: continue
            rc['clean_n']+=1; rc['clean_blk']+=bool(blocking); continue
        k=f'{ev}|{s}|{cid}|{trial}'
        if k not in items: continue
        for g in items[k]['gold']:
            rc['n']+=1; rc['caught']+=caught_by(k,g['id'],fs,rule)
    return rc
std=lambda f:f.get('severity') in BLK
agree2=lambda f:f.get('severity') in BLK and (f.get('agreement') or 1)>=2
anysev=lambda f:True
def show(label,rc): print(f"{label:60} recall {rc['caught']}/{rc['n']} = {100*rc['caught']/max(1,rc['n']):.1f}%   clean blocks {rc['clean_blk']}/{rc['clean_n']}")
for ev,split in [('eval-mvi7bktt0cz50o81qkik8c','dev'),('eval-mvif9n84010bmzy1tk9std','heldout')]:
    show(f'D {split} standard rule (any blocker/major)',recall_and_fb(ev,'D-adversarial-union2',std))
    show(f'D {split} two-tier: block only if both samples agree',recall_and_fb(ev,'D-adversarial-union2',agree2))
show('heldout production standard (mv92)',recall_and_fb('eval-mv92iu6p0y8ns1b0ifjg8t','sol-6.1-medium-standard',std))
show('heldout production standard on #542 cases (mvih)',recall_and_fb('eval-mvih4jfr07m09eu0wfoy22','sol-6.1-medium-standard',std))
show('heldout adversarial single (mv92)',recall_and_fb('eval-mv92iu6p0y8ns1b0ifjg8t','sol-6.1-medium-adversarial',std))
# Sol ∪ Opus on E2 (paired): per (case,trial), union of Sol blocking and Opus findings
E2='eval-mv7rznhb0nugf7t09om5i6'
by=collections.defaultdict(dict)
for cid,trial,o,s in trials(E2): by[(cid,trial)][s]=o
for label,orule in [('Sol∪Opus(blocking)',std),('Sol∪Opus(any severity)',anysev)]:
    rc=collections.Counter()
    for (cid,trial),d in by.items():
        c=cases[cid]
        if not any(x.get('required') for x in c.get('defects',[])):
            b=any(std(f) for f in d.get('codex/sol-6.1@medium',{}).get('findings',[])) or any(orule(f) for f in d.get('claude/opus',{}).get('findings',[]))
            rc['clean_n']+=1; rc['clean_blk']+=b; continue
        caught=set()
        for s,rule in [('codex/sol-6.1@medium',std),('claude/opus',orule)]:
            k=f'{E2}|{s}|{cid}|{trial}'
            if k not in items: continue
            fs=d[s].get('findings',[])
            for g in items[k]['gold']:
                if caught_by(k,g['id'],fs,rule): caught.add(g['id'])
        n=len([x for x in c['defects'] if x.get('required')]); rc['n']+=n; rc['caught']+=len(caught)
    show('E2 dev '+label,rc)
show('E2 dev Sol alone',recall_and_fb(E2,'codex/sol-6.1@medium',std))
show('E2 dev Opus alone (blocking)',recall_and_fb(E2,'claude/opus',std))
show('E2 dev Opus alone (any severity)',recall_and_fb(E2,'claude/opus',anysev))
