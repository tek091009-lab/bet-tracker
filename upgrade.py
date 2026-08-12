from pathlib import Path
import base64,gzip,hashlib
p=Path("dist/index.html")
s=p.read_text()
R={
"Local prototype":"Live account",
"Your changes save automatically in this browser. No bookmaker account is connected.":"Your changes save automatically to your account and sync across your devices.",
"View connection plan →":"Manage connections →",
"Future integrations":"Imports & integrations",
"This prototype keeps data on your device, but the app is structured so manual entry can later be replaced by official account connectors.":"Bet Tracker is live with account sync. Bookmaker history can be added manually, by file import, or later through approved account connectors where available.",
"Connection-ready structure":"Import-ready structure",
"No rebuild required later.":"Built for account and file connections.",
"The screens read from one data service. Today it saves in your browser; a later version can point that same service at accounts and cloud storage.":"Your tracker already syncs through your account. File imports and approved bookmaker connections can feed the same data without changing the rest of the app.",
"Manual in prototype":"Manual / file import",
"No equivalent public customer OAuth connection has been committed to this prototype.":"No equivalent public customer account connection is currently enabled, so these remain manual or file-import routes.",
"Local data controls":"Data controls","Back up this prototype":"Back up Bet Tracker",
"Export everything to a JSON file, restore a previous backup, or reset to the original example data.":"Export everything to a JSON file, restore a previous backup, or clear your tracker data while keeping your account.",
"Reset demo":"Reset tracker",
"Enter the starting stake, target return and number of days. The required decimal odds and every step calculate automatically.":"Choose your starting stake, target and number of bets. Bet Tracker calculates the odds needed and automatically adjusts the remaining ladder after each result.",
"Number of days":"Number of bets","Required odds per step":"Required odds per bet"," steps completed":" bets completed",
' across ",a.days," steps.':' across ",a.days," bets.','children:"Day"':'children:"Bet"'}
for a,b in R.items(): s=s.replace(a,b)
old='var _l=["Bet365","Paddy Power","William Hill","Betfred","Ladbrokes","Betfair","Sky Bet"],On=["Football","Darts","Basketball","Free Spins"],Mn='
new='var _l=(()=>{let t=["Bet365","Paddy Power","William Hill","Betfred","Ladbrokes","Betfair","Sky Bet"];try{let l=JSON.parse(localStorage.getItem("bet-tracker-prototype-v1")||"{}");return[...new Set([...t,...(Array.isArray(l.customApps)?l.customApps:[])])]}catch{return t}})(),On=(()=>{let t=["Football","Darts","Basketball","Free Spins"];try{let l=JSON.parse(localStorage.getItem("bet-tracker-prototype-v1")||"{}");return[...new Set([...t,...(Array.isArray(l.customSports)?l.customSports:[])])]}catch{return t}})(),Mn='
assert old in s;s=s.replace(old,new,1)
old='f=is[u];return(0,c.jsxs)("article",{className:"bank-card"'
assert old in s;s=s.replace(old,'f=is[u]??{accent:"#2e67f0",secondary:"#0d2945",text:"#fff"};return(0,c.jsxs)("article",{className:"bank-card"',1)
old='style:{background:is[i].accent,color:is[i].text??"#fff"}'
new='style:{background:(is[i]??{accent:"#2e67f0",text:"#fff"}).accent,color:(is[i]??{text:"#fff"}).text??"#fff"}'
assert old in s;s=s.replace(old,new,1)
old='    "Sky Bet": "skybet.com"\n  };'
assert old in s;s=s.replace(old,'    "Sky Bet": "skybet.com",\n    ...((()=>{try{return JSON.parse(localStorage.getItem("bet-tracker-prototype-v1")||"{}").customAppDomains||{}}catch{return{}}})())\n  };',1)
extra=Path("/tmp/bt-extra.html").read_text()
s=s.replace("</body>",extra+"\n</body>",1)
s=s.replace("bet-tracker-prototype-v1","bet-tracker-live-v1")

