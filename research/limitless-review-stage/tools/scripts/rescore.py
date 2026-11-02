"""Rescore stored review trials: ±5 grader vs Claude judge vs Terra judge vs consensus. Per (eval, system, split)."""
import json,os,collections,sys
R=os.path.expanduser('~/limitless-orch/review-research/')
cases={c['id']:c for c in json.load(open('~/code/limitless/.claude/worktrees/bun-test-performance-7b568d/evals/review/cases.json'))['cases']}
items={}
for f in ['phase0/val_items.jsonl','phase0/rest_items.jsonl']:
    for l in open(R+f): d=json.loads(l); items[d['key']]=d
blind={v['blind_id']:k for k,v in items.items()}
def load(paths):
    out={}
    for p in paths:
        if not os.path.exists(R+p): continue
        for l in open(R+p):
            try: d=json.loads(l)
            except: continue
            if 'matches' in d: out[blind.get(d['key'],d['key'])]=d['matches']
    return out
CL=load([f'phase0/val_claude_out_{i}.jsonl' for i in range(3)]+[f'phase0/rest_claude_out_{i}.jsonl' for i in range(6)])
TE=load(['phase0/val_terra.jsonl','phase0/rest_terra.jsonl'])
BLK=('blocker','major')
def jm(J,k):
    """gold id -> (matched finding severity or None, confidence)"""
    it=items[k]; fs={f['id']:f for f in it['findings']}; out={}
    if not it['findings']: return {g['id']:(None,1) for g in it['gold']}
    if k not in J: return None
    for m in J[k]:
        f=fs.get(m.get('finding')); out[m.get('gold')]=(f['severity'] if f else None, m.get('confidence') or 0)
    return out
def grader(it):
    used=set(); res={}
    finds=[f for f in it['findings'] if f['severity'] in BLK]
    for g in it['gold']:
        lo,hi=(g['lines']+[g['lines'][-1]])[:2] if g.get('lines') else (0,0)
        h=[f for f in finds if f['id'] not in used and f['file']==g['file'] and lo-5<=(f['line'] or 0)<=hi+5]
        res[g['id']]=bool(h)
        if h: used.add(h[0]['id'])
    return res
agg=collections.defaultdict(lambda:collections.Counter()); dis=[]
for k,it in items.items():
    split=cases[it['case']].get('split') or 'none'
    a=agg[(it['eval'],it['system'],split)]
    g5=grader(it); c=jm(CL,k); t=jm(TE,k)
    for g in it['gold']:
        gid=g['id']; a['n']+=1; a['grader']+=g5[gid]
        cb=c and c.get(gid,(None,0))[0] in BLK; tb=t and t.get(gid,(None,0))[0] in BLK
        cany=c and c.get(gid,(None,0))[0] is not None
        if c is not None: a['n_c']+=1; a['claude']+=bool(cb); a['claude_any']+=bool(cany)
        if t is not None: a['n_t']+=1; a['terra']+=bool(tb)
        if c is not None and t is not None:
            a['n_ct']+=1; a['both']+=bool(cb and tb); a['either']+=bool(cb or tb)
            if bool(cb)!=bool(tb): dis.append((k,gid,bool(cb),bool(tb)))
pct=lambda x,n: f'{100*x/n:5.1f}' if n else '  -  '
print(f"{'eval':28} {'system':34} {'split':7} {'n':>4} grader claude(any) terra  both either [n_ct]")
for (e,s,sp),a in sorted(agg.items()):
    print(f"{e[:28]:28} {str(s)[:34]:34} {sp:7} {a['n']:4} {pct(a['grader'],a['n'])} {pct(a['claude'],a['n_c'])}({pct(a['claude_any'],a['n_c'])}) {pct(a['terra'],a['n_t'])} {pct(a['both'],a['n_ct'])} {pct(a['either'],a['n_ct'])} [{a['n_ct']}]")
print('judge disagreements (blocking):',len(dis))
json.dump(dis,open(R+'phase0/judge_disagreements.json','w'))
