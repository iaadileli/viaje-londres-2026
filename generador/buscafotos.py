import json, subprocess, time, sys
def buscar(q, n=6):
    cmd = ['curl','-s','--max-time','25','-G','https://commons.wikimedia.org/w/api.php',
      '--data-urlencode','action=query','--data-urlencode','generator=search',
      '--data-urlencode',f'gsrsearch={q}','--data-urlencode','gsrnamespace=6',
      '--data-urlencode',f'gsrlimit={n}','--data-urlencode','prop=imageinfo',
      '--data-urlencode','iiprop=url|size|extmetadata','--data-urlencode','iiurlwidth=1100',
      '--data-urlencode','format=json']
    try: pages = json.loads(subprocess.run(cmd, capture_output=True, text=True).stdout).get('query',{}).get('pages',{})
    except Exception: return []
    out=[]
    for p in pages.values():
        i=p['imageinfo'][0]; m=i.get('extmetadata',{})
        if i['width'] < 640: continue
        if not p['title'].lower().endswith(('.jpg','.jpeg')): continue  # la url trae parámetros al final
        out.append({'t':p['title'], 'url':i.get('thumburl') or i['url'],
                    'lic':m.get('LicenseShortName',{}).get('value','?'),
                    'w':i['width']})
    return out
if __name__ == '__main__':
    PLATOS = json.load(open(sys.argv[1]))
    res = {}
    for k, q in PLATOS.items():
        r = buscar(q); res[k] = r
        print(f'  {k:12s} {len(r)} · ' + (f'{r[0]["t"][5:52]}  [{r[0]["lic"]}]' if r else '— sin resultado'))
        time.sleep(0.5)
    json.dump(res, open(sys.argv[2],'w'), ensure_ascii=False)