# Import-aware account state: exact imported returns/P&L and per-bookmaker opening balances.
assert s.count('version:1,startingBalance:0,transactions:[],bets:[]') == 2
s=s.replace('version:1,startingBalance:0,transactions:[],bets:[]','version:1,startingBalance:0,bookmakerStartingBalances:{},transactions:[],bets:[]')
old='ts=t=>!t.odds||!t.stake?0:fi(t)?t.odds*t.stake-t.stake:t.odds*t.stake,Pt=t=>t.result==="Pending"?null:t.result==="Void"?0:t.result==="Cash Out"?t.cashoutProfit??0:t.result==="Loss"?fi(t)?0:-t.stake:t.result==="Win"?fi(t)?ts(t):ts(t)-t.stake:null,_n=t=>fi(t)?0:t.stake,as=t=>[...t].sort((l,a)=>l.date.localeCompare(a.date)||l.createdAt-a.createdAt),lm=t=>{let l=as(t.bets),a=0,e=0;return l.map(n=>{let u=t.transactions.filter(b=>b.date<=n.date).reduce((b,h)=>b+(h.type==="deposit"?h.amount:-h.amount),0),i=t.startingBalance+u+a-e,f=Pt(n),s=_n(n),m=s>0&&i>0?s/i:0;return f===null?e+=s:a+=f,{...n,potentialReturns:ts(n),profitLoss:f,bankrollRisk:m,balanceAfter:t.startingBalance+u+a-e}})},oi=t=>{let l=t.transactions.reduce((e,n)=>e+(n.type==="deposit"?n.amount:-n.amount),0),a=t.bets.reduce((e,n)=>e+(Pt(n)??-_n(n)),0);return t.startingBalance+l+a},es=(t,l)=>{let a=t.transactions.filter(u=>u.app===l&&u.type==="deposit").reduce((u,i)=>u+i.amount,0),e=t.transactions.filter(u=>u.app===l&&u.type==="withdrawal").reduce((u,i)=>u+i.amount,0),n=t.bets.filter(u=>u.app===l).reduce((u,i)=>u+(Pt(i)??-_n(i)),0);return{balance:a-e+n,deposits:a,withdrawals:e,netDW:e-a}}'
new='ts=t=>Number.isFinite(t.importedPotentialReturns)?t.importedPotentialReturns:!t.odds||!t.stake?0:fi(t)?t.odds*t.stake-t.stake:t.odds*t.stake,Pt=t=>Number.isFinite(t.manualProfitLoss)?t.manualProfitLoss:t.result==="Pending"?null:t.result==="Void"?0:t.result==="Cash Out"?t.cashoutProfit??0:t.result==="Loss"?fi(t)?0:-t.stake:t.result==="Win"?fi(t)?ts(t):ts(t)-t.stake:null,_n=t=>fi(t)?0:t.stake,as=t=>[...t].sort((l,a)=>l.date.localeCompare(a.date)||l.createdAt-a.createdAt),lm=t=>{let l=as(t.bets),a=0,e=0;return l.map(n=>{let u=t.transactions.filter(b=>b.date<=n.date).reduce((b,h)=>b+(h.type==="deposit"?h.amount:-h.amount),0),o=Object.values(t.bookmakerStartingBalances||{}).reduce((b,h)=>{let d=typeof h==="object"&&h?h.date:null,p=typeof h==="number"?h:Number(h?.amount)||0;return b+(!d||d<=n.date?p:0)},0),i=t.startingBalance+o+u+a-e,f=Pt(n),s=_n(n),m=s>0&&i>0?s/i:0;return f===null?e+=s:a+=f,{...n,potentialReturns:ts(n),profitLoss:f,bankrollRisk:m,balanceAfter:t.startingBalance+o+u+a-e}})},oi=t=>{let l=t.transactions.reduce((e,n)=>e+(n.type==="deposit"?n.amount:-n.amount),0),a=t.bets.reduce((e,n)=>e+(Pt(n)??-_n(n)),0),o=Object.values(t.bookmakerStartingBalances||{}).reduce((e,n)=>e+(typeof n==="number"?n:Number(n?.amount)||0),0);return t.startingBalance+o+l+a},es=(t,l)=>{let a=t.transactions.filter(u=>u.app===l&&u.type==="deposit").reduce((u,i)=>u+i.amount,0),e=t.transactions.filter(u=>u.app===l&&u.type==="withdrawal").reduce((u,i)=>u+i.amount,0),n=t.bets.filter(u=>u.app===l).reduce((u,i)=>u+(Pt(i)??-_n(i)),0),o=t.bookmakerStartingBalances?.[l],r=typeof o==="number"?o:Number(o?.amount)||0;return{balance:r+a-e+n,startingBalance:r,deposits:a,withdrawals:e,netDW:e-a}}'
assert s.count(old)==1
s=s.replace(old,new,1)

# Self-service Connections importer. The uploaded files are parsed in the browser; only imported tracker data is persisted.
import_js=gzip.decompress(base64.b64decode(''.join(Path('import/import-v1.b64').read_text().split()))).decode()
assert hashlib.sha256(import_js.encode()).hexdigest()=='cc091bd4ea3c901c6adb83d5b1bc16514c5d43e41dfdf0d08dad6d08ddfc62c5'
s=s.replace('</body>',f'<script id="bt-import-bets-v1">\n{import_js}\n</script>\n</body>',1)

p.write_text(s)
b=s.encode()
assert len(b)==375553,len(b)
assert hashlib.sha256(b).hexdigest()=='ff3d4675f69201265eaccb0d7d64ecde844f06116573c94b3580ac60c9bd29fe'
for marker in ['bt-live-v2-enhancer','Save ladder to history','Your sports & betting apps','bt-import-bets-v1','Paddy Power statement PDF','bookmakerStartingBalances']:
    assert marker in s,marker
