from pathlib import Path
import hashlib
p=Path('dist/index.html')
s=p.read_text()

old='''    "Bet365":{live:false,title:"Import Bet365 bets",text:"Your Bet365 statement format is recognised. It contains sport, description, odds, result, stakes, returns, deposits and withdrawals. The statement is image-based, so the dedicated table reader is still being added before one-click importing is enabled."},'''
new='''    "Bet365":{live:true,title:"Import Bet365 bets",text:"Upload a Bet365 Statement of All Transactions PDF. Bet Tracker can read sport, description, selection odds, result, stakes/returns, deposits and withdrawals directly from the statement."},'''
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)

old='''  function setPaddyPanel(p){\n    const h2=p.querySelector(".bt-import-head h2");'''
new='''  function setPaddyPanel(p){\n    window.bt365RestorePaddy?.(p);\n    const h2=p.querySelector(".bt-import-head h2");'''
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)

old='''    if(bookmaker==="Paddy Power")setPaddyPanel(p);'''
new='''    if(bookmaker==="Paddy Power")setPaddyPanel(p);else if(bookmaker==="Bet365")window.bt365ConfigureImport?.(p);'''
assert s.count(old)==1,s.count(old)
s=s.replace(old,new,1)

js=Path('bet365_import.js').read_text()
s=s.replace('</body>',f'<script id="bt-bet365-import-v1">\n{js}\n</script>\n</body>',1)
p.write_text(s)
b=p.read_bytes()
assert len(b)==408740,len(b)
assert hashlib.sha256(b).hexdigest()=='8c7cdea779f910c19aa0596d617a0bb89a388c3c01240e68f0a9438279f2f380'
for marker in ['bt-bet365-import-v1','"Bet365":{live:true','window.bt365ConfigureImport?.(p)','AUTH_NAMESPACE="bettracker-auth:"']:
    assert marker in s,marker
print('Applied Bet365 importer:',len(b),'bytes')
