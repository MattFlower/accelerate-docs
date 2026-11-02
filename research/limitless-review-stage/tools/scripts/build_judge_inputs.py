"""Build one judge item per stored review trial: required gold defects + all reviewer findings (blind to system)."""
import sqlite3,json,os,sys,hashlib
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
cases={c['id']:c for c in json.load(open('~/code/limitless/.claude/worktrees/bun-test-performance-7b568d/evals/review/cases.json'))['cases']}
evals=sys.argv[2].split(',')
out=open(sys.argv[1],'w'); n=0
for ev in evals:
  for cid,model,trial,oj,dj in db.execute("select case_id,model_id,trial,output_json,details_json from eval_trials where eval_run_id=? and status='ok'",(ev,)):
    c=cases.get(cid)
    if not c or not oj: continue
    gold=[{'id':f'G{i+1}','file':d['file'],'lines':d.get('lines'),'summary':d['summary'],'category':d.get('category')} for i,d in enumerate(x for x in c.get('defects',[]) if x.get('required'))]
    if not gold: continue
    o=json.loads(oj); sysn=json.loads(dj).get('system') or model
    finds=[{'id':f'F{i+1}','severity':f.get('severity'),'file':f.get('file'),'line':f.get('line'),'title':f.get('title'),'detail':(f.get('detail') or '')[:700],'failure_scenario':(f.get('failure_scenario') or '')[:300]} for i,f in enumerate(o.get('findings',[]))]
    key=f'{ev}|{sysn}|{cid}|{trial}'
    item={'key':key,'eval':ev,'system':sysn,'case':cid,'trial':trial,'gold':gold,'findings':finds}
    item['blind_id']=hashlib.sha1(key.encode()).hexdigest()[:10]
    out.write(json.dumps(item)+'\n'); n+=1
print(n,'items')
