"""Generate static architecture diagrams from the public project accounts.

Run from any directory. Both sizes share the same nodes and relationships.
"""
from pathlib import Path
from html import escape
import re

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'public/diagrams'
# Node: identifier, title, description, kind, column, row.
DIAGRAMS = {
'ame-settlement': ('Settlement platform', [
('trade','Trade input','Reduced trade message','external',0,0),
('state','Settlement state','Trade lifecycle and instructions','service',1,0),
('gateway','Outbound gateway','Settlement instruction to SWIFT','service',2,0),
('updates','Downstream services','Receive updated trade state','external',0,1),
('matching','Matching service','Market update to the right trade','service',1,1),
('market','Market / SWIFT MQ','Instructions and confirmations','external',2,1)],
[('trade','state'),('state','gateway'),('gateway','market'),('market','matching'),('matching','state'),('state','updates')]),
'ame-business-flow': ('New business flow on shared infrastructure', [
('new','New business flow','Requirements and financial rules','external',0,0),
('platform','Shared AME platform','Seven existing services','service',1,0),
('existing','Existing business lines','Established behavior to preserve','external',2,0),
('regression','Regression framework','New and existing business cases','test',0,1),
('readiness','Readiness work','Integration across shared services','service',1,1)],
[('new','platform'),('existing','platform'),('regression','platform'),('readiness','platform')]),
'ame-adlc': ('Agent-assisted development architecture', [
('jira','Jira MCP','Ticket requirements','external',0,0),
('docs','Shared ADLC repo','Service and business-line context','store',1,0),
('code','Local repositories','Service source code','store',2,0),
('tests','Groovy framework','Local E2E scenario validation','test',0,1),
('claude','Claude Code','Context, code changes and tools','agent',1,1),
('bitbucket','Bitbucket MCP','PRs for pushed code changes','external',2,1),
('services','Local service setup','Mixed containers and processes','service',0,2),
('symphony','Symphony','Existing PR notification integration','external',2,2)],
[('jira','claude'),('docs','claude'),('code','claude'),('claude','tests'),('tests','services'),('claude','bitbucket'),('bitbucket','symphony')]),
'ame-regression': ('E2E regression test architecture', [
('cases','300+ scenarios','Messages and expected outcomes','store',0,0),
('runner','Groovy framework','Replay, polling and assertions','test',1,0),
('report','Failure reporting','Stakeholder email notifications','external',2,0),
('mq','MQ / Kafka','Scenario messages','broker',0,1),
('services','AME services','Dev environment or local setup','service',1,1),
('db','Service databases','Read and check resulting state','store',2,1)],
[('cases','runner'),('runner','report'),('runner','mq'),('mq','services'),('services','db'),('runner','db')]),
'ame-netting': ('Netting aggregation architecture', [
('trades','Trade table','Eligible underlying trades','store',0,0),
('engine','Netting aggregator','Combine compatible obligations','service',1,0),
('rules','Grouping rules','Multi-field netting identifier','store',2,0),
('schedule','Aggregation scheduler','Runs roughly every 5 seconds','service',0,1),
('release','Scheduled release','About one hour before EOD','service',1,1),
('gateway','Outbound processing','Consolidated instructions to SWIFT','external',2,1)],
[('trades','engine'),('rules','engine'),('schedule','engine'),('engine','release'),('release','gateway')]),
'ame-matching': ('Reusable matching-service architecture', [
('market','Market messages','Confirmations and status updates','external',0,0),
('matching','Kafka / WebFlux service','Enrich, transform and match','service',1,0),
('state','Settlement state','Apply matched trade updates','service',2,0),
('reference','External data services','Additional matching context','external',0,1),
('common','Composable functions','Shared processing across flows','store',1,1),
('business','Business-line behavior','Differences within the workflow','store',2,1)],
[('market','matching'),('matching','state'),('reference','matching'),('common','matching'),('business','matching')]),
'ame-eod': ('Concurrent end-of-day dispatch', [
('trigger','EOD message','Start bulk dispatch','external',0,0),
('pod1','Service pod A','Multithreaded processing','service',1,0),
('broker','Message broker','Published downstream messages','broker',2,0),
('db','Database work','Coordinated record pickup','store',0,1),
('pod2','Service pod B','Concurrent work pickup','service',1,1),
('downstream','Downstream services','End-of-day processing','external',2,1)],
[('trigger','pod1'),('db','pod1'),('db','pod2'),('pod1','broker'),('pod2','broker'),('broker','downstream')]),
'ame-search': ('Client-data search architecture', [
('sources','Reference services','Different data contracts','external',0,0),
('kafka','Kafka events','Asynchronous source updates','broker',1,0),
('db','Consolidated database','Client-data foundation','store',2,0),
('client','Search clients','Synchronous requests','external',0,1),
('search','Search component','Query construction and retrieval','service',1,1),
('index','Elasticsearch','Precomputed searchable client view','store',2,1)],
[('sources','kafka'),('kafka','index'),('client','search'),('search','index'),('db','index')]),
'ame-kubernetes': ('Team Kubernetes migration', [
('legacy','Existing services','Previous on-premises infrastructure','external',0,0),
('images','Container images','Service packaging','store',1,0),
('platform','Internal Kubernetes','Application pods','service',2,0),
('team','Senior engineers','Led the migration','external',1,1),
('support','My contribution','Assisted the team','external',0,1)],
[('legacy','images'),('images','platform'),('team','images'),('team','platform'),('support','team')]),
'splice': ('Splice: cache reuse and evaluation paths', [
('memory','Retrieved memories','Chunks change order per request','store',0,0),
('kv','Chunk KV store','Cached keys and values','store',1,0),
('position','RoPE re-rotation','Correct cached key positions','service',2,0),
('quality','Transformers path','Evaluate correction vs. recompute','agent',1,1),
('serving','vLLM connector','Serve uncorrected reuse','service',2,1),
('eval','Quality evaluation','LoCoMo F1 and context error','test',1,2),
('bench','Serving benchmark','Synthetic reuse; TTFT and throughput','test',2,2)],
[('memory','kv'),('kv','position'),('position','quality'),('position','serving'),('quality','eval'),('serving','bench')]),
'canary': ('Canary: monitor and policy evaluation', [
('data','Agent trajectories','SWE-agent and OpenHands','store',0,0),
('features','Prefix features','Only observations so far','service',1,0),
('monitor','ML monitors','LightGBM, GRU and baselines','agent',2,0),
('labels','Recorded outcomes','Held-out evaluation labels','store',0,1),
('policy','Stopping policy','Success-loss budget and threshold','service',1,1),
('analysis','Offline evaluation','Estimated cost saved / successes lost','test',2,1)],
[('data','features'),('features','monitor'),('monitor','policy'),('policy','analysis'),('labels','analysis')]),
'finetuning-lab': ('Fine-tuning experiment architecture', [
('data','TruthfulQA splits','Fixed train, validation and test','store',0,0),
('model','Qwen2.5-1.5B','Shared starting model','agent',1,0),
('variants','Training variants','LoRA ranks and full fine-tuning','service',2,0),
('checks','Training checks','Non-finite guard and reruns','test',0,1),
('runs','Three seeds','H100 training runs','service',1,1),
('eval','Held-out evaluation','MC1 accuracy and resource use','test',2,1)],
[('data','runs'),('model','variants'),('variants','runs'),('checks','runs'),('runs','eval')]),
'kv-cache-retention': ('KV-cache compression study', [
('data','LongBench questions','Same prompts and decoding','store',0,0),
('model','Llama-3-8B','Shared inference model','agent',1,0),
('methods','Four compression methods','Calibrated to 16 MiB prompt KV','service',2,0),
('logs','Retention logs','Positions kept by layer and head','store',0,1),
('runs','Compressed inference','Generate and record answers','service',1,1),
('review','Answer and evidence review','F1, alignment and failure analysis','test',2,1)],
[('data','runs'),('model','runs'),('methods','runs'),('runs','logs'),('runs','review'),('logs','review')]),
'llm-prompting-lab': ('Prompting benchmark architecture', [
('grid','Experiment settings','Model, temperature and prompt','store',0,0),
('ollama','Ollama models','Reversal and decimal division','agent',1,0),
('outputs','Model responses','Raw recorded outputs','store',2,0),
('truth','Python ground truth','Independent exact answers','service',0,1),
('grader','Deterministic grader','Accuracy and error categories','test',1,1),
('explorer','Result explorer','Aggregate and individual trials','external',2,1)],
[('grid','ollama'),('ollama','outputs'),('outputs','grader'),('truth','grader'),('grader','explorer')]),
'word2vec-lab': ('Embedding evaluation architecture', [
('data','Movie-review corpus','Shared training text','store',0,0),
('vectors','Embedding variants','Scratch, pretrained and fine-tuned','agent',1,0),
('sentences','Sentence vectors','Average word embeddings','service',2,0),
('similarity','Similarity checks','Human similarity benchmarks','test',0,1),
('classifier','Logistic regression','Same untuned evaluation recipe','service',1,1),
('results','Held-out results','Sentiment and controlled comparisons','test',2,1)],
[('data','vectors'),('vectors','sentences'),('vectors','similarity'),('sentences','classifier'),('classifier','results')])
}

