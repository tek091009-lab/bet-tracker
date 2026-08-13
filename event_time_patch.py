from pathlib import Path
import hashlib
p=Path('dist/index.html')
b=p.read_bytes()
assert len(b)==423486,len(b)
assert hashlib.sha256(b).hexdigest()=='7feb4b213058a71963577a8cec22a77b55ec04da603f5c31693917ddb3529435'
s=b.decode()
old='t.transactions.filter(b=>b.date<=n.date)'
new='t.transactions.filter(b=>(Number(b.createdAt)||Date.parse(b.date+"T12:00:00"))<=(Number(n.createdAt)||Date.parse(n.date+"T12:00:00")))'
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)
assert old not in s
marker='<!-- bt-event-time-v1: running bankroll uses transaction createdAt -->\n'
assert marker not in s
s=s.replace('</body>',marker+'</body>',1)
p.write_text(s)
b=p.read_bytes()
assert len(b)==423651,len(b)
assert hashlib.sha256(b).hexdigest()=='5f01ae48883f7add774bb5b0ccc2fec9962217312af631c7e2ff6449acad2013'
assert 'bt-event-time-v1' in s
assert 'Number(b.createdAt)' in s and 'Number(n.createdAt)' in s
print('Applied transaction event-time bankroll patch:',len(b),'bytes')
