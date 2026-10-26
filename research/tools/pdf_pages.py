import sys, pypdf
r=pypdf.PdfReader(sys.argv[1]); n=len(r.pages); ref=None
for i,p in enumerate(r.pages):
    t=p.extract_text() or ''
    if 'References' in t and ref is None and i>2:
        # references heading page: check first lines
        if t.strip().split('\n')[0].strip().startswith('References') or '\nReferences\n' in t: ref=i+1
print('total pages',n,'references start page',ref)
for i in range(n):
    t=(r.pages[i].extract_text() or '').strip().split('\n')
    print(i+1, len((r.pages[i].extract_text() or '').split()),'words |', t[0][:70] if t else '')
