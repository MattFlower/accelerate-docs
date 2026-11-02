"""Run the Codex judge over judge items; resumable cache. Usage: judge_codex.py items.jsonl out.jsonl model effort [conc]"""
import json,sys,os,subprocess,tempfile,concurrent.futures,threading
sys.path.insert(0,os.path.dirname(__file__)); from judge_prompt import prompt,parse
items_p,out_p,model,effort=sys.argv[1:5]; conc=int(sys.argv[5]) if len(sys.argv)>5 else 4
done=set()
if os.path.exists(out_p):
    for l in open(out_p):
        try: done.add(json.loads(l)['key'])
        except: pass
items=[json.loads(l) for l in open(items_p)]
todo=[i for i in items if i['key'] not in done]
lock=threading.Lock(); wd=tempfile.mkdtemp(prefix='judge-')
def run(item):
    if not item['findings']:
        return {'key':item['key'],'matches':[{'gold':g['id'],'finding':None,'confidence':1,'reason':'no findings'} for g in item['gold']]}
    of=os.path.join(wd,item['blind_id']+'.out')
    for attempt in range(2):
        try:
            subprocess.run(['codex','exec','-m',model,'-c',f'model_reasoning_effort={effort}','-s','read-only','--skip-git-repo-check','--ephemeral','-C',wd,'-o',of,'-'],input=prompt(item),text=True,capture_output=True,timeout=600)
            return {'key':item['key'],'matches':parse(open(of).read())}
        except Exception as e:
            err=str(e)
    return {'key':item['key'],'error':err}
with concurrent.futures.ThreadPoolExecutor(conc) as ex:
    for r in ex.map(run,todo):
        with lock:
            open(out_p,'a').write(json.dumps(r)+'\n')
print('done',len(todo))
