import json,collections,subprocess,sys,glob,os
S=sys.argv[1]
r=[x for x in json.load(open(f'{S}/d-perdefect.json')) if x['system'].startswith('D')]
cases={c['id']:c for c in json.load(open('evals/review/cases.json'))['cases']}
repo=glob.glob(os.path.expanduser('~/limitless-orch/lab/home/repos/**/*limitless*'),recursive=False)
import pathlib
cand=[p for p in pathlib.Path(os.path.expanduser('~/limitless-orch/lab/home/repos')).rglob('HEAD')]
g=os.path.expanduser('~/limitless-orch/lab/home/repos/MattFlower__limitless.git'); print(g)
def files(c):
    o=subprocess.run(['git','-C',g,'diff','--name-only',c['base'],c['head']],capture_output=True,text=True)
    return set(o.stdout.split()) if o.returncode==0 else None
rows=collections.defaultdict(list)
for x in r: rows[(x['caseId'],x['gold'])].append(x)
agg=collections.Counter(); out=[]
for (cid,gold),t in rows.items():
    c=cases[cid]; d=c['defects'][int(gold[1:])-1]; fs=files(c)
    inside=None if fs is None else d['file'] in fs
    n=sum(x['caught'] for x in t)
    agg[('in-diff' if inside else 'OUT' if inside is False else '?', n)]+=1
    if n==0: out.append((cid,gold,'in' if inside else 'OUT',d['category'],d['file'],d['summary'][:110]))
print(sorted(agg.items(),key=str)); print(len(rows),'defects')
json.dump(out,open(f'{S}/missed.json','w'),indent=0)
for o in out: print(*o,sep=' | ')
