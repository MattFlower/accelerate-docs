import json,random,sys,collections
S,new=sys.argv[1],sys.argv[2]
cases={c['id']:c for c in json.load(open('evals/review/cases.json'))['cases']}
stored=json.load(open(f'{S}/d-perdefect.json')); arm=json.load(open(new))
def idx(rows,pred): return {(x['caseId'],x['gold'],x['trial']):x['caught'] for x in rows if pred(x)}
D=idx(stored,lambda x:x['system'].startswith('D')); E=idx(stored,lambda x:x['system']=='sol-6.1-medium-adversarial')
B=idx(arm,lambda x:True); keys=sorted(D)
missing=[k for k in keys if k not in B]; print('trials',len(keys),'missing in arm',len(missing))
sec=lambda k:cases[k[0]]['defects'][int(k[1][1:])-1]['category']=='security'
def show(n,f,ks=keys): print(f'{n:32}{sum(f(k) for k in ks):4}/{len(ks)} {100*sum(f(k) for k in ks)/len(ks):.1f}%')
dv=lambda k:D[k]; bv=lambda k:B.get(k,False); ev=lambda k:E.get(k,False)
u=lambda k:dv(k) or bv(k); c=lambda k:ev(k) or bv(k)
for lab,ks in (('ALL',keys),('SECURITY',[k for k in keys if sec(k)]),('NON-SEC',[k for k in keys if not sec(k)])):
    print('--',lab); show('D union (stored)',dv,ks); show('boundary alone',bv,ks); show('E3 alone',ev,ks); show('D OR boundary',u,ks); show('E3 OR boundary (cost-neutral)',c,ks)
def boot(a,b,n=10000):
    cs=sorted({k[0] for k in keys}); per={x:[(a(k)-b(k)) for k in keys if k[0]==x] for x in cs}; random.seed(20261106); ds=[]
    for _ in range(n):
        s=[v for _ in cs for v in per[random.choice(cs)]]; ds.append(sum(s)/len(s))
    ds.sort(); return sum(a(k)-b(k) for k in keys)/len(keys),ds[int(.05*n)],ds[int(.025*n)]
print('D OR boundary - D  (diff, one-sided lower 95, two-sided lower 95)',boot(u,dv)); print('E3 OR boundary - D',boot(c,dv))
gain=[k for k in keys if bv(k) and not dv(k)]; print('gained',len(gain))
print(collections.Counter(k[0]+' '+k[1] for k in gain).most_common(40))
