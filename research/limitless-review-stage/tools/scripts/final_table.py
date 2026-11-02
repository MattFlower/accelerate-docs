"""Final judged recall: two-judge consensus, with code-reading tiebreak verdicts overriding on contested items."""
import json,os,collections
R=os.path.expanduser('~/limitless-orch/review-research/')
exec(open(R+'scripts/replays.py').read().split("std=lambda")[0])
std=lambda f:f.get('severity') in BLK
priv={o['tid']:o for o in json.load(open(R+'phase0/tiebreak_private.json'))}
TB={}
for f in ['a','b']:
    for v in json.load(open(R+f'phase0/tiebreak_{f}_out.json')): TB[(priv[v['tid']]['_key'],priv[v['tid']]['_gid'])]=(v['verdict']=='SAME',priv[v['tid']])
# judge accuracy vs code on tiebreak items, per arm
acc=collections.defaultdict(collections.Counter)
for (k,gid),(same,o) in TB.items():
    arm=items[k]['system']; jc=bool(o['_judges']['claude']); jt=bool(o['_judges']['terra'])
    acc[arm]['n']+=1; acc[arm]['claude_ok']+=(jc==same); acc[arm]['terra_ok']+=(jt==same); acc[arm]['both_ok']+=((jc and jt)==same); acc[arm]['code_same']+=same
print('judge vs code-reading on contested items, per arm:')
for a,c in acc.items(): print(f"  {a:34} n={c['n']:2} code SAME {c['code_same']:2}  claude ok {c['claude_ok']}  terra ok {c['terra_ok']}  both-rule ok {c['both_ok']}")
def caught(k,gid,fs):
    if (k,gid) in TB: return TB[(k,gid)][0]
    return caught_by(k,gid,fs,std)
rows=[('dev','eval-mv7igcxy1tl7bg203warej','codex/sol-6.1@medium','production sol@medium (E1)'),
      ('dev','eval-mvhaoiqd04069nv0pjqdv4','sol-6.1-medium-standard-setup','production + setup'),
      ('dev','eval-mv7igcxy1tl7bg203warej','codex/sol-6.1@high','sol@high (same run as E1)'),
      ('dev','eval-mv8gnw6f03ggcas1ml9ate','sol-6.1-medium-adversarial','adversarial prompt (E3)'),
      ('dev','eval-mvi7bktt0cz50o81qkik8c','D-adversarial-union2','union of 2 adversarial (D)'),
      ('dev','eval-mvicu2zq10nvz5i1tilfbr','F-adversarial-checklist','checklist F (own cohort)'),
      ('dev','eval-mvie4edg0rt3i0m0xflslq','codex/sol-6.1@medium','production on F added cases'),
      ('dev','eval-mvia5vc9053f9yo0mx5pd8','E','trace finder (E)'),
      ('dev','eval-mvhaoiqd04069nv0pjqdv4','sol-6.1-medium-probe-setup','probe + setup'),
      ('dev','eval-mv7rznhb0nugf7t09om5i6','claude/opus','opus'),
      ('dev','eval-mvlhu0571ydkrqq15dbjsa','claude/opus@high','opus@high'),
      ('heldout','eval-mv92iu6p0y8ns1b0ifjg8t','sol-6.1-medium-standard','production (held-out)'),
      ('heldout','eval-mv92iu6p0y8ns1b0ifjg8t','sol-6.1-medium-adversarial','adversarial (held-out)'),
      ('heldout','eval-mvif9n84010bmzy1tk9std','D-adversarial-union2','D (held-out)')]
res={}
for split,ev,sysn,label in rows:
    n=c=0; percase={}
    for cid,trial,o,s in trials(ev):
        if s!=sysn: continue
        k=f'{ev}|{s}|{cid}|{trial}'
        if k not in items: continue
        for g in items[k]['gold']:
            n+=1; x=caught(k,g['id'],o.get('findings',[])); c+=x; percase[(cid,trial,g['summary'])]=x
    res[label]=percase
    print(f"{split:8} {label:34} {c:3}/{n:3} = {100*c/max(1,n):5.1f}%")
json.dump({k:{'|'.join(map(str,kk)):v for kk,v in d.items()} for k,d in res.items()},open(R+'phase0/final_percase.json','w'))
# F cohort comparison
F=res['checklist F (own cohort)']; P1=res['production sol@medium (E1)']; P2=res['production on F added cases']; E3=res['adversarial prompt (E3)']
fc={k[0] for k in F}
pc=[v for k,v in P1.items() if k[0] in fc]+list(P2.values())
print('F cohort: F',sum(F.values()),'/',len(F),' production',sum(pc),'/',len(pc),' E3 (19 orig)',sum(v for k,v in E3.items() if k[0] in fc),'/',sum(1 for k in E3 if k[0] in fc))
