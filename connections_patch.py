from pathlib import Path
import hashlib
p=Path('dist/index.html')
s=p.read_text()

# Keep the full importer out of the Connections page layout. It exists only as a hidden modal opened from bookmaker cards.
old='grid.parentNode.insertBefore(el,grid);bind(el)}'
new='document.body.appendChild(el);el.classList.add("bt-import-modal-panel");el.style.display="none";bind(el)}'
assert old in s
s=s.replace(old,new,1)

js=r'''<script id="bt-connections-card-import-v2">
(()=>{
  "use strict";
  const BOOKMAKERS={
    "Paddy Power":{live:true,title:"Import Paddy Power bets",text:"Upload your Paddy Power customer statement. Bet Tracker can import stakes, results, deposits, withdrawals and the opening balance. Paddy does not include the sport, event, market or selection for normal sportsbook bets, so Sport and Description stay blank for bulk editing afterwards."},
    "Bet365":{live:false,title:"Import Bet365 bets",text:"Your Bet365 statement format is recognised. It contains sport, description, odds, result, stakes, returns, deposits and withdrawals. The statement is image-based, so the dedicated table reader is still being added before one-click importing is enabled."},
    "Betfair":{live:false,title:"Import Betfair bets",text:"Betfair has an official account/API route. Direct account importing is planned through that approved route rather than asking for your bookmaker password."},
    "William Hill":{live:false,title:"Import William Hill bets",text:"William Hill statement/history importing is being prepared. Once the export format is mapped, this button will accept the supported statement directly."},
    "Betfred":{live:false,title:"Import Betfred bets",text:"Betfred statement/history importing is being prepared. Once the export format is mapped, this button will accept the supported statement directly."},
    "Ladbrokes":{live:false,title:"Import Ladbrokes bets",text:"Ladbrokes statement/history importing is being prepared. Once the export format is mapped, this button will accept the supported statement directly."},
    "Sky Bet":{live:false,title:"Import Sky Bet bets",text:"Sky Bet history importing is being prepared. Once the export format is mapped, this button will accept the supported statement directly."}
  };
  const isConnections=()=>[...document.querySelectorAll("h1")].some(h=>h.textContent.trim()==="Connections");
  const panel=()=>document.querySelector("#bt-import-bets");
  function closeModal(){
    const back=document.querySelector("#bt-import-modal-backdrop");
    const p=panel();
    if(p){p.style.display="none";p.classList.remove("bt-modal-open");document.body.appendChild(p)}
    back?.remove();
    document.body.classList.remove("bt-import-open");
  }
  function makeBackdrop(){
    document.querySelector("#bt-import-modal-backdrop")?.remove();
    const b=document.createElement("div");b.id="bt-import-modal-backdrop";b.className="bt-import-modal-backdrop";
    b.addEventListener("mousedown",e=>{if(e.target===b)closeModal()});
    document.body.appendChild(b);return b;
  }
  function setPaddyPanel(p){
    const h2=p.querySelector(".bt-import-head h2");if(h2)h2.textContent="Import Paddy Power bets";
    const intro=p.querySelector(".bt-import-head p");if(intro)intro.textContent="Upload your Paddy Power statement, choose the dates you want, preview the records and import them into your account.";
    const bookLabel=p.querySelector("#bt-import-bookmaker")?.closest("label");if(bookLabel)bookLabel.style.display="none";
    const fileLabel=p.querySelector("#bt-import-statement")?.closest("label");if(fileLabel){fileLabel.style.display="flex";fileLabel.style.gridColumn="1/-1"}
    p.querySelector(".bt-paddy-limit")?.style.removeProperty("display");
    p.querySelector("#bt-read-import")?.style.removeProperty("display");
    let info=p.querySelector("#bt-bookmaker-import-info");if(info)info.remove();
  }
  function openLive(bookmaker){
    const p=panel();if(!p)return;
    if(bookmaker==="Paddy Power")setPaddyPanel(p);
    const back=makeBackdrop();
    let close=p.querySelector(".bt-import-modal-close");
    if(!close){close=document.createElement("button");close.type="button";close.className="bt-import-modal-close";close.setAttribute("aria-label","Close import");close.textContent="×";close.onclick=closeModal;p.appendChild(close)}
    back.appendChild(p);p.style.display="block";p.classList.add("bt-modal-open");document.body.classList.add("bt-import-open");
  }
  function openInfo(bookmaker){
    const info=BOOKMAKERS[bookmaker];if(!info)return;
    const back=makeBackdrop();
    const box=document.createElement("section");box.className="bt-import-info-modal";
    box.innerHTML=`<button class="bt-import-modal-close" type="button" aria-label="Close import">×</button><p class="eyebrow">BOOKMAKER HISTORY</p><h2>${info.title}</h2><p>${info.text}</p><div class="bt-import-info-actions"><button type="button" class="button" data-close>Close</button></div>`;
    box.querySelector(".bt-import-modal-close").onclick=closeModal;box.querySelector("[data-close]").onclick=closeModal;back.appendChild(box);document.body.classList.add("bt-import-open");
  }
  function openImport(bookmaker){const info=BOOKMAKERS[bookmaker];if(!info)return;if(info.live)openLive(bookmaker);else openInfo(bookmaker)}
  function sync(){
    if(!isConnections()){closeModal();return}
    document.querySelectorAll(".connection-card").forEach(card=>{
      const name=card.querySelector("h3")?.textContent.trim();if(!name||!BOOKMAKERS[name])return;
      if(card.querySelector(".bt-card-import"))return;
      const b=document.createElement("button");b.type="button";b.className="bt-card-import";b.textContent="Import";b.onclick=e=>{e.preventDefault();e.stopPropagation();openImport(name)};card.appendChild(b);
    });
  }
  const style=document.createElement("style");style.id="bt-connections-card-import-style";style.textContent=`
    .connection-card{grid-template-columns:auto 1fr auto auto!important}
    .connection-card>.bt-card-import{padding:8px 12px;border:1px solid rgba(69,119,255,.45);border-radius:7px;background:rgba(46,103,240,.14);color:#bcd0ff;font-size:9px;font-weight:800;cursor:pointer}
    .connection-card>.bt-card-import:hover{background:rgba(46,103,240,.24);color:#eef4ff}
    #bt-import-bets.bt-import-modal-panel{position:relative;margin:0;width:min(1120px,calc(100vw - 40px));max-height:calc(100vh - 50px);overflow:auto;box-sizing:border-box;z-index:10002}
    .bt-import-modal-backdrop{position:fixed;z-index:10000;inset:0;display:grid;place-items:center;padding:24px;background:rgba(0,8,18,.82);backdrop-filter:blur(8px)}
    .bt-import-modal-close{position:absolute;top:14px;right:14px;z-index:5;width:34px;height:34px;border:1px solid rgba(139,174,209,.25);border-radius:9px;background:#0a1d34;color:#b6c8dc;font-size:22px;line-height:1;cursor:pointer}
    .bt-import-info-modal{position:relative;width:min(620px,calc(100vw - 40px));padding:26px;border:1px solid rgba(91,139,255,.24);border-radius:18px;background:linear-gradient(145deg,#0e233f,#071427);box-shadow:0 35px 100px rgba(0,0,0,.55);color:#eaf2ff}
    .bt-import-info-modal h2{margin:5px 0 10px;font-size:23px}.bt-import-info-modal>p:last-of-type{margin:0;color:#9db0c9;font-size:12px;line-height:1.65;max-width:540px}.bt-import-info-actions{display:flex;justify-content:flex-end;margin-top:20px}
    body.bt-import-open{overflow:hidden}
    @media(max-width:760px){.connection-card{grid-template-columns:auto 1fr auto!important}.connection-card>.bt-card-import{grid-column:2/-1;justify-self:end}.bt-import-modal-backdrop{padding:12px}#bt-import-bets.bt-import-modal-panel{width:calc(100vw - 24px);max-height:calc(100vh - 24px)}}
  `;document.head.appendChild(style);
  document.addEventListener("keydown",e=>{if(e.key==="Escape"&&document.querySelector("#bt-import-modal-backdrop"))closeModal()});
  const mo=new MutationObserver(()=>setTimeout(sync,0));mo.observe(document.getElementById("bet-tracker-root")||document.body,{subtree:true,childList:true});sync();
})();
</script>'''
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s)
b=p.read_bytes()
assert len(b)==393477,len(b)
assert hashlib.sha256(b).hexdigest()=='b0ee18f785f0fec55731ee3d619ac867c32693655eb282861d4b54ade9b4595c'
for x in ['bt-connections-card-import-v2','bt-card-import','Import Paddy Power bets','bt-import-modal-backdrop','document.body.appendChild(el);el.classList.add("bt-import-modal-panel")']:
    assert x in s,x
print('Applied bookmaker-card import modals:',len(b),'bytes')
