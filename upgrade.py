from pathlib import Path
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
p.write_text(s)
assert len(s.encode())==350096,len(s.encode())
assert "bt-live-v2-enhancer" in s and "Save ladder to history" in s and "Your sports & betting apps" in s
