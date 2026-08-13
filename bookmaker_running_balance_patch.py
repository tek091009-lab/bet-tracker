from pathlib import Path
import hashlib
p=Path('dist/index.html')
b=p.read_bytes()
assert len(b)==423651,len(b)
assert hashlib.sha256(b).hexdigest()=='5f01ae48883f7add774bb5b0ccc2fec9962217312af631c7e2ff6449acad2013'
s=b.decode()
old='lm=t=>{let l=as(t.bets),a=0,e=0;return l.map(n=>{let u=t.transactions.filter(b=>(Number(b.createdAt)||Date.parse(b.date+"T12:00:00"))<=(Number(n.createdAt)||Date.parse(n.date+"T12:00:00"))).reduce((b,h)=>b+(h.type==="deposit"?h.amount:-h.amount),0),o=Object.values(t.bookmakerStartingBalances||{}).reduce((b,h)=>{let d=typeof h==="object"&&h?h.date:null,p=typeof h==="number"?h:Number(h?.amount)||0;return b+(!d||d<=n.date?p:0)},0),i=t.startingBalance+o+u+a-e,f=Pt(n),s=_n(n),m=s>0&&i>0?s/i:0;return f===null?e+=s:a+=f,{...n,potentialReturns:ts(n),profitLoss:f,bankrollRisk:m,balanceAfter:t.startingBalance+o+u+a-e}})}'
new='lm=t=>{let l=as(t.bets),a={},e={};return l.map(n=>{let r=n.app,u=t.transactions.filter(b=>b.app===r&&(Number(b.createdAt)||Date.parse(b.date+"T12:00:00"))<=(Number(n.createdAt)||Date.parse(n.date+"T12:00:00"))).reduce((b,h)=>b+(h.type==="deposit"?h.amount:-h.amount),0),o=t.bookmakerStartingBalances?.[r],q=typeof o==="object"&&o?(!o.date||o.date<=n.date?Number(o.amount)||0:0):Number(o)||0,i=q+u+(a[r]||0)-(e[r]||0),f=Pt(n),s=_n(n),m=s>0&&i>0?s/i:0;return f===null?e[r]=(e[r]||0)+s:a[r]=(a[r]||0)+f,{...n,potentialReturns:ts(n),profitLoss:f,bankrollRisk:m,balanceAfter:q+u+(a[r]||0)-(e[r]||0)}})}'
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)
marker='<!-- bt-bookmaker-running-balance-v1: bet rows use bookmaker-specific timed cash movements -->\n'
assert marker not in s
s=s.replace('</body>',marker+'</body>',1)
p.write_text(s)
b=p.read_bytes()
assert len(b)==423725,len(b)
assert hashlib.sha256(b).hexdigest()=='cb2ef414ab60c37f09d48ca790e56d0aa2763225b561efae6666487371092ada'
assert 'bt-bookmaker-running-balance-v1' in s
assert 'b.app===r' in s and 't.bookmakerStartingBalances?.[r]' in s
print('Applied bookmaker-specific timed running balance patch:',len(b),'bytes')
