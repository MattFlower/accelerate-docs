import sqlite3,json,os,collections,sys
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
cases={c['id']:c for c in json.load(open('~/code/limitless/.claude/worktrees/bun-test-performance-7b568d/evals/review/cases.json'))['cases']}
def hits(ev):
  H={}  # (system,case,trial,defidx)->(blk,any)
  for cid,model,trial,oj,dj in db.execute("select case_id,model_id,trial,output_json,details_json from eval_trials where eval_run_id=? and status='ok'",(ev,)):
    c=cases.get(cid)
    if not c or not oj: continue
    try:o=json.loads(oj)
    except: continue
    s=json.loads(dj).get('system') or model; allf=o.get('findings',[])
    for i,g in enumerate(d for d in c.get('defects',[]) if d.get('required')):
      lo,hi=(g['lines']+[g['lines'][-1]])[:2] if g.get('lines') else (0,0)
      m=lambda fs:any(f.get('file')==g['file'] and lo-5<=(f.get('line') or 0)<=hi+5 for f in fs)
      H[(s,cid,trial,i)]=(m([f for f in allf if f.get('severity') in('blocker','major')]),m(allf))
  return H
def rep(H,a,b,amode,bmode):
  keys={k[1:] for k in H if k[0]==a}&{k[1:] for k in H if k[0]==b}
  ua=sum(H[(a,)+k][amode] for k in keys); ub=sum(H[(b,)+k][bmode] for k in keys)
  u=sum(H[(a,)+k][amode] or H[(b,)+k][bmode] for k in keys)
  # defect-level: caught in any trial
  dk=collections.defaultdict(lambda:[0,0])
  for k in keys:
    d=(k[0],k[2]); dk[d][0]|=H[(a,)+k][amode]; dk[d][1]|=H[(b,)+k][bmode]
  print(f"{a}[{'blk' if amode==0 else 'any'}] {100*ua/len(keys):.1f}  {b}[{'blk' if bmode==0 else 'any'}] {100*ub/len(keys):.1f}  union-per-trial {100*u/len(keys):.1f}  n={len(keys)} | defects caught ever: A {sum(v[0] for v in dk.values())} B {sum(v[1] for v in dk.values())} union {sum(v[0] or v[1] for v in dk.values())} of {len(dk)}; only-B {sum((not v[0]) and v[1] for v in dk.values())}")
H=hits('eval-mv7rznhb0nugf7t09om5i6')
rep(H,'codex/sol-6.1@medium','claude/opus',0,0)
rep(H,'codex/sol-6.1@medium','claude/opus',0,1)
H2=hits('eval-mv7igcxy1tl7bg203warej')
rep(H2,'codex/sol-6.1@medium','codex/sol-6.1@high',0,0)
