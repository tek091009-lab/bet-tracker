from pathlib import Path
import hashlib
p=Path('dist/index.html')
s=p.read_text()

old='''  const STORE_KEY="bet-tracker-live-v1";\n  const REMEMBER_KEY="betTrackerRememberDevice";'''
new='''  const STORE_KEY="bet-tracker-live-v1";\n  const AUTH_NAMESPACE="bettracker-auth:";\n  const REMEMBER_KEY="betTrackerRememberDevice";'''
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)

old='''  const authStorage={\n    getItem(k){return localStorage.getItem(k)||sessionStorage.getItem(k)},\n    setItem(k,v){if(localStorage.getItem(REMEMBER_KEY)==="1"){localStorage.setItem(k,v);sessionStorage.removeItem(k)}else{sessionStorage.setItem(k,v);localStorage.removeItem(k)}},\n    removeItem(k){localStorage.removeItem(k);sessionStorage.removeItem(k)}\n  };'''
new='''  const authStorage={\n    getItem(k){const n=AUTH_NAMESPACE+k;return localStorage.getItem(n)||sessionStorage.getItem(n)},\n    setItem(k,v){const n=AUTH_NAMESPACE+k;if(localStorage.getItem(REMEMBER_KEY)==="1"){localStorage.setItem(n,v);sessionStorage.removeItem(n)}else{sessionStorage.setItem(n,v);localStorage.removeItem(n)}},\n    removeItem(k){const n=AUTH_NAMESPACE+k;localStorage.removeItem(n);sessionStorage.removeItem(n)}\n  };'''
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)

# Do not clear origin-wide sessionStorage. Holiday Savings shares the same GitHub Pages origin.
old='sessionStorage.clear();await client.auth.signOut({scope:"local"}).catch(()=>{});'
assert s.count(old)==1,s.count(old)
s=s.replace(old,'await client.auth.signOut({scope:"local"}).catch(()=>{});',1)
old='sessionStorage.clear();location.reload()'
assert s.count(old)==1,s.count(old)
s=s.replace(old,'location.reload()',1)

p.write_text(s)
b=p.read_bytes()
assert len(b)==383642,len(b)
assert hashlib.sha256(b).hexdigest()=='dd8769c4549114c889767b1dd58f30fe709c633b16c876ea7d8154345bdf01bc'
assert 'AUTH_NAMESPACE="bettracker-auth:"' in s
assert 'sessionStorage.clear()' not in s
print('Applied Bet Tracker auth isolation:',len(b),'bytes')
