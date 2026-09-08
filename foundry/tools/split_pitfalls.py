"""Stage 6b - Extract `## Pitfalls` into routed reference pages (profile 1.4.0).

Reads the blocks parsed by split_blocks.py and the index->group map in
split_groups.py, writes one `references/pitfalls-*.md` page per group, and
rewrites the `## Pitfalls` section of SKILL.md into one routing stub per entry.

Run from the sage-waggle skill directory (the one holding SKILL.md and
references/); see Appendix A of the paper.
"""

import argparse,io,json,os,re,sys

_here=os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path: sys.path.insert(0,_here)
from split_groups import GROUPS

ap=argparse.ArgumentParser()
ap.add_argument('--blocks',required=True,help='blocks.json from split_blocks.py')
ap.add_argument('--skill',default='SKILL.md',help='SKILL.md to rewrite in place')
ap.add_argument('--refs',default='references',help='directory for the new pages')
args=ap.parse_args()

recs=json.load(open(args.blocks,encoding='utf-8'))
STUB_MAX=150
def key_span(text):
    spans=re.findall(r'`([^`\n]{4,80})`',text)
    if not spans: return None
    cmdish=[s for s in spans if re.search(r'[ /._-]',s) and not s.startswith('http')]
    return max(cmdish or spans,key=len)
def stub_for(r):
    m=re.match(r'- \*\*(.+?)\*\*\s*:?\s*(.*)',r['first'],re.S)
    label,body=(m.group(1),m.group(2)) if m else (None,r['first'][2:])
    body=re.sub(r'\s+',' ',body).strip()
    cut=body[:STUB_MAX]
    dot=max(cut.rfind('. '),cut.rfind('? '),cut.rfind('! '))
    if dot>60: body=cut[:dot+1]
    elif len(body)>STUB_MAX: body=cut[:cut.rfind(' ')].rstrip(' ,;—-')+' …'
    if body.count('`')%2: body=body.rsplit('`',1)[0].rstrip()+' …'
    ks=key_span(r['text'])
    if ks and ks not in body: body=body.rstrip('… ').rstrip()+f" → `{ks}`"
    return label,body
stub=[]
for slug,desc,idxs in GROUPS:
    page=[f"# {desc[0].upper()+desc[1:]}","",
          "Extracted from `sage-waggle/SKILL.md` `## Pitfalls`. Each entry is a field-observed",
          "failure and its fix. Routed from the Pitfalls index in SKILL.md.",""]
    for i in idxs: page += [recs[i]['text'],""]
    io.open(os.path.join(args.refs,f'{slug}.md'),'w',encoding='utf-8').write('\n'.join(page).rstrip()+'\n')
    stub.append(f"\n### {desc[0].upper()+desc[1:]}\n")
    stub.append(f"→ `references/{slug}.md`\n")
    for i in idxs:
        l,b=stub_for(recs[i]); stub.append(f"- **{l}** — {b}" if l else f"- {b}")
hdr=["## Pitfalls","",
 "Field-observed failures, grouped. Each line is the symptom plus its key command; the",
 "full cause, fix and evidence are on the linked page — **open the page before acting**,",
 "the one-liners are for routing only.",""]
sec='\n'.join(hdr+stub).rstrip()+'\n'
lines=io.open(args.skill,encoding='utf-8').read().split('\n')
a=lines.index('## Pitfalls'); b=next(i for i,l in enumerate(lines) if l.startswith('## ECR Readiness'))
s='\n'.join(lines[:a]+sec.rstrip('\n').split('\n')+['']+lines[b:])
io.open(args.skill,'w',encoding='utf-8').write(s)
print(args.skill,len(s),'headroom',100000-len(s),'| pages',len(GROUPS))
