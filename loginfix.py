from pathlib import Path
p=Path('dist/index.html')
s=p.read_text()
old='const out=await client.auth.signInWithPassword({email:emailFor(username),password});if(out.error)throw new Error(mode==="login"?"Username or password is incorrect.":out.error.message);'
new='let out=await client.auth.signInWithPassword({email:emailFor(username),password});if(out.error&&mode==="login")out=await client.auth.signInWithPassword({email:`${username}@users.holidaysavings.app`,password});if(out.error)throw new Error(mode==="login"?"Username or password is incorrect.":out.error.message);'
assert old in s
s=s.replace(old,new,1)
p.write_text(s)
