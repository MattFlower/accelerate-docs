import sqlite3,json,os,re,collections,sys
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
cases={c['id']:c for c in json.load(open('~/code/limitless/.claude/worktrees/bun-test-performance-7b568d/evals/review/cases.json'))['cases']}
EVALS=sys.argv[1:] or ['eval-mv7igcxy1tl7bg203warej','eval-mv8gnw6f03ggcas1ml9ate','eval-mv92iu6p0y8ns1b0ifjg8t','eval-mvi7bktt0cz50o81qkik8c','eval-mvif9n84010bmzy1tk9std']
W=lambda s:set(re.findall(r'[a-z]{4,}',(s or '').lower()))
def blk(f): return f.get('severity') in('blocker','major')
out=[];stats=collections.Counter()
for ev in EVALS:
  for cid,model,trial,oj,dj in db.execute("select case_id,model_id,trial,output_json,details_json from eval_trials where eval_run_id=? and status='ok'",(ev,)):
    c=cases.get(cid)
    if not c or not oj: continue
    try: o=json.loads(oj)
    except: continue
    finds=[f for f in o.get('findings',[]) if blk(f)]
    sysname=json.loads(dj).get('system')
    for i,g in enumerate(d for d in c.get('defects',[]) if d.get('required')):
      lo,hi=(g['lines']+[g['lines'][-1]])[:2] if g.get('lines') else (0,0)
      hit=[f for f in finds if f.get('file')==g['file'] and lo-5<=(f.get('line') or 0)<=hi+5]
      stats['defect-trials']+=1
      if hit: stats['caught']+=1; continue
      cands=[]
      for f in finds:
        ov=len(W(g['summary'])&(W(f.get('title'))|W(f.get('detail'))))/max(1,len(W(g['summary'])))
        same=f.get('file')==g['file']
        if same or ov>=0.5: cands.append((round(ov,2),same,f.get('file'),f.get('line'),f.get('title')))
      if cands:
        stats['missed-with-candidate']+=1
        out.append({'eval':ev,'system':sysname,'case':cid,'trial':trial,'gold':g['summary'],'gold_file':g['file'],'gold_lines':g.get('lines'),'cands':sorted(cands,reverse=True)[:3]})
      else: stats['missed-no-candidate']+=1
print(dict(stats))
json.dump(out,open('grader_candidates.json','w'),indent=1)
sameF=sum(1 for x in out if any(c[1] for c in x['cands']))
print('candidates total',len(out),'with same-file finding',sameF)
