import sqlite3,json,os,collections,sys
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
cases={c['id']:c for c in json.load(open('~/code/limitless/.claude/worktrees/bun-test-performance-7b568d/evals/review/cases.json'))['cases']}
for ev in sys.argv[1:]:
  st=collections.defaultdict(collections.Counter)
  for cid,model,trial,oj,dj in db.execute("select case_id,model_id,trial,output_json,details_json from eval_trials where eval_run_id=? and status='ok'",(ev,)):
    c=cases.get(cid)
    if not c or not oj: continue
    try: o=json.loads(oj)
    except: continue
    s=json.loads(dj).get('system') or model
    allf=o.get('findings',[])
    st[s]['trials']+=1; st[s]['nf']+=len(allf)
    for f in allf: st[s]['sev_'+str(f.get('severity'))]+=1
    for g in (d for d in c.get('defects',[]) if d.get('required')):
      lo,hi=(g['lines']+[g['lines'][-1]])[:2] if g.get('lines') else (0,0)
      m=lambda fs:[f for f in fs if f.get('file')==g['file'] and lo-5<=(f.get('line') or 0)<=hi+5]
      st[s]['n']+=1
      if m([f for f in allf if f.get('severity') in('blocker','major')]): st[s]['blk']+=1
      if m(allf): st[s]['any']+=1
  for s,v in st.items():
    print(ev,s,dict(v), f"blocking {100*v['blk']/max(1,v['n']):.1f}% any-sev {100*v['any']/max(1,v['n']):.1f}%")
