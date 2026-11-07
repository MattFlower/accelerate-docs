import json,random,collections,os,sqlite3,statistics as st
P=os.path.expanduser('~/limitless-orch/review-research/p12'); S10=os.path.expanduser('~/limitless-orch/review-research/p10')
cases={c['id']:c for c in json.load(open('evals/review/cases.json'))['cases']}
st0=json.load(open(f'{S10}/d-perdefect.json')); T=json.load(open(f'{P}/p12-perdefect.json'))
idx=lambda rows,pred:{(x['caseId'],x['gold'],x['trial']):x['caught'] for x in rows if pred(x)}
D=idx(st0,lambda x:x['system'].startswith('D')); E=idx(st0,lambda x:x['system']=='sol-6.1-medium-adversarial'); A=idx(T,lambda x:True)
keys=sorted(set(D)&set(A)); print('rows D',len(D),'U3',len(A),'shared',len(keys))
print('U3 %d/%d %.1f%%  D %d %.1f%%'%(sum(A[k] for k in keys),len(keys),100*sum(A[k] for k in keys)/len(keys),sum(D[k] for k in keys),100*sum(D[k] for k in keys)/len(keys)))
def boot(a,b,ks,n=10000):
    cs=sorted({k[0] for k in ks}); per={x:[a(k)-b(k) for k in ks if k[0]==x] for x in cs}; random.seed(20261107); ds=[]
    for _ in range(n):
        s=[v for _ in cs for v in per[random.choice(cs)]]; ds.append(sum(s)/len(s))
    ds.sort(); return round(100*sum(a(k)-b(k) for k in ks)/len(ks),1),round(100*ds[int(.05*n)],1),round(100*ds[int(.025*n)],1)
print('U3 - D (diff, 1s lo, 2s lo)',boot(lambda k:A[k],lambda k:D[k],keys))
ke=[k for k in keys if k in E]; print('context: U3 OR D per trial',sum(A[k] or D[k] for k in keys),'; E3 alone',sum(E[k] for k in ke),'/',len(ke))
cat=lambda k:cases[k[0]]['defects'][int(k[1][1:])-1]['category']
for c in sorted({cat(k) for k in keys}):
    ks=[k for k in keys if cat(k)==c]; print(' ',c,len(ks),'U3',sum(A[k] for k in ks),'D',sum(D[k] for k in ks))
print('gained',[k for k in keys if A[k] and not D[k]]); print('lost',[k for k in keys if D[k] and not A[k]])
c=json.load(open(f'{P}/p12-clean.json'))
print('clean trials',len(c),'nonok',sum(x['status']!='ok' for x in c),'blocks',sum(bool(x['blocking']) for x in c),'excl082',sum(bool(x['blocking']) for x in c if x['caseId']!='review-082'),'/',sum(x['caseId']!='review-082' for x in c))
for x in c:
    if x['blocking']: print('  ',x['caseId'],x['trial'],[t[:100] for t in x['titles']])
db=sqlite3.connect('file:'+os.path.expanduser('~/limitless-orch/lab/home/limitless.db')+'?mode=ro',uri=True); ev=open(f'{P}/eval-id').read().strip()
for name,q,s in (('U3',ev,'D3-adversarial-union3'),('D',"eval-mvw0y6v31sec2vc1agx2t1",'D-adversarial-union2')):
    rows=db.execute("select duration_ms,cost_equiv_usd,output_json,status from eval_trials where eval_run_id=? and json_extract(details_json,'$.system')=?",(q,s)).fetchall()
    ok=[r for r in rows if r[3]=='ok']; d=sorted(r[0] for r in ok); f=[len(json.loads(r[2]).get('findings',[])) for r in ok]
    print(name,len(rows),'ok',len(ok),'p50 %.0fs p90 %.0fs equiv p50 %.3f total %.2f findings/trial %.2f'%(st.median(d)/1000,d[int(.9*len(d))]/1000,st.median([r[1] or 0 for r in ok]),sum(r[1] or 0 for r in rows),sum(f)/len(f)))
