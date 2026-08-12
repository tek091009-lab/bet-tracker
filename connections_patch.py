from pathlib import Path
import hashlib
p=Path('dist/index.html')
s=p.read_text()
old='function install(){addStyles();const h=[...document.querySelectorAll("h1")].find(x=>x.textContent.trim()==="Connections");if(!h)return;'
new='function install(){addStyles();const h=[...document.querySelectorAll("h1")].find(x=>x.textContent.trim()==="Connections");if(!h){document.querySelector("#bt-import-bets")?.remove();return;}'
assert old in s
s=s.replace(old,new,1)
js=r'''<script id="bt-connections-import-nav-v1">
(()=>{
  "use strict";
  const supported={
    "Paddy Power":{
      status:"Statement import available",
      title:"Import Paddy Power bets",
      text:"Upload your Paddy Power customer statement. Stakes, results, deposits, withdrawals and opening balance can be imported. Paddy does not provide sport or description for normal sportsbook bets, so those stay blank for bulk editing afterwards."
    },
    "Bet365":{
      status:"Statement format recognised",
      title:"Bet365 statement import",
      text:"Bet365 statements include sport, bet description, selection odds, result, stakes, returns, deposits and withdrawals. This PDF format is image-based, so it needs the Bet365 OCR importer before it is enabled for one-click import."
    }
  };
  function isConnections(){return [...document.querySelectorAll("h1")].some(h=>h.textContent.trim()==="Connections")}
  function importPanel(){return document.querySelector("#bt-import-bets")}
  function setSpecific(bookmaker,scroll=true){
    const panel=importPanel();if(!panel)return;
    const info=supported[bookmaker];if(!info)return;
    panel.dataset.bookmaker=bookmaker;
    const sel=panel.querySelector("#bt-import-bookmaker");
    if(sel){const opt=[...sel.options].find(o=>o.textContent.trim().startsWith(bookmaker));if(opt&&!opt.disabled){sel.value=opt.value;sel.dispatchEvent(new Event("change",{bubbles:true}))}}
    let specific=panel.querySelector("#bt-specific-import-info");
    if(!specific){specific=document.createElement("div");specific.id="bt-specific-import-info";specific.style.cssText="margin:0 0 16px;padding:13px 14px;border-radius:12px;border:1px solid rgba(83,130,255,.24);background:rgba(46,103,240,.08);color:#aebfd5;font-size:12px;line-height:1.55";const head=panel.querySelector(".bt-import-grid");panel.insertBefore(specific,head)}
    specific.innerHTML=`<strong style="display:block;color:#edf4ff;font-size:13px;margin-bottom:3px">${info.title}</strong>${info.text}`;
    if(bookmaker==="Paddy Power"){
      panel.querySelector("#bt-import-statement")?.closest("label")?.style.removeProperty("display");
      panel.querySelector(".bt-paddy-limit")?.style.removeProperty("display");
      panel.querySelector("#bt-read-import")?.style.removeProperty("display");
    }else{
      const fileLabel=panel.querySelector("#bt-import-statement")?.closest("label");if(fileLabel)fileLabel.style.display="none";
      const lim=panel.querySelector(".bt-paddy-limit");if(lim)lim.style.display="none";
      const read=panel.querySelector("#bt-read-import");if(read)read.style.display="none";
      const st=panel.querySelector("#bt-import-status");if(st){st.textContent="Bet365 import is not enabled until the image-based statement reader is finished.";st.className="bt-import-status"}
      panel.querySelector("#bt-import-preview")?.replaceChildren();
    }
    if(scroll)panel.scrollIntoView({behavior:"smooth",block:"start"});
  }
  function syncCards(){
    if(!isConnections())return;
    document.querySelectorAll(".connection-card").forEach(card=>{
      const name=card.querySelector("h3")?.textContent.trim();const btn=card.querySelector(":scope > button");if(!name||!btn)return;
      const info=supported[name];
      if(name==="Paddy Power"){
        const status=card.querySelector(".connection-status");if(status){status.textContent=info.status;status.classList.remove("muted")}
        const p=card.querySelector("p");if(p)p.textContent="Customer statement PDF import is available. Sport and description are left blank because Paddy does not supply them in the statement.";
        btn.disabled=false;btn.textContent="Import";btn.dataset.btImportButton="1";btn.onclick=()=>setSpecific(name,true);
      } else if(name==="Bet365"){
        const status=card.querySelector(".connection-status");if(status)status.textContent=info.status;
        const p=card.querySelector("p");if(p)p.textContent="The statement contains detailed bet data, but the PDF is image-based. Import will be enabled once the OCR reader is active.";
        btn.disabled=true;btn.textContent="Reader being added";
      }
    });
    const panel=importPanel();if(panel&&!panel.dataset.bookmaker)setSpecific("Paddy Power",false);
  }
  const mo=new MutationObserver(()=>setTimeout(syncCards,0));mo.observe(document.getElementById("bet-tracker-root")||document.body,{subtree:true,childList:true});
  window.addEventListener("bt:open-import",e=>setSpecific(e.detail?.bookmaker||"Paddy Power",true));
  syncCards();
})();
</script>'''
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s)
b=p.read_bytes()
assert len(b)==390403,len(b)
assert hashlib.sha256(b).hexdigest()=='7cb8a414978f990298d03741dd0c16c5c412c638b196d213ba01d6ad6eebbd24'
for x in ['bt-connections-import-nav-v1','document.querySelector("#bt-import-bets")?.remove()','Statement import available','Reader being added']:
    assert x in s,x
print('Applied Connections-only import navigation:',len(b),'bytes')
