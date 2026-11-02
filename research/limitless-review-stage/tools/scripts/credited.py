import sqlite3,json,os,collections
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
cases={c['id']:c for c in json.load(open('~/code/limitless/.claude/worktrees/bun-test-performance-7b568d/evals/review/cases.json'))['cases']}
EVALS=['eval-mv7igcxy1tl7bg203warej','eval-mv8gnw6f03ggcas1ml9ate','eval-mvi7bktt0cz50o81qkik8c']
out=[];cnt=collections.Counter()
for ev in EVALS:
  for cid,trial,oj,dj in db.execute("select case_id,trial,output_json,details_json from eval_trials where eval_run_id=? and status='ok'",(ev,)):
    c=cases.get(cid)
    if not c or not oj or c.get('split')!='dev': continue
    o=json.loads(oj); sysn=json.loads(dj).get('system')
    finds=[f for f in o.get('findings',[]) if f.get('severity') in('blocker','major')]
    used=set()
    for g in [d for d in c.get('defects',[]) if d.get('required')]:
      lo,hi=(g['lines']+[g['lines'][-1]])[:2] if g.get('lines') else (0,0)
      hits=[(i,f) for i,f in enumerate(finds) if i not in used and f.get('file')==g['file'] and lo-5<=(f.get('line') or 0)<=hi+5]
      if hits:
        i,f=hits[0]; used.add(i); cnt[sysn]+=1
        out.append({'eval':ev,'system':sysn,'case':cid,'trial':trial,'gold':g['summary'],'gold_file':g['file'],'gold_lines':g.get('lines'),'finding_line':f.get('line'),'finding_title':f.get('title'),'finding_detail':(f.get('detail') or '')[:600]})
print(dict(cnt), len(out))
json.dump(out,open('credited_candidates.json','w'),indent=1)
