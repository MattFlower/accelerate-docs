import sqlite3,json,os,collections
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
cases={c['id']:c for c in json.load(open('~/code/limitless/.claude/worktrees/bun-test-performance-7b568d/evals/review/cases.json'))['cases']}
EVALS=['eval-mv7igcxy1tl7bg203warej','eval-mv8gnw6f03ggcas1ml9ate','eval-mv92iu6p0y8ns1b0ifjg8t','eval-mvi7bktt0cz50o81qkik8c','eval-mvif9n84010bmzy1tk9std']
V=json.load(open('an/grader_verdicts.json'))
same=collections.Counter(); unc=collections.Counter()
for x in V:
  if x['verdict']=='SAME': same[(x['eval'],x['system'])]+=1
  if x['verdict']=='UNCLEAR': unc[(x['eval'],x['system'])]+=1
st=collections.defaultdict(collections.Counter)
for ev in EVALS:
  for cid,model,trial,oj,dj in db.execute("select case_id,model_id,trial,output_json,details_json from eval_trials where eval_run_id=? and status='ok'",(ev,)):
    c=cases.get(cid)
    if not c or not oj: continue
    try: o=json.loads(oj)
    except: continue
    finds=[f for f in o.get('findings',[]) if f.get('severity') in('blocker','major')]
    s=json.loads(dj).get('system')
    for g in (d for d in c.get('defects',[]) if d.get('required')):
      lo,hi=(g['lines']+[g['lines'][-1]])[:2] if g.get('lines') else (0,0)
      hit=[f for f in finds if f.get('file')==g['file'] and lo-5<=(f.get('line') or 0)<=hi+5]
      st[(ev,s)]['n']+=1
      if hit: st[(ev,s)]['c']+=1
for k,v in sorted(st.items()):
  n,c=v['n'],v['c']; s=same[k]; u=unc[k]
  print(k, n, c, f"{100*c/n:.1f}% -> {100*(c+s)/n:.1f}% (+unclear {100*(c+s+u)/n:.1f}%)")
