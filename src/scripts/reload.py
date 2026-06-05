import urllib.request, json, http.cookiejar

# Читаем token из jupyter
try:
    with urllib.request.urlopen('http://localhost:8889/api/sessions') as r:
        sessions = json.loads(r.read())
    print('Sessions:', len(sessions))
    changed = ['FunctorHierarchy','Comonads','Profunctors','Optics',
               'YonedaLemma','MetaProgramming','Concurrency','DistributedHaskell','GPUHaskell']
    for s in sessions:
        path = s.get('path','') or s.get('notebook',{}).get('path','')
        name = path.replace('.ipynb','').split('/')[-1]
        if name in changed:
            print(f'Session found for {name}: {s["id"]}')
except Exception as e:
    print(f'Error: {e}')
