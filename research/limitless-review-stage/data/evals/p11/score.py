import json,random,sys,collections,os,sqlite3,statistics as st
P=os.path.expanduser('~/limitless-orch/review-research/p11'); S10=os.path.expanduser('~/limitless-orch/review-research/p10')
cases={c['id']:c for c in json.load(open('evals/review/cases.json'))['cases']}
st0=json.load(open(f'{S10}/d-perdefect.json')); T=json.load(open(f'{P}/p11-perdefect.json'))
def idx(rows,pred): return {(x['caseId'],x['gold'],x['trial']):x['caught'] for x in rows if pred(x)}
D=idx(st0,lambda x:x['system'].startswith('D')); E=idx(st0,lambda x:x['system']=='sol-6.1-medium-adversarial'); A=idx(T,lambda x:True)
print('rows D',len(D),'E3',len(E),'T',len(A))
keys=sorted(set(D)&set(E)&set(A)); print('shared',len(keys))
defs=sorted({k[:2] for k in keys})
print('per-trial  T %d/%d %.1f  E3 %.1f  D %.1f'%(sum(A[k] for k in keys),len(keys),100*sum(A[k] for k in keys)/len(keys),100*sum(E[k] for k in keys)/len(keys),100*sum(D[k] for k in keys)/len(keys)))
def orr(M,d): return any(M.get((d[0],d[1],t),False) for t in (0,1))
print('OR-of-2  T %d/%d  E3 %d/%d  mixed(E3t0|Tt1 avg) '%(sum(orr(A,d) for d in defs),len(defs),sum(orr(E,d) for d in defs),len(defs)))
mix=sum((E.get((d[0],d[1],0),False) or A.get((d[0],d[1],1),False))+(E.get((d[0],d[1],1),False) or A.get((d[0],d[1],0),False)) for d in defs)/2
print('mixed adversarial+thorough pair %.1f/%d'%(mix,len(defs)))
print('D OR T per-trial %d/%d %.1f'%(sum(D[k] or A[k] for k in keys),len(keys),100*sum(D[k] or A[k] for k in keys)/len(keys)))
print('D 3-sample OR (D t | T other) same; D OR-of-2-trials %d/%d'%(sum(orr(D,d) for d in defs),len(defs)))
def boot(a,b,ks,n=10000):
    cs=sorted({k[0] for k in ks}); per={x:[a(k)-b(k) for k in ks if k[0]==x] for x in cs}; random.seed(20261106); ds=[]
    for _ in range(n):
        s=[v for _ in cs for v in per[random.choice(cs)]]; ds.append(sum(s)/len(s))
    ds.sort(); return round(100*sum(a(k)-b(k) for k in ks)/len(ks),1),round(100*ds[int(.05*n)],1),round(100*ds[int(.025*n)],1)
print('A T-E3 per trial (diff,1s lo,2s lo)',boot(lambda k:A[k],lambda k:E[k],keys))
print('B OR T - OR E3',boot(lambda d:orr(A,d),lambda d:orr(E,d),defs))
print('OR T - D mean per-trial', 100*sum(orr(A,d) for d in defs)/len(defs)-100*sum(D[k] for k in keys)/len(keys))
print('D OR T - D',boot(lambda k:D[k] or A[k],lambda k:D[k],keys))
cat=lambda k:cases[k[0]]['defects'][int(k[1][1:])-1]['category']
for c in sorted({cat(k) for k in keys}):
    ks=[k for k in keys if cat(k)==c]; print(' ',c,len(ks),'T',sum(A[k] for k in ks),'E3',sum(E[k] for k in ks),'D',sum(D[k] for k in ks))
g=[d for d in defs if orr(A,d) and not orr(E,d)]; l=[d for d in defs if orr(E,d) and not orr(A,d)]; print('OR gained',g,'lost',l)
c=json.load(open(f'{P}/p11-clean.json')); pair=collections.defaultdict(bool)
for x in c: pair[x['caseId']]|=bool(x['blocking'])
print('clean trials',len(c),'nonok',sum(x['status']!='ok' for x in c),'trial blocks',sum(bool(x['blocking']) for x in c),'excl082',sum(bool(x['blocking']) for x in c if x['caseId']!='review-082'),'pair OR excl082',sum(v for k,v in pair.items() if k!='review-082'),'/15')
for x in c:
    if x['blocking']: print('  ',x['caseId'],x['trial'],[t[:90] for t in x['titles']])
db=sqlite3.connect('file:'+os.path.expanduser('~/limitless-orch/lab/home/limitless.db')+'?mode=ro',uri=True)
ev=open(f'{P}/eval-id').read().strip()
for name,q in (('T',ev),('E3','eval-mvw0y6v31sec2vc1agx2t1')):
    rows=db.execute("select duration_ms,cost_equiv_usd,tokens_out,output_json from eval_trials where eval_run_id=? and status='ok' and json_extract(details_json,'$.system') in ('sol-6.1-medium-thorough','sol-6.1-medium-adversarial')",(q,)).fetchall()
    d=sorted(r[0] for r in rows); fnd=[len(json.loads(r[3]).get('findings',[])) for r in rows]
    print(name,len(rows),'p50 %.0fs p90 %.0fs equiv p50 %.3f tot %.2f tokout %d findings mean %.2f'%(st.median(d)/1000,d[int(.9*len(d))]/1000,st.median(r[1] or 0 for r in rows) if False else st.median([r[1] or 0 for r in rows]),sum(r[1] or 0 for r in rows),st.median([r[2] or 0 for r in rows]),sum(fnd)/len(fnd)))
print('T non-ok',db.execute("select status,count(*) from eval_trials where eval_run_id=? group by 1",(ev,)).fetchall())
print('--- post-hoc controls (not pre-registered)')
full=[d for d in defs if all((d[0],d[1],t) in E for t in (0,1))]; print('defects with both E3 trials',len(full),'dropped',[d for d in defs if d not in full])
print('B on complete defects: OR T %d OR E3 %d of %d'%(sum(orr(A,d) for d in full),sum(orr(E,d) for d in full),len(full)),boot(lambda d:orr(A,d),lambda d:orr(E,d),full))
print('3 samples, D+T %d vs D+E3 %d of %d (D %d)'%(sum(D[k] or A[k] for k in keys),sum(D[k] or E[k] for k in keys),len(keys),sum(D[k] for k in keys)),'diff',boot(lambda k:D[k] or A[k],lambda k:D[k] or E[k],keys))
print('D+E3 - D',boot(lambda k:D[k] or E[k],lambda k:D[k],keys))
