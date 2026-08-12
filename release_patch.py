from pathlib import Path
import base64,gzip,hashlib
p=Path('dist/index.html')
s=p.read_text()

# Give each rendered bet row its stable id so the browser can support Excel-style multi-select.
old='function m1({item:t,onEdit:l,onDelete:a}){return(0,c.jsxs)("tr",{children:['
new='function m1({item:t,onEdit:l,onDelete:a}){return(0,c.jsxs)("tr",{"data-bet-id":t.id,children:['
assert old in s
s=s.replace(old,new,1)

# General Paddy Power statement imports: the statement does not contain sport/event/selection details.
old='''      <label>Existing Bet Tracker Excel <span style="font-weight:400">(optional)</span><input id="bt-import-enrichment" type="file" accept=".xlsx,.xls"><small>If supplied, Bet Tracker uses your old workbook to restore sport, description, odds, type and result where possible.</small></label>
      <div style="align-self:end"><small><strong style="color:#d6e2f4">Paddy Power:</strong> statement = money/account history. Old tracker = detailed bet metadata. Unmatched rows are flagged for review instead of guessed.</small></div>'''
new='''      <div class="bt-paddy-limit" style="grid-column:1/-1;padding:12px 14px;border-radius:12px;background:rgba(255,184,0,.08);border:1px solid rgba(255,184,0,.2);color:#d9c98f;font-size:12px;line-height:1.55"><strong style="color:#ffe08a">What Paddy Power does not provide:</strong> its customer statement does not include the sport, event, market or selection for normal sportsbook bets. Bet Tracker will therefore import <strong>Sport</strong> and <strong>Description</strong> as blank. Fill those in after import — you can select multiple bets in Bet Tracker and update them together.</div>'''
assert old in s
s=s.replace(old,new,1)

old='const status=document.querySelector("#bt-import-status"),btn=document.querySelector("#bt-read-import"),statement=document.querySelector("#bt-import-statement")?.files?.[0],enrich=document.querySelector("#bt-import-enrichment")?.files?.[0];'
new='const status=document.querySelector("#bt-import-status"),btn=document.querySelector("#bt-read-import"),statement=document.querySelector("#bt-import-statement")?.files?.[0];'
assert old in s
s=s.replace(old,new,1)

old='''      const paddy=await parsePaddyPdf(statement);let tracker=[];
      if(enrich){status.textContent="Reading your old Bet Tracker workbook…";tracker=await parseTrackerExcel(enrich,"Paddy Power")}
      const recon=reconcile(paddy.bets,tracker);
      parsed={...paddy,tracker,recon};'''
new='''      const paddy=await parsePaddyPdf(statement);const tracker=[];
      const recon=reconcile(paddy.bets,tracker);
      parsed={...paddy,tracker,recon};'''
assert old in s
s=s.replace(old,new,1)

old='      status.textContent=`Found ${paddy.bets.length} sportsbook bets${tracker.length?` and ${tracker.length} Paddy Power rows in your old tracker`:""}.`;'
new='      status.textContent=`Found ${paddy.bets.length} Paddy Power sportsbook bets. Sport and Description will be left blank because the statement does not contain them.`;'
assert old in s
s=s.replace(old,new,1)

old='let m=rest.match(/^(S\\/\\d+\\/\\d+)\\s*Sports:\\s*Bet Placed\\s*\\(Transaction ID:\\s*(S\\/\\d+\\/\\d+)\\)\\s*([0-9]+(?:\\.[0-9]+)?)\\s+([0-9]+(?:\\.[0-9]+)?)$/i);'
new='let m=rest.match(/^(S\\/\\d+\\/\\d+)\\s*Sports:\\s*(?:Free\\s*Bet\\s*)?Bet Placed(?:.*?Free\\s*Bet.*?)?\\s*\\(Transaction ID:\\s*(S\\/\\d+\\/\\d+)\\)\\s*([0-9]+(?:\\.[0-9]+)?)\\s+([0-9]+(?:\\.[0-9]+)?)$/i)||rest.match(/^(S\\/\\d+\\/\\d+)\\s*Sports:\\s*Bet Placed\\s*\\(Transaction ID:\\s*(S\\/\\d+\\/\\d+)\\)\\s*([0-9]+(?:\\.[0-9]+)?)\\s+([0-9]+(?:\\.[0-9]+)?)$/i);'
assert old in s
s=s.replace(old,new,1)