STYLE='''
:root{--bg:#fff;--fg:#172333;--muted:#5d6a7d;--line:#8c9aaf;--grid:#e8edf4;--service:#edf4ff;--service-line:#668fd0;--store:#edf8f5;--store-line:#5a9b8a;--agent:#f3efff;--agent-line:#9280c6;--test:#fff7e9;--test-line:#bf994e;--external:#f5f6f8;--external-line:#a0a9b6}
@media(prefers-color-scheme:dark){:root{--bg:#111214;--fg:#e4e6ea;--muted:#a6b0c2;--line:#76859c;--grid:#252b35;--service:#17253b;--service-line:#6285bd;--store:#142b27;--store-line:#60998a;--agent:#252038;--agent-line:#9989c8;--test:#30281a;--test-line:#b5995f;--external:#1e2229;--external-line:#7b8595}}
.bg{fill:var(--bg)}.grid{fill:none;stroke:var(--grid);stroke-width:.7}.edge{fill:none;stroke:var(--line);stroke-width:1.5;stroke-linejoin:round}.arrow{fill:var(--line)}.node{stroke-width:1.2}.title{font:600 13px system-ui,sans-serif;fill:var(--fg)}.subtitle{font:11px system-ui,sans-serif;fill:var(--muted)}.type{font:9px ui-monospace,monospace;letter-spacing:.7px;fill:var(--muted)}
'''
TYPES={'service':'COMPONENT','store':'DATA / CONTEXT','agent':'MODEL / AGENT','test':'VALIDATION','external':'EXTERNAL','broker':'MESSAGING'}

