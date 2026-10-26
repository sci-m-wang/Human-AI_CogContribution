import os, sys, json, base64, hashlib, time, urllib.request, urllib.error
base=os.environ['AZURE_OPENAI_BASE_URL'].rstrip('/'); key=os.environ['AZURE_OPENAI_API_KEY']; dep=os.environ['AZURE_OPENAI_DEPLOYMENT']
def gen(prompt_file,out,size='1536x1024',quality='high'):
    prompt=open(prompt_file,encoding='utf-8').read()
    body=json.dumps({'model':dep,'prompt':prompt,'size':size,'quality':quality,'n':1}).encode()
    req=urllib.request.Request(base+'/images/generations',data=body,headers={'api-key':key,'Content-Type':'application/json'})
    t0=time.time()
    try:
        r=json.load(urllib.request.urlopen(req,timeout=600))
    except urllib.error.HTTPError as e:
        print('HTTP',e.code,e.read()[:400].decode('utf-8','replace')); return False
    d=r['data'][0]
    if 'b64_json' in d: img=base64.b64decode(d['b64_json'])
    else: img=urllib.request.urlopen(d['url']).read()
    open(out,'wb').write(img)
    rec={'tool':'azure-openai images/generations (python port of imagegen.mjs)','model':dep,'size':size,'quality':quality,'prompt_file':os.path.basename(prompt_file),
         'prompt_sha256':hashlib.sha256(prompt.encode('utf-8')).hexdigest(),'seconds':round(time.time()-t0,1),'bytes':len(img),'output_sha256':hashlib.sha256(img).hexdigest(),
         'timestamp':time.strftime('%Y-%m-%dT%H:%M:%S%z')}
    json.dump(rec,open(out+'.json','w'),indent=1); print('ok',out,rec['seconds'],'s',len(img),'bytes'); return True
if __name__=='__main__':
    gen(sys.argv[1],sys.argv[2],*(sys.argv[3:4] or ['1536x1024']))
