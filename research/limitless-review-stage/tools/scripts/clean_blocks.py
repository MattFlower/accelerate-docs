import sqlite3,json,os,collections,re
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
cases={c['id']:c for c in json.load(open('~/code/limitless/.claude/worktrees/bun-test-performance-7b568d/evals/review/cases.json'))['cases']}
clean={k for k,c in cases.items() if not any(d.get('required') for d in c.get('defects',[]))}
rows=[];per=collections.Counter()
for ev,cid,trial,oj,dj in db.execute("select t.eval_run_id,t.case_id,t.trial,t.output_json,t.details_json from eval_trials t join eval_runs r on r.id=t.eval_run_id where r.role='review' and t.status='ok' and r.created_at>1791900000000"):
    if cid not in clean or not oj: continue
    o=json.loads(oj); sysn=json.loads(dj).get('system')
    for f in o.get('findings',[]):
        if f.get('severity') in('blocker','major'):
            rows.append({'eval':ev,'system':sysn,'case':cid,'trial':trial,'file':f.get('file'),'line':f.get('line'),'severity':f.get('severity'),'title':f.get('title'),'detail':f.get('detail'),'failure_scenario':f.get('failure_scenario')})
            per[cid]+=1
print(len(rows),'blocking findings on',len(per),'clean cases'); print(per.most_common())
json.dump(rows,open(os.path.expanduser('~/limitless-orch/review-research/phase0/clean_blocks.json'),'w'),indent=1)