def wrap(text,limit):
    words=text.split(); lines=[]; line=''
    for word in words:
        if line and len(line)+len(word)+1>limit: lines.append(line); line=word
        else: line=(line+' '+word).strip()
    if line: lines.append(line)
    return lines

def svg(name,mobile=False):
    title,nodes,edges=DIAGRAMS[name]
    W=400 if mobile else 760; NW=166 if mobile else 210; NH=112 if mobile else 104
    gapx=32 if mobile else 40; gapy=54 if mobile else 56
    pos={}
    for i,(key,_,_,_,col,row) in enumerate(nodes):
        c,r=(i%2,i//2) if mobile else (col,row)
        pos[key]=(18+c*(NW+gapx),30+r*(NH+gapy),c,r)
    H=max(y+NH for _,y,_,_ in pos.values())+30
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" aria-labelledby="title desc">',f'<title id="title">{escape(title)}</title>',f'<desc id="desc">{escape("; ".join(next(n[1] for n in nodes if n[0]==a)+" connects to "+next(n[1] for n in nodes if n[0]==b) for a,b in edges))}</desc>',f'<style>{STYLE}</style>',f'<defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path class="arrow" d="M0 0L10 5L0 10Z"/></marker><pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse"><path class="grid" d="M20 0H0V20"/></pattern></defs>',f'<rect class="bg" width="{W}" height="{H}"/><rect fill="url(#grid)" width="{W}" height="{H}"/>']
    for a,b in edges:
        ax,ay,ac,ar=pos[a]; bx,by,bc,br=pos[b]
        if ar==br:
            if ac<bc: x1,y1,x2,y2=ax+NW,ay+NH/2,bx,by+NH/2
            else: x1,y1,x2,y2=ax,ay+NH/2,bx+NW,by+NH/2
            if abs(ac-bc)>1:
                yy=ay-14; path=f'M{x1} {y1}H{x1+9}V{yy}H{x2-9}V{y2}H{x2}'
            else: path=f'M{x1} {y1}H{x2}'
        elif ac==bc and abs(ar-br)==1:
            x1=ax+NW/2; y1=ay+NH if ar<br else ay; y2=by if ar<br else by+NH
            path=f'M{x1} {y1}V{y2}'
        elif ac==bc:
            xx=ax-10 if ac==0 else ax+NW+10
            x1=ax if ac==0 else ax+NW
            path=f'M{x1} {ay+NH/2}H{xx}V{by+NH/2}H{x1}'
        else:
            # Route through the space between rows, rather than through components.
            x1=ax+NW/2; y1=ay+NH if ar<br else ay
            x2=bx+NW/2; y2=by if ar<br else by+NH
            gutter=ax+NW+gapx/2 if bc>ac else ax-gapx/2
            source_lane=y1+gapy/2 if ar<br else y1-gapy/2
            target_lane=y2-gapy/2 if ar<br else y2+gapy/2
            path=f'M{x1} {y1}V{source_lane}H{gutter}V{target_lane}H{x2}V{y2}'
        parts.append(f'<path class="edge" d="{path}" marker-end="url(#arrow)"/>')
    for key,label,detail,kind,_,_ in nodes:
        x,y,_,_=pos[key]; color='service' if kind=='broker' else kind
        parts.append(f'<g><rect class="node" x="{x}" y="{y}" width="{NW}" height="{NH}" rx="9" fill="var(--{color})" stroke="var(--{color}-line)"/>')
        parts.append(f'<text class="type" x="{x+12}" y="{y+19}">{TYPES[kind]}</text>')
        lines=wrap(label,20 if mobile else 26)
        for j,line in enumerate(lines): parts.append(f'<text class="title" x="{x+12}" y="{y+40+j*16}">{escape(line)}</text>')
        for j,line in enumerate(wrap(detail,24 if mobile else 30)):
            parts.append(f'<text class="subtitle" x="{x+12}" y="{y+43+len(lines)*16+j*14}">{escape(line)}</text>')
        parts.append('</g>')
    parts.append('</svg>')
    return '\n'.join(parts),H

OUT.mkdir(exist_ok=True)
for name in DIAGRAMS:
    for mobile in (False,True):
        image,_=svg(name,mobile)
        (OUT/f'{name}{"-mobile" if mobile else ""}.svg').write_text(image+'\n')

# Replace only the summary diagrams added during this discussion.
roles={
'associate':['ame-settlement','ame-business-flow','ame-adlc','ame-regression','ame-netting'],
'analyst':['ame-matching','ame-eod','ame-search','ame-kubernetes']}
pages=[(ROOT/f'src/content/experience/jp-morgan-chase-{role}.md',names) for role,names in roles.items()]
pages += [(ROOT/f'src/content/projects/{name}.md',[name]) for name in DIAGRAMS if not name.startswith('ame-')]
for page,names in pages:
    text=page.read_text()
    figures=list(re.finditer(r'<figure class="(?:system-flow|architecture-diagram)">.*?</figure>',text,re.S))
    assert len(figures)==len(names),(page,len(figures))
    for match,name in reversed(list(zip(figures,names))):
        caption=re.search(r'<figcaption>(.*?)</figcaption>',match[0],re.S)[1]
        title=DIAGRAMS[name][0]
        _,height=svg(name)
        replacement=f'''<figure class="architecture-diagram">
<p class="architecture-label">{escape(title)}</p>
<picture>
<source media="(max-width: 34rem)" srcset="/diagrams/{name}-mobile.svg" />
<img src="/diagrams/{name}.svg" alt="{escape(title)}: {escape('; '.join(n[1] for n in DIAGRAMS[name][1]))}. Arrows show component connections." width="760" height="{height}" loading="lazy" />
</picture>
<figcaption>{caption}</figcaption>
</figure>'''
        text=text[:match.start()]+replacement+text[match.end():]
    page.write_text(text)
print(f'Generated {len(DIAGRAMS)} architecture diagrams in desktop/mobile layouts.')
