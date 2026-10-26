import docx, re, sys
d=docx.Document(sys.argv[1])
paras=[(p.style.name,p.text) for p in d.paragraphs if p.text.strip()]
body=[]; 
for s,t in paras:
    if s=='Heading 1' and t.strip()=='References': break
    body.append((s,t))
bad=0
print('== dashes and semicolons')
for s,t in body:
    for ch,name in [('\u2014','em dash'),('\u2013','en dash'),(';','semicolon')]:
        if ch in t: print(name,'|',s,'|',t[:90]); bad+=1
print('== colons per paragraph (>1)')
for s,t in body:
    if s=='Normal' and t.count(':')>1: print(t.count(':'),'|',t[:100])
print('== sentence length (<5 or >32 words), body paragraphs only')
for s,t in body:
    if s!='Normal': continue
    # strip citations in parentheses for sentence split
    sents=re.split(r'(?<=[.?!])\s+(?=[A-Z(])',t)
    for x in sents:
        n=len(x.split())
        if n<5 or n>32: print(n,'|',x[:140])
print('== risky phrases')
pats=[r'worth noting',r'\bwe do not\b',r'\bwithout\b',r'\bno [a-z]+ ',r'\bnot used\b',r'\bonly\b',r'admittedly',r'we should point out',r'it should be noted',r'\bcould not\b',r'\bcannot\b',r'\bnot\b']
for s,t in body:
    if s!='Normal': continue
    for pt in pats:
        for m in re.finditer(pt,t):
            a=max(0,m.start()-40); print(pt,'|',t[a:m.end()+50].replace('\n',' ')); 
print('== paragraph sentence counts (<3 or >9)')
for s,t in body:
    if s!='Normal' or len(t.split())<40: continue
    n=len(re.split(r'(?<=[.?!])\s+(?=[A-Z(])',t))
    if n<4 or n>10: print(n,'|',t[:80])
print('== italics in body runs')
for p in d.paragraphs:
    if p.style.name=='Normal' and any(r.italic for r in p.runs) and not p.text.startswith(('Ackoff',)):
        if 'https://doi' not in p.text: print('italic run |',p.text[:80])
