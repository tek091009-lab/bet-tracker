from pathlib import Path
import hashlib
p=Path('dist/index.html')
s=p.read_text()

# 1. The importer lives on document.body as a hidden modal. Check globally so the
# Connections MutationObserver cannot create another copy on every DOM mutation.
old='if(!root||root.querySelector("#bt-import-bets"))return;'
new='if(!root||document.querySelector("#bt-import-bets"))return;'
assert s.count(old)==1
s=s.replace(old,new,1)

# 2. Moving an already-body-owned hidden panel back to body is itself a DOM
# mutation. Only move it when it is actually inside the modal backdrop.
old='if(p){p.style.display="none";p.classList.remove("bt-modal-open");document.body.appendChild(p)}'
new='if(p){p.style.display="none";p.classList.remove("bt-modal-open");if(p.parentNode!==document.body)document.body.appendChild(p)}'
assert s.count(old)==1
s=s.replace(old,new,1)

# 3. Navigation cleanup must be a no-op unless a modal is genuinely open.
old='if(!isConnections()){closeModal();return}'
new='if(!isConnections()){if(document.querySelector("#bt-import-modal-backdrop")||document.body.classList.contains("bt-import-open"))closeModal();return}'
assert s.count(old)==1
s=s.replace(old,new,1)

# 4. Coalesce rapid React DOM mutations into one sync rather than queueing an
# unbounded number of setTimeout callbacks during page navigation.
old='const mo=new MutationObserver(()=>setTimeout(sync,0));mo.observe(document.getElementById("bet-tracker-root")||document.body,{subtree:true,childList:true});sync();'
new='let syncQueued=false;const mo=new MutationObserver(()=>{if(syncQueued)return;syncQueued=true;setTimeout(()=>{syncQueued=false;sync()},0)});mo.observe(document.getElementById("bet-tracker-root")||document.body,{subtree:true,childList:true});sync();'
assert s.count(old)==1
s=s.replace(old,new,1)

p.write_text(s)
b=p.read_bytes()
assert len(b)==393705,len(b)
assert hashlib.sha256(b).hexdigest()=='9e5c9cef73dd61a562d2ad3838646d105be4b9529e50848cbfc3fc8b366b1a4b'
for marker in [
    'document.querySelector("#bt-import-bets"))return',
    'if(p.parentNode!==document.body)document.body.appendChild(p)',
    'syncQueued=false',
    'bt-connections-card-import-v2'
]:
    assert marker in s,marker
print('Applied navigation crash hotfix:',len(b),'bytes')