old='if(m){bets.push({date,time,when,app:"Paddy Power",sourceRef:m[1],transactionId:m[2],stake:Number(m[3]),balanceAfter:Number(m[4]),sport:"Uncategorised",type:"Medium Risk (Evs - 10/1)",description:"Paddy Power sportsbook bet",odds:1,result:"Pending",matchConfidence:"unmatched",matchedFromTracker:false});continue}'
new='if(m){const isFree=/free\\s*bet|freebet|bonus\\s*bet/i.test(rest);bets.push({date,time,when,app:"Paddy Power",sourceRef:m[1],transactionId:m[2],stake:Number(m[3]),balanceAfter:Number(m[4]),sport:"",type:isFree?"Free Bet":"Medium Risk (Evs - 10/1)",description:"",odds:1,result:"Pending",matchConfidence:"unmatched",matchedFromTracker:false,freeBetDetected:isFree});continue}'
assert old in s
s=s.replace(old,new,1)

old='''    <p class="bt-preview-note">${parsed.tracker.length?`Your old tracker is being used to enrich Paddy Power rows with sport, description, odds, bet type and result. ${parsed.recon.matched} tracker rows were directly reconciled; tracker-only and statement-only rows are clearly flagged.`:"No old tracker was supplied, so Paddy rows use generic descriptions and remain Pending until reviewed."} Deposits and withdrawals come from the statement. Casino/gaming rows are excluded.</p>'''
new='''    <p class="bt-preview-note"><strong>Paddy Power limitation:</strong> the statement does not provide the sport, event, market or selection for normal sportsbook bets, so <strong>Sport and Description are intentionally left blank</strong>. Fill them in after import; Bet Tracker supports selecting several bets and bulk-editing those fields together. Free Bets are marked automatically when the statement identifies them. Deposits and withdrawals come from the statement. Casino/gaming rows are excluded.</p>'''
assert old in s
s=s.replace(old,new,1)

old='r.matchConfidence==="tracker-only"?"Tracker only":"Unresolved"'
new='r.matchConfidence==="tracker-only"?"Tracker only":"Statement only"'
assert old in s
s=s.replace(old,new,1)

old='sport:r.sport||"Uncategorised",type:r.type||"Medium Risk (Evs - 10/1)",description:r.description||"Paddy Power sportsbook bet"'
new='sport:r.sport??"",type:r.type||"Medium Risk (Evs - 10/1)",description:r.description??""'
assert old in s
s=s.replace(old,new,1)

# Add bulk-selection/bulk-edit UI.
bulk=gzip.decompress(base64.b64decode(''.join(Path('bulk/bulk-v1.b64').read_text().split()))).decode()
assert hashlib.sha256(bulk.encode()).hexdigest()=='dc0daf188100f3f222e7e8ceb3f2135da4c418eadcd41c3af7f8a08d81d02f90'
s=s.replace('</body>',f'<script id="bt-bulk-bets-v1">\n{bulk}\n</script>\n</body>',1)

p.write_text(s)
b=p.read_bytes()
assert len(b)==385806,len(b)
assert hashlib.sha256(b).hexdigest()=='7c8723e6c8f4e9a1028c0672c45c6aab29513c89cac9c5eea133c9e44426a169'
for marker in ['bt-bulk-bets-v1','data-bet-id','Delete selected','Select all filtered','Sport and Description are intentionally left blank','What Paddy Power does not provide']:
    assert marker in s,marker
print('Applied Paddy import + bulk edit release:',len(b),'bytes')
