from pathlib import Path
import hashlib,re
p=Path('dist/index.html')
s=p.read_text()

# Emergency stability rollback: remove the entire DOM-driven bulk-selection layer.
# It was attaching UI and row handlers inside the React-owned Bet Tracker page.
s,n=re.subn(r'\n?<script id="bt-bulk-bets-v1">.*?</script>\n?', '\n', s, count=1, flags=re.S)
assert n==1,n

# Restore React bet rows to their native structure as well.
old='function m1({item:t,onEdit:l,onDelete:a}){return(0,c.jsxs)("tr",{"data-bet-id":t.id,children:['
new='function m1({item:t,onEdit:l,onDelete:a}){return(0,c.jsxs)("tr",{children:['
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)

p.write_text(s)
b=p.read_bytes()
assert len(b)==383570,len(b)
assert hashlib.sha256(b).hexdigest()=='ed29821ea31fa9df732a3cc5c2aeb4ebbed8ba3eb7ab229b00e67d2848b7b6f3'
assert 'bt-bulk-bets-v1' not in s
assert 'data-bet-id' not in s
assert 'bt-connections-card-import-v2' in s
assert 'bt-import-bets-v1' in s
print('Applied Bet Tracker stability rollback:',len(b),'bytes')
