from pathlib import Path
import re,hashlib,base64,gzip

p=Path("dist/index.html")
s=p.read_text()
m=re.search(r'<script id="bt-bet365-import-v1">\n(.*?)\n</script>',s,re.S)
assert m, "current Bet365 importer script missing"

blob=''.join(Path("bet365_grid_v2.b64").read_text().split())
js=gzip.decompress(base64.b64decode(blob)).decode()
assert len(js.encode())==34963
assert hashlib.sha256(js.encode()).hexdigest()=="4d1d9f7757c4c35481456c1e4e1e491694625d038cbb2bc83e2698fd54c9fa62"

s=s[:m.start()]+'<script id="bt-bet365-import-v2">\n'+js+'\n</script>'+s[m.end():]
p.write_text(s)
b=p.read_bytes()
assert len(b)==418741,len(b)
assert hashlib.sha256(b).hexdigest()=="d212d57eb8ebe443459d91d50746d75b42a797f4f5601d36756fe10dee41a49a"
for x in ["bt-bet365-import-v2","GRID_RATIOS","detectTableGrid","ocrGridPage","Grid-verified Bet365 import","window.bt365OpenDedicated",'id="bt365-dedicated-import"']:
    assert x in s,x
assert "bt-bet365-import-v1" not in s
print("Applied Bet365 grid-first importer v2:",len(b),"bytes")
