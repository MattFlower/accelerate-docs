"""Phase 1.0 pooling from stored trials: findings on REAL cases that neither judge matched to any gold defect.
Out: phase1/pool_stored.json {case: [finding + provenance]}; counts on stdout."""
import json,os,collections
R=os.path.expanduser('~/limitless-orch/review-research/')
exec(open(R+'scripts/rescore.py').read().split("agg=collections")[0])
pool=collections.defaultdict(list); n=collections.Counter()
for k,it in items.items():
    matched=set()
    for J in (CL,TE):
        for m in J.get(k,[]) or []:
            if m.get('finding'): matched.add(m['finding'])
    for f in it['findings']:
        sev=f.get('severity'); n[('all',sev)]+=1
        if f['id'] in matched: continue
        n[('unmatched',sev)]+=1
        pool[it['case']].append({**f,'_eval':it['eval'],'_system':it['system'],'_trial':it['trial']})
json.dump(pool,open(R+'phase1/pool_stored.json','w'),indent=1)
print(sorted(n.items())); print('cases with pooled findings',len(pool))
blk={c:[f for f in fs if f['severity'] in BLK] for c,fs in pool.items()}
print('unmatched blocking',sum(map(len,blk.values())),'cases',sum(1 for v in blk.values() if v))
