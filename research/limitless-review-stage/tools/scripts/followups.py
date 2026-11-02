import sqlite3, json, collections, re
db=sqlite3.connect('file:'+__import__('os').path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
SINCE=1791460000000
rounds=db.execute("select run_id,source_run_id,pr_url,round,reviewed_sha,findings,created_at from review_rounds where kind='review' and created_at>? order by created_at",(SINCE,)).fetchall()
# runs belonging to each PR: source run + all round runs
pr_runs=collections.defaultdict(set)
for r in db.execute("select run_id,source_run_id,pr_url from review_rounds"):
    pr_runs[r[2]].update([r[0],r[1]])
def reviews(run):
    out=[]
    for name,content,ts in db.execute("select name,content,created_at from artifacts where run_id=? and kind='review'",(run,)):
        try: out.append((name,json.loads(content),ts))
        except: pass
    return out
models=collections.Counter(); nfind=[]; 
tot=0; matched_nonblock=0; matched_block=0; examples=[]
words=lambda s:set(w for w in re.findall(r'[a-z]{4,}',s.lower()))
for run_id,src,pr,rnd,sha,findings,ts in rounds:
    orch=[f for f in json.loads(findings) if f.get('severity') in ('blocker','major')]
    # factory reviews done before this orchestrator round
    fac=[]
    for rr in pr_runs[pr]:
        for name,rv,rts in reviews(rr):
            if rts<ts:
                fac.append(rv)
    for rv in fac:
        models[rv.get('model')]+=1
    for f in orch:
        tot+=1
        best=None
        for rv in fac:
            blk={(b.get('file'),b.get('line'),b.get('title')) for b in rv.get('blocking',[])}
            for g in rv.get('findings',[]):
                if g.get('file')!=f.get('file'): continue
                sim=len(words(g.get('title',''))&words(f.get('title','')))/max(1,len(words(f.get('title',''))))
                near=abs((g.get('line') or 0)-(f.get('line') or 0))<=10
                if near and sim>=0.3 or sim>=0.5:
                    isblk=(g.get('file'),g.get('line'),g.get('title')) in blk
                    best=(isblk,g,sim,rv.get("model"))
                    if not isblk: break
        if best:
            if best[0]: matched_block+=1
            else:
                matched_nonblock+=1
                examples.append((pr,rnd,f.get('severity'),f.get('title')[:90],best[1].get('severity'),best[1].get('title')[:90],round(best[2],2),best[3]))
print('orchestrator blocker/major findings:',tot)
print('similar to an earlier factory BLOCKING finding:',matched_block)
print('similar to an earlier factory NON-blocking finding:',matched_nonblock)
print('factory review models (reviews before orch rounds):',models.most_common())
for e in examples[:40]: print(e)
