import sqlite3,json,collections,os,datetime
db=sqlite3.connect('file:'+os.path.expanduser('~/.limitless/limitless.db')+'?mode=ro',uri=True)
# all PRs with a factory delivery since SINCE: source runs with a pr; orchestrator round1 per pr
SINCE=1791460000000
r1={}
for run_id,src,pr,rnd,f,ts in db.execute("select run_id,source_run_id,pr_url,round,findings,created_at from review_rounds where kind='review' and created_at>?",(SINCE,)):
    n=sum(1 for x in json.loads(f) if x.get('severity') in('blocker','major'))
    r1.setdefault(pr,{})[rnd]=(src,n,ts)
# model of last factory review in source run
stat=collections.defaultdict(lambda:[0,0,0])
for pr,rs in r1.items():
    if 1 not in rs: continue
    src,n,ts=rs[1]
    row=db.execute("select content from artifacts where run_id=? and kind='review' order by created_at desc limit 1",(src,)).fetchone()
    m=json.loads(row[0]).get('model') if row else None
    s=stat[m]; s[0]+=1; s[1]+=n; s[2]+=sum(v[1] for v in rs.values())
for m,(p,n,a) in stat.items(): print(m,'PRs w/ orch round1',p,'round1 B/M per PR',round(n/p,2),'all-rounds B/M per PR',round(a/p,2))
# how many factory PRs (source runs that delivered a PR) got NO orchestrator round?
tot=db.execute("select count(*) from runs where created_at>? and pr_url is not null",(SINCE,)).fetchone() if 'pr_url' in [c[1] for c in db.execute('pragma table_info(runs)')] else None
print('runs with pr since:',tot, 'PRs with orch rounds:',len(r1))
