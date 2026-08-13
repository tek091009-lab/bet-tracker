from pathlib import Path
import hashlib

p=Path('dist/index.html')
b=p.read_bytes()
assert len(b)==421962,len(b)
assert hashlib.sha256(b).hexdigest()=='65a8899cfc1a76f9ba6ee9dc5dbefd66c626c456e1776565476627b68f23f737'
s=b.decode()
assert 'bt365-viewport-layout-fix-v1' not in s

style='''
<style id="bt365-viewport-layout-fix-v1">
#bt365-dedicated-import{
  width:min(1180px,calc(100vw - 24px))!important;
  height:min(920px,calc(100dvh - 24px));
  max-height:calc(100dvh - 24px)!important;
  overflow-y:auto!important;
  overflow-x:hidden!important;
  overscroll-behavior:contain;
  scrollbar-gutter:stable;
}
#bt365-dedicated-import .bt-import-modal-close{position:sticky;top:10px;float:right;margin:0 0 -34px 10px;z-index:30}
#bt365-dedicated-import .bt-import-table{max-height:min(32vh,300px)!important;overflow:auto!important}
#bt365-dedicated-import #bt365-raw-table .bt-import-table{max-height:min(28vh,250px)!important}
#bt365-dedicated-import .bt-import-table table{max-width:100%;}
#bt365-dedicated-import .bt-import-table th,#bt365-dedicated-import .bt-import-table td{overflow-wrap:anywhere;word-break:normal}
#bt365-dedicated-import .bt-import-final{
  position:sticky;bottom:0;z-index:25;
  margin:14px -16px -16px;padding:14px 16px;
  background:linear-gradient(180deg,rgba(7,20,39,.94),#071427 28%);
  border-top:1px solid rgba(91,139,255,.22);
  box-shadow:0 -14px 30px rgba(0,0,0,.28);
}
#bt365-dedicated-import #bt365-confirm{flex:0 0 auto}
@media(max-width:760px){
  #bt365-dedicated-import{width:calc(100vw - 12px)!important;height:calc(100dvh - 12px);max-height:calc(100dvh - 12px)!important}
  #bt365-dedicated-import .bt-import-table{max-height:28vh!important}
  #bt365-dedicated-import .bt-import-final{margin-left:-8px;margin-right:-8px;padding-left:10px;padding-right:10px}
}
</style>
'''

s=s.replace('</head>',style+'</head>',1)
p.write_text(s)
b=p.read_bytes()
assert len(b)==423486,len(b)
assert hashlib.sha256(b).hexdigest()=='7feb4b213058a71963577a8cec22a77b55ec04da603f5c31693917ddb3529435'
print('Applied Bet365 viewport layout fix:',len(b),'bytes')
