from pathlib import Path
import re, hashlib
p=Path('dist/index.html')
s=p.read_text()

# Bet365 must open its own dedicated importer rather than reusing the Paddy panel.
old='function openImport(bookmaker){const info=BOOKMAKERS[bookmaker];if(!info)return;if(info.live)openLive(bookmaker);else openInfo(bookmaker)}'
new='function openImport(bookmaker){const info=BOOKMAKERS[bookmaker];if(!info)return;if(bookmaker==="Bet365"){window.bt365OpenDedicated?.();return}if(info.live)openLive(bookmaker);else openInfo(bookmaker)}'
assert s.count(old)==1, s.count(old)
s=s.replace(old,new,1)

m=re.search(r'(<script id="bt-bet365-import-v1">\n)(.*?)(\n</script>)',s,re.S)
assert m
js=m.group(2)
oldlet='let pdfModule=null,tessPromise=null,worker=null,current=null,paddySnapshot=null,paddyReadHandler=null;'
newlet='let pdfModule=null,tessPromise=null,worker=null,current=null,paddySnapshot=null,paddyReadHandler=null,activeImportPanel=null;\n  const importPanel=()=>activeImportPanel||document.querySelector("#bt-import-bets");'
assert js.count(oldlet)==1
js=js.replace(oldlet,newlet,1)
js=js.replace('document.querySelector("#bt-import-bets")','importPanel()')

marker='  window.bt365RestorePaddy=restorePaddy;'
assert marker in js
opener=r'''  window.bt365OpenDedicated=()=>{
    document.querySelector("#bt-import-modal-backdrop")?.remove();
    const back=document.createElement("div");back.id="bt-import-modal-backdrop";back.className="bt-import-modal-backdrop";
    const p=document.createElement("section");p.id="bt365-dedicated-import";p.className="bt-import-panel bt-import-modal-panel bt-modal-open";
    p.innerHTML=`
      <button class="bt-import-modal-close" type="button" aria-label="Close Bet365 import">×</button>
      <div class="bt-import-head"><div><p class="eyebrow">BET365 HISTORY</p><h2>Import Bet365 bets</h2><p>Upload your Bet365 Statement of All Transactions, choose the dates you want, preview the OCR-read records and then import them.</p></div><span class="bt-import-pill">Preview before import</span></div>
      <div class="bt-import-grid">
        <label style="grid-column:1/-1">Bet365 Statement of All Transactions PDF<input id="bt-import-statement" type="file" accept="application/pdf,.pdf"><small>Use Bet365's Statement of All Transactions PDF. It is read in your browser and is not saved to Bet Tracker.</small></label>
        <div style="grid-column:1/-1;padding:12px 14px;border-radius:12px;background:rgba(46,103,240,.08);border:1px solid rgba(83,130,255,.22);color:#aebfd5;font-size:12px;line-height:1.55"><strong style="color:#e8f0ff">What Bet365 provides:</strong> sport, event/market description, selection odds, result, stakes/returns, deposits and withdrawals. Bet365's PDF is image-based, so Bet Tracker reads it with OCR and shows a preview before anything is imported.</div>
        <div id="bt365-range" style="grid-column:1/-1;display:grid;grid-template-columns:repeat(2,minmax(0,220px));gap:12px"><label style="display:flex;flex-direction:column;gap:7px;font-size:12px;font-weight:700;color:#b8c6d9">Import from<input id="bt365-from" type="date" style="background:#07182e;color:#eef4ff;border:1px solid #263d5f;border-radius:10px;padding:11px 12px"></label><label style="display:flex;flex-direction:column;gap:7px;font-size:12px;font-weight:700;color:#b8c6d9">Import to<input id="bt365-to" type="date" style="background:#07182e;color:#eef4ff;border:1px solid #263d5f;border-radius:10px;padding:11px 12px"></label></div>
      </div>
      <div class="bt-import-actions"><button class="button primary" id="bt-read-import">Read Bet365 statement</button><span class="bt-import-status" id="bt-import-status">Choose the Bet365 statement and dates, then read it. Large history ranges can take a few minutes because Bet365 supplies page images.</span></div>
      <div id="bt-import-preview"></div>`;
    const close=()=>{if(activeImportPanel===p)activeImportPanel=null;back.remove();document.body.classList.remove("bt-import-open")};
    p.querySelector(".bt-import-modal-close").onclick=close;back.addEventListener("mousedown",e=>{if(e.target===back)close()});p.querySelector("#bt-read-import").onclick=analyseBet365;
    activeImportPanel=p;back.appendChild(p);document.body.appendChild(back);document.body.classList.add("bt-import-open");
  };
'''
js=js.replace(marker,opener+marker,1)
s=s[:m.start(2)]+js+s[m.end(2):]

p.write_text(s)
b=p.read_bytes()
assert len(b)==411851,len(b)
assert hashlib.sha256(b).hexdigest()=='b94e26655862dcff1c83cfe4e8c1725167972ebc2a99fd6d98b7a3f436b9c073'
for x in ['window.bt365OpenDedicated','id="bt365-dedicated-import"','BET365 HISTORY','Bet365 Statement of All Transactions PDF','if(bookmaker==="Bet365"){window.bt365OpenDedicated?.();return}']:
    assert x in s,x
ded=s[s.index('window.bt365OpenDedicated'):s.index('window.bt365RestorePaddy')]
assert 'bt-import-bookmaker' not in ded
print('Applied dedicated Bet365 importer UI:',len(b),'bytes')
