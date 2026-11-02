"""Compare judge matches with the audit truth on dev E1/E3/D. Truth per (key,gold summary): caught iff an audited
blocking finding was judged SAME (credited or missed audit); UNCLEAR excluded; unaudited misses = not caught."""
import json,os,sys,collections
R=os.path.expanduser('~/limitless-orch/review-research/')
items={json.loads(l)['key']:json.loads(l) for l in open(R+'phase0/val_items.jsonl')}
blind={v['blind_id']:k for k,v in items.items()}
truth={}
for k,it in items.items():
    for g in it['gold']: truth[(k,g['summary'])]=False
for v in json.load(open(R+'credited_verdicts.json')):
    k=f"{v['eval']}|{v['system']}|{v['case']}|{v['trial']}"
    if (k,v['gold']) in truth: truth[(k,v['gold'])]= {'SAME':True,'DIFFERENT':False}.get(v['verdict'],None)
for v in json.load(open(R+'grader_verdicts.json')):
    k=f"{v['eval']}|{v['system']}|{v['case']}|{v['trial']}"
    if (k,v['gold']) in truth and v['verdict']!='DIFFERENT':
        truth[(k,v['gold'])]= True if v['verdict']=='SAME' else None
def load(paths):
    out={}
    for p in paths:
        if not os.path.exists(p): continue
        for l in open(p):
            try: d=json.loads(l)
            except: continue
            k=blind.get(d['key'],d['key'])
            if 'matches' in d: out[k]=d['matches']
    return out
def judged(matches,key,blocking=True):
    it=items[key]; res={}
    fs={f['id']:f for f in it['findings']}
    for m in matches:
        g=next((x for x in it['gold'] if x['id']==m.get('gold')),None)
        if not g: continue
        f=fs.get(m.get('finding'))
        res[g['summary']]=bool(f) and (not blocking or f['severity'] in('blocker','major'))
    return res
judges={'terra':load([R+'phase0/val_terra.jsonl']),'claude':load([R+f'phase0/val_claude_out_{i}.jsonl' for i in range(3)])}
for name,J in judges.items():
    c=collections.Counter()
    for (k,gs),t in truth.items():
        if t is None or k not in J: continue
        j=judged(J[k],k).get(gs,False)
        c[(t,j)]+=1
    n=sum(c.values())
    if n: print(name,'n',n,'agree',round((c[(True,True)]+c[(False,False)])/n,3),'truth+judge-',c[(True,False)],'truth-judge+',c[(False,True)],'both+',c[(True,True)])
# judge-judge agreement
if all(judges.values()):
    c=collections.Counter()
    for k in set(judges['terra'])&set(judges['claude']):
        a=judged(judges['terra'][k],k); b=judged(judges['claude'][k],k)
        for gs in a: c[(a[gs],b.get(gs,False))]+=1
    n=sum(c.values()); print('terra vs claude n',n,'agree',round((c[(True,True)]+c[(False,False)])/n,3),dict(c))
