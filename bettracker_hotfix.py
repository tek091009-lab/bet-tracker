from pathlib import Path
import hashlib
p=Path('dist/index.html')
s=p.read_text()

# The bulk selector must not insert extra TD/TH elements into React-owned tables.
# React can re-render those rows and fight the external DOM changes until the page locks up.
old='''  function syncRows(){
    const rows=visibleRows();
    rows.forEach((tr,idx)=>{
      const id=tr.dataset.betId;if(!id)return;
      if(!tr.querySelector("td.bt-select-cell")){
        const td=document.createElement("td");td.className="bt-select-cell";td.innerHTML=`<input type="checkbox" class="bt-row-select" aria-label="Select bet">`;tr.insertBefore(td,tr.firstChild);
        const cb=td.firstElementChild;
        cb.addEventListener("click",e=>{e.stopPropagation();selectId(id,idx,{shift:e.shiftKey,add:true});updateUi()});
      }
      if(!tr.dataset.bulkBound){
        tr.dataset.bulkBound="1";
        tr.addEventListener("click",e=>{if(e.target.closest("button,input,select,a,label"))return;e.preventDefault();selectId(id,idx,{shift:e.shiftKey,add:e.ctrlKey||e.metaKey});updateUi()});
      }
    });
    const head=document.querySelector(".bet-table thead tr");if(head&&!head.querySelector("th.bt-select-col")){const th=document.createElement("th");th.className="bt-select-col";th.title="Select bets";head.insertBefore(th,head.firstChild)}
  }'''
new='''  function syncRows(){
    const rows=visibleRows();
    rows.forEach((tr,idx)=>{
      const id=tr.dataset.betId;if(!id)return;
      if(!tr.dataset.bulkBound){
        tr.dataset.bulkBound="1";
        tr.addEventListener("click",e=>{if(e.target.closest("button,input,select,a,label"))return;e.preventDefault();selectId(id,idx,{shift:e.shiftKey,add:e.ctrlKey||e.metaKey});updateUi()});
      }
    });
  }'''
assert s.count(old)==1
s=s.replace(old,new,1)

# Coalesce React mutations and observe only the app root rather than the full document.
old='  const mo=new MutationObserver(()=>install());mo.observe(document.documentElement,{childList:true,subtree:true});install();'
new='  let bulkInstallQueued=false;const mo=new MutationObserver(()=>{if(bulkInstallQueued)return;bulkInstallQueued=true;requestAnimationFrame(()=>{bulkInstallQueued=false;install()})});mo.observe(document.getElementById("bet-tracker-root")||document.body,{childList:true,subtree:true});install();'
assert s.count(old)==1
s=s.replace(old,new,1)

p.write_text(s)
b=p.read_bytes()
assert len(b)==393221,len(b)
assert hashlib.sha256(b).hexdigest()=='d980668a46c6deb42b451d6b231e56aae89e0c527de9f32178ce6b9ad98d04fd'
assert 'tr.insertBefore(td,tr.firstChild)' not in s
assert 'head.insertBefore(th,head.firstChild)' not in s
assert 'bulkInstallQueued=false' in s
print('Applied Bet Tracker React table hotfix:',len(b),'bytes')
